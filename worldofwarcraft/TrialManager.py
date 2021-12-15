import os
import sqlite3
from datetime import date
from definitions import ROOT_DIR, DB_NAME, TRIAL_TABLE
from worldofwarcraft.WowData import TrialError
from worldofwarcraft.TrialModel import Trial, create_trial_from_tuple

"""
Backend for all TrialCommands 
Interacts with TrailModel and SQLite to make updates to the db
"""

db = sqlite3.connect(os.path.join(ROOT_DIR, DB_NAME))
cur = db.cursor()

class TrialManager:

    def __init__(self):
        self.trial_list: list[Trial] = []
        self.table_name = TRIAL_TABLE  # Equates to Discord server ID 'g<id>'
        self.get_all_trials()

    """Helper Functions"""
    def get_all_trials(self):
        """
        DB query to fetch all trials from the table
        Stores results in self.trial_list
        :return:
        """

        cur.execute(f"SELECT * from {self.table_name}")
        self.trial_list: list[Trial] = [create_trial_from_tuple(trial) for trial in cur.fetchall()]

    def get_all_trials_as_str(self) -> str:
        """
        Unused but may be helpful for something

        :return: str of all trial's in trial_list
        """
        trials = [str(trial) for trial in self.trial_list]
        return '\n'.join(trials)

    def get_all_trials_as_tuple(self) -> list[tuple]:
        """
        Gets all trials as a tuple to be used in !list_trials()
        tuple format: (trial.name, trial.spec, trial._class, trial.days_as_trial)

        :return: list[tuple] of every trial in trial_list
        """
        return [trial.get_trial() for trial in self.trial_list]

    def get_name_of_all_trials(self) -> list[str]:
        """
        Gets all trial names from trial_list

        :return: list[str] of every trial in trial_list
        """
        return [trial.name for trial in self.trial_list]

    def get_Trial_by_name(self, name: str) -> Trial:
        """
        :param name: str trial's name ('Notey')
        :return: Trial from trial's name
        """
        if name not in self.get_name_of_all_trials():
            raise TrialError
        for trial in self.trial_list:
            if trial.name == name:
                return trial

    def get_trials_ready_for_promotion(self) -> list[str]:
        return [trial.name for trial in self.trial_list if trial.check_for_promotion()]

    def update_db_and_list(self):
        """
        Helper function to be called after every db action

        Commits the changes to the db
        Calls get_all_trials to update trial_list with changes from the db

        :return: None
        """
        db.commit()
        self.get_all_trials()

    """ DB Actions """
    def add_trial(self, name: str, cls: str, spec: str, logs, date_joined=date.today(), active=1):
        """
        Adds a trial to the db
        Creates a Trial() and adds it to the trial_list

        :param name: str trial's name ('Notey')
        :param cls: str trial's WoW class (Paladin, Warlock, Mage)
        :param spec:  str trial's WoW class specification (Prot, Afflication, Frost)
        :param logs: str url to trial's Warcraft logs (optional can be added later)
        :param date_joined: date object - default date.today()
        :param active: 0 or 1
        :return: Trial
        """
        db.execute(f"INSERT INTO {self.table_name} "
                   f"VALUES (?,?,?,?,?,?)",
                   (name, cls, spec, date_joined, logs, active))
        db.commit()

        trial: Trial = Trial(name, cls, spec, active=active, date_joined=date_joined, logs=logs)
        self.trial_list.append(trial)
        return trial

    def promote_trial(self, trial: Trial):
        """
        DB action for 'promoting' a trial or simply deleting their entry from the db

        :param trial: TrialModel
        :return: None
        """

        db.execute(f"""DELETE FROM {self.table_name}
                    WHERE name=:name
                    """, {'name': trial.name})
        self.update_db_and_list()

    def change_start_date(self, trial: Trial, new_date=date.today()):
        """
        DB action for changing the start_date or 'date_joined' for a trial

        :param trial: TrialModel
        :param new_date: str date format: '2021-11-30'
        :return: None
        """

        db.execute(f"""UPDATE {self.table_name}
                    SET date=:date
                    WHERE name=:name 
                    """,  {'date': str(new_date), 'name': trial.name})
        self.update_db_and_list()

    def add_logs(self, trial: Trial, logs: str):
        """
        DB action for adding/updating logs for a trial
        For Discord command !add_logs

        :param trial: TrialModel
        :param logs: str url to trial's Warcraft logs ('https://www.warcraftlogs.com/character/id/55296682')
        :return: None
        """

        db.execute(f"""UPDATE {self.table_name}
                    SET logs=:logs
                    WHERE name=:name
                     """, {'logs': logs, 'name': trial.name})

    def change_status(self, trial: Trial, status: int):
        """
        DB action for changing a trial's status"
        For Discord command !make_inactive

        :param trial: TrialModel
        :param status: '0' for inactive - '1' for active
        :return: None
        """
        db.execute(f"""UPDATE {self.table_name}
                        SET active=:status
                        WHERE name=:name
                    """, {'status': status, 'name': trial.name})
        self.update_db_and_list()


if __name__ == "__main__":
    # For testing
    tm = TrialManager()
    print(tm.trial_list)
    for t in tm.trial_list:
        print(t.class_icon)
    #tm.check_for_promotions()
    pass


