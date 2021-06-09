import sqlite3
from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db


class Test(TestTemplate):
    def test_delete_row(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [0, 'a'])
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [0, 'abc'])

        before = db.getTableData(self.BASE_DB_NAME_EXTENSION, "tablename")

        columnNames = ['abc', 'bca']
        rowToDelete = [0, 'a']
        db.deleteRow(self.BASE_DB_NAME_EXTENSION, "tablename", columnNames, rowToDelete)

        after = db.getTableData(self.BASE_DB_NAME_EXTENSION, "tablename")

        self.assertListEqual(before, [(0, 'a'), (0, 'abc')])
        self.assertListEqual(after, [(0, 'abc')])

    def test_delete_row_shouldNotDeleteRow_whenColumnNamesAreWrong(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [0, 'a'])
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [0, 'abc'])

        wrongColumnNames = ['abc', 'bba']
        rowToDelete = [0, 'a']
        self.assertRaises(sqlite3.OperationalError, db.deleteRow, self.BASE_DB_NAME_EXTENSION, "tablename", wrongColumnNames, rowToDelete)


