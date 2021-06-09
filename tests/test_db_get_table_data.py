from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db


class Test(TestTemplate):
    def test_get_table_data(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [0, 'a'])
        db.insertRow(self.BASE_DB_NAME_EXTENSION, "tablename", [1, 'abc'])

        self.assertListEqual(db.getTableData(self.BASE_DB_NAME_EXTENSION, "tablename"), [(0, 'a'), (1,'abc')])
