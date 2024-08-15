import discord
from discord.ext import commands


class VerifyEmbed(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        
    @discord.ui.button(label="Verify Test", style=discord.ButtonStyle.green)
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(button)
        print(interaction)
        button.disabled = True
        await interaction.response.send_message(content="TEstsetests", view=self, ephemeral=True)