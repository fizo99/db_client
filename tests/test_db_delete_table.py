from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db


class Test(TestTemplate):
    def test_delete_table(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        self.assertListEqual(db.getTableNames(self.BASE_DB_NAME_EXTENSION), ['tablename'])
        db.deleteTable(self.BASE_DB_NAME_EXTENSION, "tablename")
        self.assertListEqual(db.getTableNames(self.BASE_DB_NAME_EXTENSION), [])
