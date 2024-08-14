from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import discord
from captcha.image import ImageCaptcha
import random
from bot import DiscordBot
import string
import os
from modules.environment import ROLE_ADMIN
from modules.buttons import VerifyButton

# Here we name the cog and create a new class for the cog.
class Verifier(commands.Cog, name="verifier"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="verify",
        description="This is example for verifier.",
    )
    async def verify_user(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        image = ImageCaptcha(width=280, height=90)
        
        captcha_text = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
        
        data = image.generate(captcha_text)
        
        role_has = discord.utils.get(context.guild.roles, name="Verified")
        
        if role_has in context.author.roles:
            context.reply("You are already verified", ephemeral=True)
        else:
            await context.reply("Check your dms", ephemeral=True)
            
            image.write(captcha_text, f"{os.path.dirname(os.path.dirname(__file__))}/resources/image/CAPTCHA.png")
            
            await context.author.send("Please verify from this captcha", file=discord.File(f"{os.path.dirname(os.path.dirname(__file__))}/resources/image/CAPTCHA.png"))
            
            print(captcha_text)
            
            while True:
                msg = await self.bot.wait_for("message", check=lambda check: check.author.id == context.author.id)
                if msg.guild == None:
                    break
            
            print(msg.content)
            
            if msg.content.lower() == captcha_text.lower():
                await context.author.send("Correct!")
                role = discord.utils.get(context.guild.roles, name="Verified")
                await context.author.add_roles(role)
            else:
                await context.author.send("Incorrect captcha")

    @commands.hybrid_command(
        name="insert_verify",
        description= "Send verify message to a channel"
    )
    @commands.has_role(ROLE_ADMIN)
    @app_commands.describe(
        channel="Channel to send to"
    )
    async def send_verify(self, context: Context, channel: discord.TextChannel) -> None:
        channel = context.guild.get_channel(channel.id)
        await channel.send(content="Button", view=VerifyButton())
        
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Verifier(bot))
