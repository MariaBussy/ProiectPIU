# Iosif Vieru 1409A
# 30.10.2024

from peewee import MySQLDatabase, SqliteDatabase
from sys import exit

db_credentials = {}

with open("database/database_config", "r") as config_file:
    for line in config_file:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=")
            db_credentials[key] = value

try:
    db = SqliteDatabase('database.db')
except Exception as e:
    print("[Database] Error:", e)
    exit(1)