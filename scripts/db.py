import os,fnmatch
import sqlite3

def getDatabaseNames():
    result = []
    path = os.path.join(os.getcwd(), 'databases')
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, '*.db'):
                result.append(name)
    return result

def getTableNames(dbName):
    connection = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        rows = cur.fetchall()
        return {
            "type": "ok",
            "resultList": [x for x, in rows]
        }

    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if connection:
            connection.close()

def getTableStructure(dbName, tableName):
    connection = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(f'pragma table_info({tableName});')

        # lp., column_name, column_type,
        rows = cur.fetchall()
        result = [{
            "lp" : x,
            "column_name" : y,
            "data_type" : z
        } for x,y,z,_,_,_ in rows]

        return {
            "type" : "ok",
            "resultList" : result
        }

    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if connection:
            connection.close()

def createDB(dbName):
    dbName = dbName + ".db"
    dbs = getDatabaseNames()
    if dbName in dbs:
        return {
            "type": "error",
            "msg": "Database exists."
        }
    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        return {
            "type": "ok",
            "msg": "Database created."
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()