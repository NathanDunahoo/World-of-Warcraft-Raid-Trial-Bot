import sqlite3
from datetime import date
from TrialModel import Trial, create_trial_from_tuple


class TrialManager:
    def __init__(self):
        self.con = sqlite3.connect('inferno.db')
        self.cur = self.con.cursor()
        self.create_table()

        self.trial_list: list[Trial] = []
        self.get_all_trials()

    def create_table(self):
        self.cur.execute("""CREATE TABLE if not exists trials
        (name text, class text, spec text, date text, notes text)""")
        self.con.commit()

    def add_trial(self, name: str, _class: str, spec: str, logs):
        self.cur.execute(f"INSERT INTO trials VALUES (?,?,?,?,?)", (name, _class, spec, date.today(), logs))
        self.con.commit()
        trial: Trial = Trial(name, _class, spec, logs=logs)
        self.trial_list.append(trial)
        return trial


    def get_all_trials(self):
        self.cur.execute("SELECT * from trials")
        self.trial_list: list[Trial] = [create_trial_from_tuple(trial) for trial in self.cur.fetchall()]


 # ___________________________________________________________________________________________________________________ #

    def get_all_trials_as_str(self) -> str:
        trials = [str(trial) for trial in self.trial_list]
        return '\n'.join(trials)

    def get_all_trials_as_tuple(self) -> list[tuple]:
        return [trial.get_trial() for trial in self.trial_list]

    def get_name_of_all_trials(self) -> list[str]:
        return [trial.name for trial in self.trial_list]

    def get_Trial_by_name(self, name: str) -> Trial:
        for trial in self.trial_list:
            if trial.name == name:
                return trial

    def is_valid_trial(self, trial: str) -> bool:
        return trial in self.get_name_of_all_trials()

    def promote_trial(self, trial: str):
        print(f"{trial} has been deleted from table")
        self.cur.execute("""DELETE FROM trials
                WHERE name=:name
        """, {'name': trial})
        self.update_db_and_list()

    def change_start_date(self, trial: str, new_date: str):
        self.cur.execute("""UPDATE trials
                SET date=:date
                WHERE name=:name
        """, {'date': new_date, 'name': trial})
        self.update_db_and_list()

    def add_logs(self, trial, logs):
        self.cur.execute("""UPDATE trials
                    SET logs=:logs
                    WHERE name=:name
            """, {'logs': logs, 'name': trial})
        self.update_db_and_list()

    def make_inactive(self, trial, status):
        self.cur.execute("""UPDATE trials
                        SET date=:status
                        WHERE name=:name
                """, {'status': status, 'name': trial})
        self.update_db_and_list()

    def update_db_and_list(self):
        self.con.commit()
        self.get_all_trials()


if __name__ == "__main__":
    #create_table()
    #con.close()
    #rint(get_all_trials())
    #print(get_all_trials_as_str())
    #get_days_as_a_trial('Notey')

    test = self.get_all_trials_as_tuple()
    print(test)
    test.sort(key=lambda x: x[3], reverse=True)
    print(test)
    pass


