#  Copyright (c) 2022. Mickael Eriksson

from unittest import TestCase

from DBClass import db_execution


class Test(TestCase):
    def test_db_execution(self):
        rows = db_execution()
        rows
        self.fail()
