import sqlite3
from datetime import date
from ErrorHandling import TrialError
from TrialModel import Trial, create_trial_from_tuple

DB_NAME = 'inferno.db'
TRIAL_TABLE = 'trials'

class TrialManager:
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    def __init__(self):
        self.create_table()

        self.trial_list: list[Trial] = []
        self.get_all_trials()

    def create_table(self):
        """
        Creates a table in DB_NAME as TRIAL_TABLE if it doesn't exist
        :return: None
        """
        self.cur.execute(f"""CREATE TABLE if not exists {TRIAL_TABLE}
        (name text, class text, spec text, date text, notes text)""")
        self.con.commit()

    def add_trial(self, name: str, _class: str, spec: str, logs, active):
        """
        Adds a trial to the db
        Creates a Trial() and adds it to the trial_list

        :param name: str trial's name ('Notey')
        :param _class: str trial's WoW class (paladin, warlock, mage)
        :param spec:  str trial's WoW class specification (prot, afflication, frost)
        :param logs: str url to trial's Warcraft logs (optional can be added later)
        :return: Trial
        """
        self.cur.execute(f"INSERT INTO {TRIAL_TABLE} VALUES (?,?,?,?,?,?)", (name, _class, spec, date.today(), logs, active))
        self.con.commit()
        trial: Trial = Trial(name, _class, spec, active, logs=logs)
        self.trial_list.append(trial)
        return trial

    def get_all_trials(self):
        """
        DB query to fetch all trials from the table
        Stores results in self.trial_list
        :return:
        """
        self.cur.execute(f"SELECT * from {TRIAL_TABLE}")
        self.trial_list: list[Trial] = [create_trial_from_tuple(trial) for trial in self.cur.fetchall()]

 # ___________________________________________________________________________________________________________________ #

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

    def is_valid_trial(self, trial: str) -> bool:
        """
        Checks if a trial is valid by seeing if their name is already in the trial_list
        Used get_name_of_all_trials() to get a list of all trial's names

        :param trial: trial's name ('Notey')
        :return: bool
        """
        return trial in self.get_name_of_all_trials()

    def promote_trial(self, trial: Trial):
        """
        DB action for 'promoting' a trial or simply deleting their entry from the db

        :param trial: TrialModel
        :return: None
        """
        print(f"{trial.name} has been deleted from table")
        self.cur.execute(f"""DELETE FROM {TRIAL_TABLE}
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
        self.cur.execute(f"""UPDATE {TRIAL_TABLE}
                SET date=:date
                WHERE name=:name
        """, {'date': str(new_date), 'name': trial.name})
        self.update_db_and_list()

    def add_logs(self, trial: Trial, logs: str):
        """
        DB action for adding/updating logs for a trial
        For Discord command !add_logs

        :param trial: TrialModel
        :param logs: str url to trial's Warcraft logs ('https://www.warcraftlogs.com/character/id/55296682')
        :return: None
        """
        self.cur.execute(f"""UPDATE {TRIAL_TABLE}
                    SET logs=:logs
                    WHERE name=:name
            """, {'logs': logs, 'name': trial.name})
        self.update_db_and_list()

    def change_status(self, trial: Trial, status: int):
        """
        DB action for changing a trial's status"
        For Discord command !make_inactive

        :param trial: TrialModel
        :param status: '0' for inactive - '1' for active
        :return: None
        """
        self.cur.execute(f"""UPDATE {TRIAL_TABLE}
                        SET active=:status
                        WHERE name=:name
                """, {'status': status, 'name': trial.name})
        self.update_db_and_list()

    def update_db_and_list(self):
        """
        Helper function to be called after every db action

        Commits the changes to the db
        Calls get_all_trials to update trial_list with changes from the db

        :return: None
        """
        self.con.commit()
        self.get_all_trials()


if __name__ == "__main__":
    tm = TrialManager()
    # create_table()
    # rint(get_all_trials())
    # print(get_all_trials_as_str())
    # get_days_as_a_trial('Notey')
    for trial in tm.trial_list:
        print(trial.__dict__)
        #rint(trial.date_joined)
    pass


