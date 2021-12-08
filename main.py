#!/usr/bin/python3
import os
from discord.ext import commands
from core import ErrorHandling

client = commands.Bot(command_prefix='!')

cog_files = ['TrialCommands', 'CustomUserCommands']
for cog_file in cog_files:
    client.load_extension(f"commands.{cog_file}")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.add_cog(ErrorHandling.ErrorHandler(client))

@client.command()
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await ctx.bot.logout()

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))

