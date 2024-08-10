from discord.ext import commands
from discord.ext.commands import Context
from discord import File
import discord
from modules.environment import WELCOME_CHANNEL_ID, LEAVE_CHANNEL_ID
from bot import DiscordBot
from modules.utils import logger
from easy_pil import Editor, load_image_async, Font
import os
import random

class JoinLeave(commands.Cog, name="joinleave"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot
        self.images = list()
        self.load_background_images()
        
    def load_background_images(self) -> None:
        for file in os.listdir(f"{os.path.dirname(os.path.dirname(__file__))}/resources/image"):
            if file.startswith("background"):
                self.images.append(f"{os.path.dirname(os.path.dirname(__file__))}/resources/image/{file}")
                
    async def getImageBackground(self, member: discord.Member):
        background = Editor(random.choice(self.images))
        profile_image = await load_image_async(str(member.avatar.url))
        background_width = float(background.image.size[0])
        background_height = float(background.image.size[1])
        
        profile = Editor(profile_image).resize((150,150)).circle_image()
        
        poppins = Font.poppins(size=50,variant="bold")
        poppins_small = Font.poppins(size=30,variant="regular")
        
        background.paste(profile,(int(background_width/2-75),int(background_height/3-75)))
        background.ellipse((int(background_width/2-75),int(background_height/3-75)),150,150, outline="white", stroke_width=5)
        
        background.text((int(background_width/2),260), f"Welcome to {member.guild.name}", color="white", font=poppins, align="center",stroke_width=1)
        background.text((int(background_width/2),325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center",stroke_width=1)
        
        file = File(fp=background.image_bytes, filename="pic.jpg")
        
        return file
    
    @commands.hybrid_command(
        name="testimage",
        description="Test send image",
    )
    @commands.is_owner()
    async def botinfo(self, context: Context) -> None:
        """
        Test sending image to the server
        """
        file = await self.getImageBackground(context.author)
        await context.send(file=file)
    
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.member) -> None:
        """
        This runs everytime a user joins the server
        """
        channel = None
        file = None
        try:
            channel = self.bot.get_channel(int(WELCOME_CHANNEL_ID))
            file = await self.getImageBackground(member)
        except commands.ChannelNotFound as e:
            logger.error(f"Error retrieving welcome channel with id : {channel}")
            raise commands.ChannelNotFound(f"Unable to retrieve welcome channel from id : {e}")
        embed = discord.Embed(
            description=f"**New User Joined!** Welcome {member}",
            color=0xE02B2B,
        )
        await channel.send(embed=embed)
        await channel.send(file=file)
        
    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member) -> None:
        """
        This runs everytime a user leaves the server
        """
        channel = None
        file = None
        try:
            channel = self.bot.get_channel(int(LEAVE_CHANNEL_ID))
            file = await self.getImageBackground(member)
        except commands.ChannelNotFound as e:
            logger.error(f"Error retrieving welcome channel with id : {channel}")
            raise commands.ChannelNotFound(f"Unable to retrieve welcome channel from id : {e}")
        embed = discord.Embed(
            description=f"**User Left!** Bye {member}",
            color=0xE02B2B,
        )
        await channel.send(embed=embed)
        await channel.send(file=file)
        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(JoinLeave(bot))
