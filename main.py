import eel
import sqlite3

import os, fnmatch


@eel.expose
def custom(x):
    try:
        conn = sqlite3.connect('example.db')
        print(sqlite3.version)
    except Exception as e:
        print(e)

@eel.expose
def getDatabases():
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(name)
        return result

    return find('*.db', 'databases/')

@eel.expose
def createDatabase(dbBame):
    databases = getDatabases()
    dbBame = dbBame + ".db"
    if dbBame in databases:
        return {
            "type": "error",
            "msg": "Database already exists."
        }
    else:
        connection = None
        try:
            connection = sqlite3.connect('databases/' + dbBame)
        except sqlite3.Error as e:
            return {
                "type": "error",
                "msg": "An error occurred: " + e.args[0]
            }
        finally:
            if connection:
                connection.close()
                return {
                    "type": "ok",
                    "msg": "Success!"
                }


if __name__ == "__main__":
    eel.init('src/static_web_folder')
    eel.start('html/databases.html', mode="chrome-app")
