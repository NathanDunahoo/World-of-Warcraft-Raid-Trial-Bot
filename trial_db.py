import sqlite3
from datetime import date
from Trial import Trial, create_trial_from_tuple

con = sqlite3.connect('inferno.db')
cur = con.cursor()


def create_table():
    cur.execute("""CREATE TABLE trials
    (name text, class text, spec text, date text, notes text)""")
    con.commit()

def add_trial(name: str, _class: str, spec: str, notes: str):
    cur.execute(f"INSERT INTO trials VALUES (?,?,?,?,?)", (name, _class, spec, date.today(), notes))
    con.commit()

def get_all_trials() -> list[Trial]:
    cur.execute("SELECT * from trials")
    return [create_trial_from_tuple(trial) for trial in cur.fetchall()]

def get_all_trials_as_str() -> str:
    trials = [str(trial) for trial in get_all_trials()]
    return '\n'.join(trials)

def get_all_trials_as_tuple() -> list[tuple]:
    return [trial.get_trial() for trial in get_all_trials()]

def get_name_of_all_trials() -> list[str]:
    return [trial.name for trial in get_all_trials()]

def get_Trial_by_name(name: str) -> Trial:
    for trial in get_all_trials():
        if trial.name == name:
            return trial

def promote_trial(trial: str):
    print(f"{trial} has been deleted from table")
    cur.execute("""DELETE FROM trials
            WHERE name=:name
    """, {'name': trial})
    con.commit()

def change_start_date(trial: str, new_date: str):
    cur.execute("""UPDATE trials
            SET date=:date
            WHERE name=:name
    """, {'date': new_date, 'name': trial})
    con.commit()

def add_logs(trial, logs):
    cur.execute("""UPDATE trials
                SET logs=:logs
                WHERE name=:name
        """, {'logs': logs, 'name': trial})
    con.commit()

def make_inactive(trial, status):
    cur.execute("""UPDATE trials
                    SET date=:status
                    WHERE name=:name
            """, {'status': status, 'name': trial})
    con.commit()

def is_valid_trial(trial: str) -> bool:
    return trial in get_name_of_all_trials()

if __name__ == "__main__":
    #create_table()
    #con.close()
    #rint(get_all_trials())
    #print(get_all_trials_as_str())
    #get_days_as_a_trial('Notey')

    test = get_all_trials_as_tuple()
    print(test)
    test.sort(key=lambda x: x[3], reverse=True)
    print(test)
    pass


