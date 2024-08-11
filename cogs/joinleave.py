from discord.ext import commands
from discord.ext.commands import Context
from discord import File
import discord
from modules.environment import CHANNEL_WELCOME, CHANNEL_LEAVE, ROLE_ADMIN
from bot import DiscordBot
from modules.utils import logger
from easy_pil import Editor, load_image_async, Font
import os
import random
from captcha.image import ImageCaptcha
import string
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
        name="captcha",
        description="Test send captcha"
    )
    async def send_captcha_verification(self, context: Context) -> None:
        try:
            image = ImageCaptcha(width=280,height=90)
            code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
            captcha_text = str(code)
            data = image.generate(captcha_text)
            
            role_verified = discord.utils.get(context.guild.roles, name="Verified")
            
            if role_verified in context.author.roles:
                await context.reply(f"You are already verified!", ephemeral=True)
            else:
                await context.reply(f"Check your DM", ephemeral=True)
                
                image.write(captcha_text, 'captcha/CAPTCHA.png')
                
                await context.author.send("Write what the captcha has")
            
        except Exception as e:
            print(e)
    
    @commands.hybrid_command(
        name="testimage",
        description="Test send image",
    )
    @commands.has_role(ROLE_ADMIN)
    async def test_image(self, context: Context) -> None:
        """
        Test sending image to the server
        """
        try:
            file = await self.getImageBackground(context.author)
            await context.send(file=file)
        except Exception as e:
            raise Exception(e)
    
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member) -> None:
        """
        This runs everytime a user joins the server
        """
        channel = None
        file = None
        try:
            channel = self.bot.get_channel(CHANNEL_WELCOME)
            file = await self.getImageBackground(member)
        except commands.ChannelNotFound as e:
            logger.error(f"Error retrieving welcome channel with id : {channel}")
            raise commands.ChannelNotFound(f"Unable to retrieve welcome channel from id : {e}")
        embed = discord.Embed(
            description=f"**New User Joined!** Welcome {member.mention}",
            color=0x14e4ef,
        )
        await channel.send(file=file)
        await channel.send(embed=embed)
        
    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member) -> None:
        """
        This runs everytime a user leaves the server
        """
        channel = None
        file = None
        try:
            channel = self.bot.get_channel(CHANNEL_LEAVE)
            file = await self.getImageBackground(member)
        except commands.ChannelNotFound as e:
            logger.error(f"Error retrieving welcome channel with id : {channel}")
            raise commands.ChannelNotFound(f"Unable to retrieve welcome channel from id : {e}")
        embed = discord.Embed(
            description=f"**User Left!** Bye {member}",
            color=0xd62e11,
        )
        await channel.send(file=file)
        await channel.send(embed=embed)
        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(JoinLeave(bot))
