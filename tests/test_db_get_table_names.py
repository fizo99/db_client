from unittest import TestCase

from db_client.tests.TestTemplate import TestTemplate
from db_client.scripts import db

class Test(TestTemplate):
    def test_get_table_names(self):
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename1", self.validTableStructure)
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename2", self.validTableStructure)
        db.createTable(self.BASE_DB_NAME_EXTENSION, "tablename3", self.validTableStructure)

        self.assertListEqual(['tablename1','tablename2','tablename3'], db.getTableNames(self.BASE_DB_NAME_EXTENSION))


