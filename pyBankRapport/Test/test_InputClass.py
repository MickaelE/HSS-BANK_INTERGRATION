from unittest import TestCase

from bankfiler.Camt54d import InputsClass


class InputsClassObject(TestCase):
    def setUp(self):
        self.InputsClass = InputsClass()


class TestInputsClass(InputsClassObject):
    def test_parsecam54(self):
        file = 'CAMT.054CNordea.xml'
        self.assertEqual(InputsClass.ParseDebitorFile(file), 0, "works")
