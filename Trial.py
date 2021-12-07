from datetime import date
from class_verifier import class_icons
from discord import Embed

class Trial:
    def __init__(self, name, wow_class, spec, date_joined, logs=''):
        self.name: str = name
        self._class: str = wow_class
        self.spec: str = spec
        self.date_joined: date = date_joined
        self.logs = logs
        self.class_icon = class_icons[self.get_class()]

    def __repr__(self):
        return f"{self.name} ({self.spec}-{self._class})"

    def __str__(self):
        return f"{self.name} ({self.spec}-{self._class}) - {self.logs}"

    def get_trial(self):
        return tuple([self.name, self.spec, self._class, self.get_days_as_a_trial()])

    def get_days_as_a_trial(self):
        if self.date_joined != '0':
            year, month, day = self.date_joined.split('-')
            date_joined = date(int(year), int(month), int(day))
            return (date.today()-date_joined).days
        else:
            return 0

    def check_for_promotion(self) -> bool:
        if self.get_days_as_a_trial == 30:
            return True
        else:
            return False

    def get_class(self):
        return self._class

    def get_embed(self) -> Embed:
        embed_description = f"Class: {self.get_class()}\n Spec: {self.spec}\n Days as Trial: {self.get_days_as_a_trial()}\n"
        embed = Embed(title=self.name, description=embed_description, url=self.logs, color=0x33B5FF)
        embed.set_thumbnail(url=self.class_icon)
        return embed


def create_trial_from_tuple(trial_info: tuple) -> Trial:
    name, _class, spec, date_joined, logs, = trial_info
    return Trial(name, _class, spec, date_joined, logs)



