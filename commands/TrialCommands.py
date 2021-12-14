from discord import Embed
from discord.ext import commands, tasks
from sqlite3 import IntegrityError
from worldofwarcraft.WowData import WowData, ClassError, SpecError
from worldofwarcraft.TrialManager import TrialManager
from definitions import ROLE_ID

"""
TrialCommands contains all commands used to manage World of Warcraft raid trials

"""

tm = TrialManager()
wd = WowData()
class TrialCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add_trial(self, ctx, name, cls: wd.check_valid_class, spec, logs=''):
        """
        Discord command for adding a new trial
        Checks if class and spec are valid
        Adds a new trial to the DB

        :param ctx: commands.Context
        :param name: str trial's name ('Notey')
        :param cls: str trial's WoW class (Paladin, Warlock, Mage)
        :param spec:  str trial's WoW class specification (Prot, Affliction, Frost)
        :param logs: str url to trial's Warcraft logs (optional can be added later)
        :return: None
        """

        try:
            wd.check_valid_spec(cls, spec)
        except SpecError:
            await ctx.send(f"{spec} is not a valid spec for {cls}: {wd.get_specs_for_class(cls)}")
            return
        try:
            trial = tm.add_trial(name, cls, spec, logs=logs)
            await ctx.send(embed=trial.get_embed())
        except IntegrityError:
            await ctx.send(f"{name} is already a trial")

    @commands.command()
    async def list_trials(self, ctx):
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
            days_as_trial = 'Inactive' if trial.days_as_trial < 0 else trial.days_as_trial
            value_desc = f"Class: {trial.get_class()}\nSpec: {trial.spec}\n Days as Trial: {days_as_trial}\n [Logs]({trial.logs})"
            embed.add_field(name=trial.name, value=value_desc)
        await ctx.send(embed=embed)

    @commands.command()
    async def get_status(self, ctx, trial: tm.get_Trial_by_name):
        """
        Discord Command for sending the status of the trial (Name, Class, Spec, Logs, Days as trial) all in an Embed

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :return: None
        """

        await ctx.send(embed=trial.get_embed())

    @commands.command()
    async def promote_trial(self, ctx, trial: tm.get_Trial_by_name):
        """
        Discord command for promoting a trial

        :param ctx: Discord Bot
        :param trial: Trial from get_Trial_by_name
        :return: None
        """

        tm.promote_trial(trial)
        await ctx.send(f"{trial} has been promoted")

    @commands.command()
    async def remove_trial(self, ctx, trial: tm.get_Trial_by_name):
        """
        Discorc command for removing a trial

        *Same as promote_trial()

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :return: None
        """

        tm.promote_trial(trial)
        await ctx.send(f"{trial.name} has been removed")

    @commands.command()
    async def change_start_date(self, ctx, trial: tm.get_Trial_by_name, date: wd.check_valid_date):
        """
        Updates a trial's join date

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :param date: str '2021-11-30'
        :return: None
        """

        tm.change_start_date(trial, date)
        await ctx.send(f"{trial.name}'s start date has been updated to {date}")

    @commands.command()
    async def make_inactive(self, ctx, trial: tm.get_Trial_by_name):
        """
        Discord command for moving trial's status to 'inactive' or '0'

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :return: None
        """

        tm.change_status(trial, 0)
        await ctx.send(f"{trial.name} has been made inactive")

    @commands.command()
    async def make_active(self, ctx, trial: tm.get_Trial_by_name):
        """
        Discord command for moving trial's status to 'active' or 1

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :return: None
        """

        tm.change_status(trial, 1)
        tm.change_start_date(trial)
        await ctx.send(f"{trial.name} has been made active")

    @commands.command()
    async def add_logs(self, ctx, trial: tm.get_Trial_by_name, logs: str):
        """
        Discord command for adding/updating logs to a trial

        :param ctx: commands.Context
        :param trial: Trial from get_Trial_by_name
        :param logs: str url for trial's Warcraft logs ('https://www.warcraftlogs.com/character/id/55296682')
        :return: None
        """

        tm.add_logs(trial, logs)
        await ctx.send(f"{trial.name}'s logs have been updated to {logs}")

    @commands.command()
    async def promotion_task(self, ctx):
        await self.check_for_trial_promotions.start(ctx)

    @tasks.loop(hours=24)
    async def check_for_trial_promotions(self, ctx):
        print("Starting checks for promotions")
        await ctx.send(
            f"<@&{ROLE_ID}> Trials ready for promotion: {', '.join(tm.get_trials_ready_for_promotion())}")

def setup(client):
    client.add_cog(TrialCommands(client))
