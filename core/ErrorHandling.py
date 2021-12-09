from discord.ext import commands
from re import search

valid_classes = ["Paladin", "Monk", "Druid", "Priest", 'Deathknight', 'Demonhunter', 'Rogue', 'Mage', 'Warlock', 'Warrior', 'Shaman', 'Hunter']
valid_specs = {
    'Paladin': ['Prot', 'Ret', 'Holy'],
    'Monk': ['Brew', 'Mistweaver', 'Windwalker'],
    'Druid': ['Boomkin', 'Bear', 'Resto'],
    'Priest': ['Shadow', 'Disc', 'Holy'],
    'Deathknight': ['Unholy', 'Blood', 'Frost'],
    'Demonhunter': ['Havoc', 'Vengeance'],
    'Rogue': ['Sub', 'Assass', 'Outlaw'],
    'Mage': ['Fire', 'Arcane', 'Frost'],
    'Warlock': ['Affliction', 'Demo', 'Destruction'],
    'Warrior': ['Arms', 'Fury', 'Prot'],
    'Shaman': ['Resto', 'Ele', 'Enhance'],
    'Hunter': ['Marksman', 'Bm', 'Survival'],
    }

class_icons = {
    "Paladin": r'https://static.wikia.nocookie.net/wowpedia/images/f/fa/Charactercreate-class_paladin.png/revision/latest/scale-to-width-down/120?cb=20200517190005',
    "Monk": r'https://static.wikia.nocookie.net/wowpedia/images/4/40/Charactercreate-class_monk.png/revision/latest/scale-to-width-down/120?cb=20200517190000',
    "Druid": r'https://static.wikia.nocookie.net/wowpedia/images/6/66/Charactercreate-class_druid.png/revision/latest/scale-to-width-down/120?cb=20200517185946',
    "Priest": r'https://static.wikia.nocookie.net/wowpedia/images/7/7e/Charactercreate-class_priest.png/revision/latest/scale-to-width-down/120?cb=20200517190009',
    'Deathknight': r'https://static.wikia.nocookie.net/wowpedia/images/d/de/Charactercreate-class_deathknight.png/revision/latest/scale-to-width-down/120?cb=20200517185937',
    'Demonhunter': r'https://static.wikia.nocookie.net/wowpedia/images/9/97/Charactercreate-class_demonhunter.png/revision/latest/scale-to-width-down/120?cb=20200517185942',
    'Rogue': r'https://static.wikia.nocookie.net/wowpedia/images/6/66/Charactercreate-class_rogue.png/revision/latest/scale-to-width-down/120?cb=20200517190014',
    'Mage': r'https://static.wikia.nocookie.net/wowpedia/images/c/cc/Charactercreate-class_mage.png/revision/latest/scale-to-width-down/120?cb=20200517185956',
    'Warlock': r'https://static.wikia.nocookie.net/wowpedia/images/4/4f/Charactercreate-class_warlock.png/revision/latest/scale-to-width-down/120?cb=20200517190024',
    'Warrior': r'https://static.wikia.nocookie.net/wowpedia/images/0/0f/Charactercreate-class_warrior.png/revision/latest/scale-to-width-down/120?cb=20200517190030',
    'Shaman': r'https://static.wikia.nocookie.net/wowpedia/images/1/17/Charactercreate-class_shaman.png/revision/latest/scale-to-width-down/120?cb=20200517190019',
    'Hunter': r'https://static.wikia.nocookie.net/wowpedia/images/e/e8/Charactercreate-class_hunter.png/revision/latest/scale-to-width-down/120?cb=20200517185951'
    }

class ClassError(Exception):
    pass

class SpecError(Exception):
    pass

class TrialError(Exception):
    pass

class BadDate(Exception):
    pass

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

def check_valid_class_spec(_class: str, spec: str):
    if _class not in valid_classes:
        raise ClassError
    else:
        if spec not in valid_specs[_class]:
            raise SpecError

def check_valid_date(date: str):
    check = search(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', date)
    if bool(check):
        return date
    else:
        raise BadDate
