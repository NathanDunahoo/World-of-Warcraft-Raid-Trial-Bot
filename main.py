#!/usr/bin/python3
from discord import Embed
from os import getenv
from discord.ext import commands, tasks
from sqlite3 import IntegrityError
import ErrorHandling
from TrialManager import TrialManager

client = commands.Bot(command_prefix='!')
tm = TrialManager()

@client.event
async def on_ready():
    print(f'We have logged in as {client}')
    client.add_cog(ErrorHandling.ErrorHandler(client))

@client.command()
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await ctx.bot.logout()

@client.command()
async def add_trial(ctx, name, _class, spec, logs=''):
    """
    Discord command for adding a new trial
    Checks if class and spec are valid
    Adds a new trial to the DB

    :param ctx: commands.Context
    :param name: str trial's name ('Notey')
    :param _class: str trial's WoW class (paladin, warlock, mage)
    :param spec:  str trial's WoW class specification (prot, afflication, frost)
    :param logs: str url to trial's Warcraft logs (optional can be added later)
    :return: None
    """
    try:
        ErrorHandling.check_valid_class_spec(_class, spec)
    except ErrorHandling.ClassError:
        await ctx.send(f"{_class} is not a valid class {ErrorHandling.valid_classes}")
        return
    except ErrorHandling.SpecError:
        await ctx.send(f"{spec} is not a valid spec for {_class} {ErrorHandling.valid_specs[_class]}")
        return
    try:
        trial = tm.add_trial(name, _class, spec, logs)
        await ctx.send(embed=trial.get_embed())
    except IntegrityError:
        await ctx.send(f"{name} is already a trial")

@client.command()
async def list_trials(ctx):
    """
    Creates an Embed object for the Discord message
    Gets a trial list list[tuple]
    Sorts list by their days as a trial

    :param ctx: commands.Context
    :return: None
    """
    list_of_sorted_trials: list[tuple] = tm.get_all_trials_as_tuple()
    list_of_sorted_trials.sort(key=lambda x: x[3], reverse=True)

    embed = Embed(title="Current Trials", color=0x33B5FF)
    for trial in list_of_sorted_trials:
        trial = tm.get_Trial_by_name(trial[0])
        value_desc = f"Class: {trial.get_class()}\nSpec: {trial.spec}\n Days as Trial: {trial.get_days_as_a_trial()}\n [Logs]({trial.logs})"
        embed.add_field(name=trial.name, value=value_desc)
    await ctx.send(embed=embed)

@client.command()
async def get_status(ctx, trial: tm.get_Trial_by_name):
    """
    Discord Command for sending the status of the trial (Name, Class, Spec, Logs, Days as trial) all in an Embed

    :param ctx: commands.Context
    :param trial: Trial from get_Trial_by_name
    :return: None
    """
    await ctx.send(embed=trial.get_embed())

@client.command()
async def promote_trial(ctx, trial: tm.get_Trial_by_name):
    """
    Discord command for promoting a trial

    :param ctx: Discord Bot
    :param trial: Trial from get_Trial_by_name
    :return: None
    """

    tm.promote_trial(trial)
    await ctx.send(f"{trial} has been promoted")


@client.command()
async def remove_trial(ctx, trial: tm.get_Trial_by_name):
    """
    Discorc command for removing a trial

    *Same as promote_trial()

    :param ctx: commands.Context
    :param trial: Trial from get_Trial_by_name
    :return: None
    """

    tm.promote_trial(trial)
    await ctx.send(f"{trial.name} has been removed")

@client.command()
async def change_start_date(ctx, trial: tm.get_Trial_by_name, new_date: str):
    # TODO add date verification/error handling
    """
    Updates a trial's join date

    :param ctx: commands.Context
    :param trial: Trial from get_Trial_by_name
    :param new_date: str '2021-11-30'
    :return: None
    """

    tm.change_start_date(trial, new_date)
    await ctx.send(f"{trial.name}'s start date has been updated to {new_date}")


@client.command()
async def make_inactive(ctx, trial: tm.get_Trial_by_name):
    """
    Discord command for moving trial's status to 'inactive' or '0'

    :param ctx: commands.Context
    :param trial: Trial from get_Trial_by_name
    :return: None
    """

    tm.make_inactive(trial, "0")
    await ctx.send(f"{trial.name} has been made inactive")

@client.command()
async def add_logs(ctx, trial: tm.get_Trial_by_name, logs: str):
    """
    Discord command for adding/updating logs to a trial
    
    :param ctx: Dcommands.Context
    :param trial: Trial from get_Trial_by_name
    :param logs: str url for trial's Warcraft logs ('https://www.warcraftlogs.com/character/id/55296682')
    :return: None
    """

    tm.add_logs(trial, logs)
    await ctx.send(f"{trial.name}'s logs have been updated to {logs}")

# TODO fix this
@tasks.loop(hours=24)
async def check_for_promotions():
    print("starting checks")
    for trial in tm.trial_list:
        if trial.check_for_promotion():
            pass


if __name__ == '__main__':
    client.run(getenv('TOKEN'))

