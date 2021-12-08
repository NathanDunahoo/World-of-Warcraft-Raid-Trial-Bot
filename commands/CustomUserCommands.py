import discord
from discord.ext import commands
import os

"""
Contains all User Defined Commands
"""
class CustomUserCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pimmy(self, ctx):
        file = r'./media/FENNECFRIDAY.mp4'
        if os.path.exists(file):
            await ctx.send(file=discord.File(file))

def setup(client):
    client.add_cog(CustomUserCommands(client))