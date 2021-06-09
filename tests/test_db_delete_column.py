from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db

class Test(TestTemplate):
    def test_delete_column(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        before = db.getTableStructure(self.BASE_DB_NAME_EXTENSION, "tablename")

        db.deleteColumn(self.BASE_DB_NAME_EXTENSION, "tablename", "abc")
        after = db.getTableStructure(self.BASE_DB_NAME_EXTENSION, "tablename")

        self.assertTrue(len(before) == 2 and len(after) == 1)
