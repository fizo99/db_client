import os, fnmatch
import sqlite3
import json
import numbers

import re

from db_client.scripts.exceptions.DatabaseExistsException import DatabaseExistsException
from db_client.scripts.exceptions.DbOperationException import DbOperationException
from db_client.scripts.exceptions.WrongNameException import WrongNameException

REGEXP_ALPHANUMERIC = "^[a-zA-Z0-9_]*$"


def getDatabaseNames():
    result = []
    path = os.path.join(os.getcwd(), 'databases')
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, '*.db'):
                result.append(name)
    return result


def query(dbName, queryString):
    connection = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(queryString)

        connection.commit()
        return {
            "type": "ok",
            "msg": "Query executed successfully"
        }

    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if connection:
            connection.close()


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
            "lp": x,
            "column_name": y,
            "data_type": z
        } for x, y, z, _, _, _ in rows]

        return {
            "type": "ok",
            "resultList": result
        }

    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if connection:
            connection.close()


def createDB(dbName: str):
    if re.match(REGEXP_ALPHANUMERIC, dbName) is None:
        raise WrongNameException("Wrong db name: " + dbName)

    dbName = dbName + ".db"

    dbs = getDatabaseNames()
    if dbName in dbs:
        raise DatabaseExistsException("Database exists: " + dbName)

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
    except sqlite3.Error as e:
        raise DbOperationException("Db error:" + e.args[0])
    finally:
        if conn:
            conn.close()


def createTable(dbName, tableName, tableContent):
    tableContent = list(tableContent)
    statement = f'create table {tableName}('
    for column in tableContent:
        statement += column['column_name'] + " " + column['data_type'] + ","
    statement = "".join(list(statement)[:-1]) + ");"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        return {
            "type": "ok",
            "msg": "Table created"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def deleteColumn(dbName, tableName, columnName):
    # rename old table
    tableStructure = getTableStructure(dbName, tableName)['resultList']
    renameTable(dbName, tableName, tableName + "_old")

    # create new table
    for x in tableStructure:
        if x['column_name'] == columnName:
            tableStructure.remove(x)

    createTable(dbName, tableName, tableStructure)

    statement = f"insert into {tableName}("
    for x in tableStructure:
        statement += x["column_name"] + ","
    statement = "".join(list(statement)[:-1]) + ") SELECT "
    for x in tableStructure:
        statement += x["column_name"] + ","
    statement = "".join(list(statement)[:-1]) + f" FROM {tableName}_old;"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)

        return {
            "type": "ok",
            "msg": "Column deleted"
        }
    except sqlite3.Error as e:
        deleteTable(dbName, tableName)
        renameTable(dbName, tableName + "_old", tableName)
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def deleteTable(dbName, tableName):
    statement = f"Drop table {tableName};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        return {
            "type": "ok",
            "msg": "Table deleted"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def getTableData(dbName, tableName):
    statement = f"select * from {tableName};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)

        rows = cur.fetchall()

        return {
            "type": "ok",
            "resultList": rows
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def addColumn(dbName, tableName, columnName, dataType):
    statement = f"alter table {tableName} add column {columnName} {dataType};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        return {
            "type": "ok",
            "msg": "Column added"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def deleteRow(dbName, tableName, columnNames, values):
    statement = f"delete from {tableName} where "
    for columnName, value in zip(columnNames, values):
        value = " is null" if value == None else f"={value}"
        statement += f"{columnName}{value} and "
    statement = "".join(list(statement)[:-5]) + ";"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        connection.commit()
        return {
            "type": "ok",
            "msg": "Row deleted"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def insertRow(dbName, tableName, values):
    statement = f"insert into {tableName} values("

    for value in values:
        value = "null" if value == None else f"{value}" if isinstance(value, numbers.Number) else f"'{value}'"
        statement += f"{value},"
    statement = "".join(list(statement)[:-1]) + ");"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        connection.commit()
        return {
            "type": "ok",
            "msg": "Row inserted"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()


def renameTable(dbName, tableName, newTableName):
    statement = f'alter table {tableName} rename to {newTableName};'
    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        connection = sqlite3.connect(path)
        cur = connection.cursor()
        cur.execute(statement)
        return {
            "type": "ok",
            "msg": "Table renamed"
        }
    except sqlite3.Error as e:
        return {
            "type": "error",
            "msg": "An error occurred: " + e.args[0]
        }
    finally:
        if conn:
            conn.close()
