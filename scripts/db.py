import os
import fnmatch
import sqlite3
import numbers

import random, string

import re

from db_client.scripts.exceptions.InvalidTypeException import InvalidTypeException
from db_client.scripts.exceptions.DatabaseExistsException import DatabaseExistsException
from db_client.scripts.exceptions.DatabaseNotExistsException import DatabaseNotExistsException
from db_client.scripts.exceptions.WrongNameException import WrongNameException

REGEXP_ALPHANUMERIC = "^[a-zA-Z0-9_]*$"
QUERY_GET_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table';"
VALID_TYPES = ['varchar', 'int', 'float']


def getDatabaseNames():
    result = []
    path = os.path.join(os.getcwd(), 'databases')
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, '*.db'):
                result.append(name)
    return result


def query(dbName: str, queryString: str):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(queryString)

        conn.commit()
    except (sqlite3.OperationalError, sqlite3.Error) as e:
        raise e
    finally:
        if conn:
            conn.close()


def getTableNames(dbName: str):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(QUERY_GET_TABLE_NAMES)

        rows = cur.fetchall()
        return [x for x, in rows]
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def getTableStructure(dbName: str, tableName: str):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(f'pragma table_info({tableName});')

        rows = cur.fetchall()
        return [{
            "lp": x,
            "column_name": y,
            "data_type": z
        } for x, y, z, _, _, _ in rows]
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


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
        conn = sqlite3.connect(path)
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def createTable(dbName, tableName, tableContent):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    tableContent = list(tableContent)
    statement = f'create table {tableName}('
    for column in tableContent:
        if column['data_type'] not in VALID_TYPES:
            raise InvalidTypeException(column['data_type'])
        statement += column['column_name'] + " " + column['data_type'] + ","
    statement = "".join(list(statement)[:-1]) + ");"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
    except (sqlite3.Error, sqlite3.OperationalError) as e:
        raise e
    finally:
        if conn:
            conn.close()


def deleteColumn(dbName, tableName, columnName):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    # rename old table
    tempName = tableName + "_temp"

    tableStructure = None
    try:
        tableStructure = getTableStructure(dbName, tableName)
        renameTable(dbName, tableName, tempName)
    except Exception as e:
        raise e

    # create new table
    for x in tableStructure:
        if x['column_name'] == columnName:
            tableStructure.remove(x)

    if len(tableStructure) == 0:
        renameTable(dbName, tempName, tableName)
        raise Exception("Table can`t have 0 columns")

    try:
        createTable(dbName, tableName, tableStructure)
    except Exception as e:
        renameTable(dbName, tempName, tableName)
        raise e

    statement = f"insert into {tableName}("
    for x in tableStructure:
        statement += x["column_name"] + ","
    statement = "".join(list(statement)[:-1]) + ") SELECT "
    for x in tableStructure:
        statement += x["column_name"] + ","
    statement = "".join(list(statement)[:-1]) + f" FROM {tempName};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
        conn.close()
        deleteTable(dbName, tempName)
    except (sqlite3.Error, sqlite3.OperationalError) as e:
        deleteTable(dbName, tableName)
        renameTable(dbName, tempName, tableName)
        raise e
    finally:
        if conn:
            conn.close()


def deleteTable(dbName, tableName):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    statement = f"Drop table {tableName};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def getTableData(dbName, tableName):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    statement = f"select * from {tableName};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)

        rows = cur.fetchall()

        return rows
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def addColumn(dbName, tableName, columnName, dataType):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    if dataType not in ['int', 'varchar', 'float']:
        raise InvalidTypeException

    statement = f"alter table {tableName} add column {columnName} {dataType};"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def deleteRow(dbName, tableName, columnNames, values):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    statement = f"delete from {tableName} where "
    for columnName, value in zip(columnNames, values):
        value = " is null" if value is None else f"{value}" if isinstance(value, numbers.Number) else f"'{value}'"
        statement += f"{columnName}={value} and "
    statement = "".join(list(statement)[:-5]) + ";"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def insertRow(dbName, tableName, values):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    statement = f"insert into {tableName} values("

    for value in values:
        value = "null" if value is None else f"{value}" if isinstance(value, numbers.Number) else f"'{value}'"
        statement += f"{value},"
    statement = "".join(list(statement)[:-1]) + ");"

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()


def renameTable(dbName, tableName, newTableName):
    if dbName not in getDatabaseNames():
        raise DatabaseNotExistsException(dbName)

    statement = f'alter table \'{tableName}\' rename to \'{newTableName}\';'

    conn = None
    try:
        path = os.path.join(os.getcwd(), 'databases', dbName)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute(statement)
    except sqlite3.Error as e:
        raise e
    finally:
        if conn:
            conn.close()
