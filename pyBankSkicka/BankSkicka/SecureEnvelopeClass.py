import xml.etree.ElementTree as ET


class SecureEnvelope:
    def __init__(self, CustomerId, Command, Timestamp, environment, targetid,
                 softwareid, filetype, content, DigestValue, SignatureValue,
                 X509IssuerName, X509SerialNumber, X509Certificate, fileName):
        self.CustomerId = CustomerId
        self.Command = Command
        self.Timestamp = Timestamp
        self.environment = environment
        self.targetid = targetid
        self.softwareid = softwareid
        self.filetype = filetype
        self.content = content
        self.DigestValue = DigestValue
        self.SignatureValue = SignatureValue
        self.X509IssuerName = X509IssuerName
        self.X509SerialNumber = X509SerialNumber
        self.X509Certificate = X509Certificate
        self.fileName = fileName
        self.xmlns_uris = {'': 'http://bxd.fi/xmldata/',
                           'xsi': 'http://www.w3.org/2001/XMLSchema-instance/'}

    def CreateXml(self):
        root_node = ET.Element("ApplicationRequest")
        # region root
        customerid = ET.SubElement(root_node, "CustomerId")
        customerid.text = self.CustomerId
        command = ET.SubElement(root_node, "Command")
        command.text = self.Command
        timestamp = ET.SubElement(root_node, "Timestamp")
        timestamp.text = self.Timestamp
        environment = ET.SubElement(root_node, "Environment")
        environment.text = self.environment
        targetid = ET.SubElement(root_node, "TargetId")
        targetid.text = self.targetid
        softwareid = ET.SubElement(root_node, "SoftwareId")
        softwareid.text = self.softwareid
        filetype = ET.SubElement(root_node, "FileType")
        filetype.text = self.filetype
        content = ET.SubElement(root_node, "Content")
        content.text = self.content
        # endregion root
        # region Signature
        signature = ET.SubElement(root_node, "Signature",
                                  xmlns="http://www.w3.org/2000/09/xmldsig#")
        # region signedinfo
        signedinfo = ET.SubElement(signature, "SignedInfo")
        canonicalizationmethod = ET.SubElement(signedinfo,
                                               "CanonicalizationMethod",
                                               Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
        signaturemethod = ET.SubElement(signedinfo, "SignatureMethod",
                                        Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1")

        # region Reference
        reference = ET.SubElement(signedinfo, "Reference", URI="")
        transforms = ET.SubElement(reference, "Transforms")
        transform = ET.SubElement(transforms, "Transform",
                                  Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
        digestmethod = ET.SubElement(reference, "DigestMethod",
                                     Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
        digestvalue = ET.SubElement(reference, "DigestValue")
        digestvalue.text = self.DigestValue
        # endregion Reference
        # endregion signedinfo
        signaturevalue = ET.SubElement(signature, "SignatureValue")
        signaturevalue.text = self.SignatureValue
        # region KeyInfo
        keyinfo = ET.SubElement(signature, "KeyInfo")
        # region X509Data
        x509data = ET.SubElement(keyinfo, "X509Data")
        x509issuerserial = ET.SubElement(x509data, "X509IssuerSerial")
        x509issuername = ET.SubElement(x509issuerserial, "X509IssuerName")
        x509issuername.text = self.X509IssuerName
        x509serialnumber = ET.SubElement(x509issuerserial, "X509SerialNumber")
        x509serialnumber.text = self.X509SerialNumber
        x509certificate = ET.SubElement(keyinfo, "X509Certificate")
        x509certificate.text = self.X509Certificate
        # endregion X509Data
        # endregion KeyInfo
        # endregion Signature
        add_XMLNS_attributes(root_node, self.xmlns_uris)
        tree = ET.ElementTree(root_node)
        tree.write(self.fileName)


def annotate_with_XMLNS_prefixes(tree, xmlns_prefix,
                                 skip_root_node=True):
    if not ET.iselement(tree):
        tree = tree.getroot()
    iterator = tree.iter()
    if skip_root_node:  # Add XMLNS prefix also to the root node?
        iterator.next()
    for e in iterator:
        if not ':' in e.tag:
            e.tag = xmlns_prefix + ":" + e.tag


def add_XMLNS_attributes(tree, xmlns_uris_dict):
    if not ET.iselement(tree):
        tree = tree.getroot()
    for prefix, uri in xmlns_uris_dict.items():
        tree.attrib['xmlns:' + prefix] = uri
