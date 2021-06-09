import os
import sqlite3
from unittest import TestCase

from db_client.scripts import db
from db_client.scripts.exceptions.DbOperationException import DbOperationException
from db_client.scripts.exceptions.InvalidTypeException import InvalidTypeException
from db_client.tests.TestTemplate import TestTemplate


class Test(TestTemplate):

    def test_create_table_shouldCreateTable(self):
        db.createTable("abc.db","tablename",self.validTableStructure)
        self.assertListEqual(db.getTableNames("abc.db"), ["tablename"])

    def test_create_table_shouldNotCreateTable_whenTableExists(self):
        db.createTable("abc.db", "tablename", self.validTableStructure)
        self.assertRaises(sqlite3.OperationalError, db.createTable, "abc.db","tablename",self.validTableStructure)

    def test_create_table_shouldNotCreateTable_whenTypeNotValid(self):
        self.assertRaises(InvalidTypeException, db.createTable, "abc.db","tablename",self.invalidTableStructure)
