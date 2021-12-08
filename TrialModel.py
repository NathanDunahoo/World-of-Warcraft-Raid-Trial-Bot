from datetime import date
from ErrorHandling import class_icons
from discord import Embed

class Trial:
    def __init__(self, name, wow_class, spec, active,  date_joined, logs=None):
        self.name: str = name
        self._class: str = wow_class
        self.spec: str = spec
        self.logs: str = logs

        self.active: int = active

        self.date_joined: date = date_joined
        self.days_as_trial: int = 0
        self.get_days_as_a_trial()

        self.class_icon = class_icons[self.get_class()]

    def __repr__(self):
        return f"{self.name}, {self._class}, {self.spec}, {self.active}, {self.date_joined}, {self.logs}"

    def __str__(self):
        return f"Trial({self.name}, {self._class}, {self.spec}, {self.active}, {self.date_joined}, {self.logs})"

    def get_trial(self) -> tuple:
        """
        Gets the Trial in tuple format

        :return: tuple(str)
        """
        return tuple([self.name, self.spec, self._class, self.days_as_trial])

    def is_active(self) -> bool:
        return self.active not in [0, 'inactive']

    def get_days_as_a_trial(self):
        if self.is_active():
            year, month, day = str(self.date_joined).split('-')
            date_joined = date(int(year), int(month), int(day))
            self.days_as_trial = int((date.today()-date_joined).days)
        else:
            self.days_as_trial = -1

    def check_for_promotion(self) -> bool:
        """
        After 30 days a trial is eligible for a promotion

        :return: None
        """
        return self.days_as_trial > 30

    def get_class(self) -> str:
        """
        Getter for Trial's WoW Class since 'class' is a Python keyword and '_class' is protected
        :return: str Trial's WoW Class
        """
        return self._class

    def get_embed(self) -> Embed:
        """
        Creates an Embed object with trial information, and class_icon

        :return: Embed
        """
        embed_description = f"Class: {self.get_class()}\n Spec: {self.spec}\n Days as Trial: {self.days_as_trial}\n"
        embed = Embed(title=self.name, description=embed_description, url=self.logs, color=0x33B5FF)
        embed.set_thumbnail(url=self.class_icon)
        return embed


def create_trial_from_tuple(trial_info: tuple) -> Trial:
    """
    Constructor for Trial
    :param trial_info: (name, _class, spec, date_joined, logs)
    :return: Trial
    """
    name, _class, spec, date_joined, logs, active = trial_info
    return Trial(name=name, wow_class=_class, spec=spec, active=active, date_joined=date_joined, logs=logs)



