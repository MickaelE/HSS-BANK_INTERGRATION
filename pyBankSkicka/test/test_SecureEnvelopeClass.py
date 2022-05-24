from unittest import TestCase
from pyBankSkicka.BankSkicka.SecureEnvelopeClass import SecureEnvelope


class TestSecureEnvelope(TestCase):
    def test_create_xml(self):
        customer_id = ''
        command = ''
        timestamp = ''
        environment = ''
        targetid = ''
        softwareid = ''
        filetype = ''
        content = ''
        digest_value = ''
        signature_value = ''
        x509_issuer_name = ''
        x509_serial_number = ''
        x509_certificate = ''
        file_name = ''
        secureenvelope = SecureEnvelope(customer_id, command, timestamp,
                                        environment, targetid,
                                        softwareid, filetype, content,
                                        digest_value, signature_value,
                                        x509_issuer_name, x509_serial_number,
                                        x509_certificate, file_name)
        secureenvelope.CreateXml()
        self.fail()
