import discord
import os
from discord.ext import commands, tasks
import class_verifier
import trial_db
from datetime import date

todays_date = date.today()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await ctx.bot.logout()

@client.command()
async def add_trial(ctx, name, _class, spec, logs=''):
    try:
        class_verifier.check_valid_class_spec(_class, spec)
    except class_verifier.ClassError:
        await ctx.send(f"{_class} is not a valid class {class_verifier.valid_classes}")
        return
    except class_verifier.SpecError:
        await ctx.send(f"{spec} is not a valid spec for {_class} {class_verifier.valid_specs[_class]}")
        return

    trial_db.add_trial(name, _class, spec, logs)
    trial = trial_db.get_Trial_by_name(name)

    await ctx.send(embed=trial.get_embed())

@client.command()
async def list_trials(ctx):
    embed = discord.Embed(title="Current Trials", color=0x33B5FF)
    list_of_sorted_trials = trial_db.get_all_trials_as_tuple()
    list_of_sorted_trials.sort(key=lambda x: x[3], reverse=True)
    for trial in list_of_sorted_trials:
        trial = trial_db.get_Trial_by_name(trial[0])
        value_desc = f"Class: {trial.get_class()}\nSpec: {trial.spec}\n Days as Trial: {trial.get_days_as_a_trial()}\n [Logs]({trial.logs})"
        embed.add_field(name=trial.name, value=value_desc)
    await ctx.send(embed=embed)

@client.command()
async def get_status(ctx, trial):
    trial = trial_db.get_Trial_by_name(trial)
    await ctx.send(embed=trial.get_embed())

@client.command()
async def promote_trial(ctx, trial):
    try:
        trial_db.promote_trial(trial)
        await ctx.send(f"{trial} has been promoted")
    except KeyError:
        await ctx.send(f"{trial} is not valid...!list_trials for all valid trials")

@client.command()
async def remove_trial(ctx, trial):
    try:
        trial_db.promote_trial(trial)
        await ctx.send(f"{trial} has been removed")
    except KeyError:
        await ctx.send(f"{trial} is not valid...!list_trials for all valid trials")

@client.command()
async def change_start_date(ctx, trial, new_date):
    trial_db.change_start_date(trial, new_date)
    await ctx.send(f"{trial}s start date has been updated to {new_date}")


@client.command()
async def make_inactive(ctx, trial):
    trial_db.make_inactive(trial, "0")
    await ctx.send(f"{trial} has been made inactive")

@client.command()
async def add_logs(ctx, trial, logs):
    trial_db.add_logs(trial, logs)
    await ctx.send(f"{trial}s logs have been updated to {logs}")

@client.command()
async def start_check_for_promotions(ctx, enabled='start', interval=24):
    if enabled.lower == 'stop':
        check_for_promotions.stop()
    elif enabled.lower() == 'start':
        check_for_promotions.change_interval(hours=int(interval))
        check_for_promotions.start(ctx)


@tasks.loop(hours=24)
async def check_for_promotions(ctx):
    print("starting checks")
    for trial in trial_db.get_all_trials():
        if trial.check_for_promotion():
            ctx.send(f"{trial} is ready for a promotion")


client.run(os.getenv('TOKEN'))
