#!/usr/bin/python3
from discord.ext import commands
from definitions import TOKEN

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

cog_files = ['TrialCommands', 'CustomUserCommands']  # Define command file here
for cog_file in cog_files:
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

