import xml.etree.ElementTree as ET


class SecureEnvelope:
    def __init__(self):
        self.xmlns_uris = {'': 'http://myhost.com/p.xsd',
              'q': 'http://myhost.com/q.xsd'

    def CreateXml(self):
        root_node = ET.Element("root")


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
