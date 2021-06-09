import os
from unittest import TestCase

from db_client.scripts import db

class Test(TestCase):
    def test_get_database_names(self):
        db.createDB("abc")
        db.createDB("bca")

        self.assertListEqual(db.getDatabaseNames(), ["abc.db","bca.db"])

        os.remove(os.path.join(os.getcwd(), 'databases', "abc.db"))
        os.remove(os.path.join(os.getcwd(), 'databases', "bca.db"))
