from os import path, getenv

"""
Used to define constants and environment variables
"""

ROOT_DIR = path.dirname(path.abspath(__file__))
ROLE_ID = getenv("ROLE_ID")  # Discord role ID for mentioning
TOKEN = getenv("TOKEN")  # Discord bot token for auth
DB_NAME = getenv("DB_NAME")  # Name of DB ('<name>.db')
TRIAL_TABLE = getenv("TRIAL_TABLE")  # Name of table ('trials')
WOW_DATA = 'wowdata.json'
