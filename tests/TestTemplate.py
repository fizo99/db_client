from unittest import TestCase
from db_client.scripts import db
import os

class TestTemplate(TestCase):
    BASE_DB_NAME = "abc"
    BASE_DB_NAME_EXTENSION = "abc.db"
    validTableStructure = [
        {
            "column_name": "abc",
            "data_type": "int"
        },
        {
            "column_name": "bca",
            "data_type": "varchar"
        }
    ]
    invalidTableStructure = [
        {
            "column_name": "abc",
            "data_type": "dsads"
        },
        {
            "column_name": "bca",
            "data_type": "varchar"
        }
    ]

    def setUp(self):
        db.createDB("abc")

    def tearDown(self):
        os.remove(os.path.join(os.getcwd(), 'databases', "abc.db"))