from unittest import TestCase

from bankfiler.DBclass import DBclass


class Test(TestCase):
    def test_create_pool(self):
        self.assertEqual(DBclass.create_pool, DBclass.create_pool, "works")
