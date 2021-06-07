from unittest import TestCase
from db_client.scripts import db
import os

from db_client.scripts.exceptions.DatabaseExistsException import DatabaseExistsException
from db_client.scripts.exceptions.WrongNameException import WrongNameException


class Test(TestCase):
    def test_createDB_shouldCreateDB(self):
        # create database
        db.createDB("abc")

        # get all available databases
        names = db.getDatabaseNames()

        self.assertListEqual(names, ["abc.db"])

        os.remove(os.path.join(os.getcwd(), 'databases', "abc.db"))

    def test_createDB_shouldRaiseDatabaseExistsException_whenDBExists(self):
        # create database twice
        db.createDB("abc")

        self.assertRaises(DatabaseExistsException, db.createDB, "abc")

        os.remove(os.path.join(os.getcwd(), 'databases', "abc.db"))

    def test_createDB_shouldRaiseWrongNameException_whenNameNotValid(self):
        # create database twice
        wrongNames = ["abc.db","*^ndshu.ab", ".djsda.sad"]
        for name in wrongNames:
            self.assertRaises(WrongNameException, db.createDB, name)


