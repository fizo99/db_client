from unittest import TestCase

from db_client.scripts import db
import os

from db_client.tests.TestTemplate import TestTemplate


class Test(TestTemplate):
    def test_rename_table(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)

        self.assertListEqual(db.getTableNames(self.BASE_DB_NAME_EXTENSION), ['tablename'])

        db.renameTable(self.BASE_DB_NAME_EXTENSION, "tablename", "newtablename")
        self.assertListEqual(db.getTableNames(self.BASE_DB_NAME_EXTENSION), ['newtablename'])
