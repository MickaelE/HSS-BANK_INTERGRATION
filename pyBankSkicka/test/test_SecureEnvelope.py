#  Copyright (c) 2022. Mickael Eriksson
import unittest
from unittest import TestCase
from BankSkicka.SecureEnvelope import SecureEnvelope


class TestBankFile(TestCase):
    def setUp(self):
        self.SecureEnvelope = SecureEnvelope()


class Test(TestBankFile):
    def test_secure_envelope(self):
        with open("test.xml", "r") as f:
            content_string = f.readlines()
            self.assertEqual(self.SecureEnvelope.__createXML__(content_string), 0)

    def test_secure_envelope_nordea(self):
        with open("test_nord.xml", "r") as f:
            content_string = f.readlines()
            self.assertEqual(self.SecureEnvelope.__createXML__(content_string), 0)
