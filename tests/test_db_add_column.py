import sqlite3
from unittest import TestCase

from db_client.scripts import db
from db_client.scripts.exceptions.InvalidTypeException import InvalidTypeException
from db_client.tests.TestTemplate import TestTemplate


class Test(TestTemplate):
    def test_add_column(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        before = db.getTableStructure(self.BASE_DB_NAME_EXTENSION, "tablename")

        db.addColumn(self.BASE_DB_NAME_EXTENSION,"tablename", "newColumn", "int")
        after = db.getTableStructure(self.BASE_DB_NAME_EXTENSION, "tablename")

        self.assertFalse(before == after)

    def test_add_column_shouldNotAddColumn_whenDataTypeInvalid(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        self.assertRaises(InvalidTypeException, db.addColumn, self.BASE_DB_NAME_EXTENSION,"tablename", "newColumn", "abc")

