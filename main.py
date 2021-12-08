#!/usr/bin/python3
from discord import Embed
from os import getenv
from discord.ext import commands, tasks
from sqlite3 import IntegrityError
import ClassSpecVerifier
from TrialManager import TrialManager
from TrialModel import Trial

client = commands.Bot(command_prefix='!')
trial_manager = TrialManager()

@client.event
async def on_ready():
    print(f'We have logged in as {client}')
    check_for_promotions.start()

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

    :param ctx: Discord Bot
    :param name: str trial's name ('Notey')
    :param _class: str trial's WoW class (paladin, warlock, mage)
    :param spec:  str trial's WoW class specification (prot, afflication, frost)
    :param logs: str url to trial's Warcraft logs (optional can be added later)
    :return: None
    """
    try:
        ClassSpecVerifier.check_valid_class_spec(_class, spec)
    except ClassSpecVerifier.ClassError:
        await ctx.send(f"{_class} is not a valid class {ClassSpecVerifier.valid_classes}")
        return
    except ClassSpecVerifier.SpecError:
        await ctx.send(f"{spec} is not a valid spec for {_class} {ClassSpecVerifier.valid_specs[_class]}")
        return
    try:
        trial = trial_manager.add_trial(name, _class, spec, logs)
        await ctx.send(embed=trial.get_embed())
    except IntegrityError:
        await ctx.send(f"{name} is already a trial")

@client.command()
async def list_trials(ctx):
    """
    Creates an Embed object for the Discord message
    Gets a trial list list[tuple]
    Sorts list by their days as a trial

    :param ctx: Discord Bot
    :return: None
    """
    list_of_sorted_trials: list[tuple] = trial_manager.get_all_trials_as_tuple()
    list_of_sorted_trials.sort(key=lambda x: x[3], reverse=True)

    embed = Embed(title="Current Trials", color=0x33B5FF)
    for trial in list_of_sorted_trials:
        trial = trial_manager.get_Trial_by_name(trial[0])
        value_desc = f"Class: {trial.get_class()}\nSpec: {trial.spec}\n Days as Trial: {trial.get_days_as_a_trial()}\n [Logs]({trial.logs})"
        embed.add_field(name=trial.name, value=value_desc)
    await ctx.send(embed=embed)

@client.command()
async def get_status(ctx, trial: str):
    """
    Discord Command for sending the status of the trial (Name, Class, Spec, Logs, Days as trial) all in an Embed

    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :return: None
    """
    trial: Trial = trial_manager.get_Trial_by_name(trial)
    await ctx.send(embed=trial.get_embed())

@client.command()
async def promote_trial(ctx, trial: str):
    """
    Discord command for promoting a trial

    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :return: None
    """
    try:
        trial_manager.promote_trial(trial)
        await ctx.send(f"{trial} has been promoted")
    except KeyError:
        await ctx.send(f"{trial} is not valid...!list_trials for all valid trials")

@client.command()
async def remove_trial(ctx, trial: str):
    """
    Discorc command for removing a trial

    *Same as promote_trial()

    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :return: None
    """
    try:
        trial_manager.promote_trial(trial)
        await ctx.send(f"{trial} has been removed")
    except KeyError:
        await ctx.send(f"{trial} is not valid...!list_trials for all valid trials")

@client.command()
async def change_start_date(ctx, trial: str, new_date: str):
    # TODO add date verification/error handling
    """
    Updates a trial's join date

    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :param new_date: str '2021-11-30'
    :return: None
    """
    trial_manager.change_start_date(trial, new_date)
    await ctx.send(f"{trial}s start date has been updated to {new_date}")


@client.command()
async def make_inactive(ctx, trial: str):
    """
    Discord command for moving trial's status to 'inactive' or '0'

    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :return: None
    """
    trial_manager.make_inactive(trial, "0")
    await ctx.send(f"{trial} has been made inactive")

@client.command()
async def add_logs(ctx, trial: str, logs: str):
    """
    Discord command for adding/updating logs to a trial
    :param ctx: Discord Bot
    :param trial: str trial's name ('Notey')
    :param logs: str url for trial's Warcraft logs ('https://www.warcraftlogs.com/character/id/55296682')
    :return: None
    """
    trial_manager.add_logs(trial, logs)
    await ctx.send(f"{trial}s logs have been updated to {logs}")

# TODO fix this
@tasks.loop(hours=24)
async def check_for_promotions():
    print("starting checks")
    for trial in trial_manager.trial_list:
        if trial.check_for_promotion():
            pass


if __name__ == '__main__':
    client.run(getenv('TOKEN'))

