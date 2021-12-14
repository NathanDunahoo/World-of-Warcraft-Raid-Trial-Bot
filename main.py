#!/usr/bin/python3
from discord import HTTPException
from discord.ext import commands
from definitions import TOKEN, ROOT_DIR
from os import listdir, path
from worldofwarcraft import WowData

client = commands.Bot(command_prefix='!')

"""
Welcome to my Discord Bot - Made by Notey#0001

This is written using the Discord library (https://discordpy.readthedocs.io/en/stable/) in Python3+

The main purpose of this bot was to manage our World of Warcraft raid roster, but is slowly expanding into a 
general purpose bot. 

Command files can be found on the commands directory - including a file for CustomCommands

To get started you will need an environment variable ('TOKEN') for your Discord developer token
https://discord.com/developers/applications/

"""

if path.exists(path.join(ROOT_DIR, 'commands')):
    command_files = [f.split('.')[0] for f in listdir('./commands') if f.endswith('.py')]
else:
    command_files = []
for cog_file in command_files:
    client.load_extension(f"commands.{cog_file}")


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.BadArgument):
            err_message: str = f'{error}'
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, HTTPException):
            err_message: str = f'{error}'
        elif isinstance(error, WowData.ClassError):
            wd = WowData.WowData()
            err_message = f'Class not valid: {wd.get_classes()}'
        else:
            err_message: str = f"Something went wrong :( {error}"
        await ctx.send(err_message)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.add_cog(ErrorHandler(client))

@client.command()
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await ctx.bot.logout()

if __name__ == '__main__':
    client.run(TOKEN)

