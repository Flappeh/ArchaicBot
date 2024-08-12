import discord
from discord.ext import commands


class VerifyButton(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)