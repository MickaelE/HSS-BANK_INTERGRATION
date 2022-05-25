from unittest import TestCase
from pyBankSkicka.BankSkicka.SecureEnvelopeClass import SecureEnvelope


class TestSecureEnvelope(TestCase):
    def test_create_xml(self):
        customer_id = '123456'
        command = 'UploadFile'
        timestamp = '2015-03-23T11:51:26.993+01:00'
        environment = 'PRODUCTION'
        targetid = '5780860238'
        softwareid = 'WTSSWebServices'
        filetype = 'NDCAPXMLI'
        content = 'gfgfdsgdfgfdgdfgfdgfdgdsfgfdgfgdfs'
        digest_value = 'pRE4OEvO6/2lskhDBqWyOC0axiM='
        signature_value = 'Vfk2JDSVodavcNGPua8WWWaNl' \
                          '/L7bgne9KLwF9zE7Nx6gFSepDhKSvI8y' \
                          '+5tFVLNfwFx9XNuqkfDrcrddQb+XWB5R6pz3ugP' \
                          '/aLpm46BMaM3twP5AkCkhvJvOoavEBYLRAwjLzL1KD' \
                          '+OQpYc1pXffRGEnSHBCZH/vxNIribycBI='
        x509_issuer_name = 'SERIALNUMBER=516406-0120, CN=Nordea Corporate CA ' \
                           '01, O=Nordea Bank AB (publ), C=SE '
        x509_serial_number = '24988089'
        x509_certificate = 'MIIDwTCCAqmgAwIBAgIEAX1JuTANBgkqhkiG9w0BAQUFADBk' \
                           'MQswCQYDVQQGEwJTRTEeMBwGA1UEChMVTm9yZGVhIEJhbmsg' \
                           'QUIgKHB1YmwpMR8wHQYDVQQDExZOb3JkZWEgQ29ycG9yYXRl' \
                           'IENBIDAxMRQwEgYDVQQFEws1MTY0MDYtMDEyMDAeFw0xMzA1' \
                           'MDIxMjI2MzRaFw0xNTA1MDIxMjI2MzRaMEQxCzAJBgNVBAYT' \
                           'AkZJMSAwHgYDVQQDDBdOb3JkZWEgRGVtbyBDZXJ0aWZpY2F0' \
                           'ZTETMBEGA1UEBRMKNTc4MDg2MDIzODCBnzANBgkqhkiG9w0B' \
                           'AQEFAAOBjQAwgYkCgYEAwtFEfAtbJuGzQwwRumZkvYh2BjGY' \
                           'VsAMUeiKtOne3bZSeisfCq+TXqL1gI9LofyeAQ9I/sDm6tL8' \
                           '0yrD5iaSUqVm6A739MsmpW/iyZcVf7ms8xAN51ESUgN6akwZ' \
                           'CU9pH62ngJDj2gUsktY0fpsoVsARdrvOFk0fTSUXKWd6LbcC' \
                           'AwEAAaOCAR0wggEZMAkGA1UdEwQCMAAwEQYDVR0OBAoECEBw' \
                           '2cj7+XMAMBMGA1UdIAQMMAowCAYGKoVwRwEDMBMGA1UdIwQM' \
                           'MAqACEALddbbzwunMDcGCCsGAQUFBwEBBCswKTAnBggrBgEF' \
                           'BQcwAYYbaHR0cDovL29jc3Aubm9yZGVhLnNlL0NDQTAxMA4G' \
                           'A1UdDwEB/wQEAwIFoDCBhQYDVR0fBH4wfDB6oHigdoZ0bGRh' \
                           'cCUzQS8vbGRhcC5uYi5zZS9jbiUzRE5vcmRlYStDb3Jwb3Jh' \
                           'dGUrQ0ErMDElMkNvJTNETm9yZGVhK0JhbmsrQUIrJTI4cHVi' \
                           'bCUyOSUyQ2MlM0RTRSUzRmNlcnRpZmljYXRlcmV2b2NhdGlv' \
                           'bmxpc3QwDQYJKoZIhvcNAQEFBQADggEBACLUPB1Gmq6286/s' \
                           'ROADo7N+w3eViGJ2fuOTLMy4R0UHOznKZNsuk4zAbS2KycbZ' \
                           'sE5py4L8o+IYoaS88YHtEeckr2oqHnPpz/0Eg7wItj8Ad+AF' \
                           'WJqzbn6Hu/LQhlnl5JEzXzl3eZj9oiiJ1q/2CGXvFomY7S4' \
                           'tgpWRmYULtCK6jode0NhgNnAgOI9uy76pSS16aDoiQWUJqQ' \
                           'gVydowAnqS9h9aQ6gedwbOdtkWmwKMDVXU6aRz9Gvk+JeYJ' \
                           'htpuP3OPNGbbC5L7NVdno+B6AtwxmG3ozd+mPcMeVuz6kKL' \
                           'AmQyIiBSrRNa5OrTkq/CUzxO9WUgTnm/Sri7zReR6mU= '
        file_name = 'test.xml'
        secureenvelope = SecureEnvelope(customer_id, command, timestamp,
                                        environment, targetid,
                                        softwareid, filetype, content,
                                        digest_value, signature_value,
                                        x509_issuer_name, x509_serial_number,
                                        x509_certificate, file_name)
        secureenvelope.CreateXml()
        self.fail()
