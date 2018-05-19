import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('../../resources/settings.ini')  # Read settings from settings.ini file
database_props = config['database_properties']
conn = pyodbc.connect('DRIVER={{{0}}};SERVER={1};DATABASE={2};UID={3};PWD={4}'
                      .format(database_props['driver'], database_props['server'], database_props['database'],
                              database_props['login_uid'], database_props['password']))  # Build connection string

cursor = conn.cursor()
