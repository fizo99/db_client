from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db


class Test(TestTemplate):
    def test_get_table_structure(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename", self.validTableStructure)

        for x,y in zip(db.getTableStructure(self.BASE_DB_NAME_EXTENSION, "tablename"), self.validTableStructure):
            self.assertEqual(x['column_name'], y['column_name'])
            self.assertEqual(x['data_type'], y['data_type'])
