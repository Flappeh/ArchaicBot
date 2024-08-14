import discord
from discord.ext import commands


class VerifyButton(discord.ui.View):
    def __init__(self, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.add_item(discord.ui.Button(label="Verify",custom_id="verify", style=discord.ButtonStyle.green))
        
        @discord.ui.button(custom_id="verify")
        async def verify_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            print(interaction.user)
            await interaction.user.send(f"Hello")