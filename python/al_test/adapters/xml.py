"""Module to define an XML adapter"""
# Python import
from xml.etree import ElementTree

# Local import
from al_test.adapters import base
from al_test.addressee import Addressee
from al_test.exceptions import MissingInformation


class XmlAdapter(base.AdapterRegistryBaseClass):
    """Adapter for XML"""

    NAME = "XML"
    EXTENSION = "xml"

    def serialize(self, filepath: str) -> Addressee:
        """Load an AML file and create an Addressee class from it"""
        # get the root of the xml file
        xml_tree = ElementTree.parse(filepath)
        root = xml_tree.getroot()

        # Try to find the wanted items
        info_dict = {}
        for info in ["name", "address", "phone"]:
            item = root.find(info)
            if item is None:
                message = "Missing {} inf the xml file".format(info)
                raise MissingInformation(message)

            info_dict[info] = item.text

        # Return an addressee class
        return Addressee(**info_dict)

    def deserialize(self, addressee: Addressee) -> str:
        """Deserialize the given addressee to an XML file"""
        # Build an xml tree
        element = ElementTree.Element("Addressee")
        for info in ["name", "address", "phone"]:
            item = ElementTree.SubElement(element, info)
            item.set("name", info)
            item.text = getattr(addressee, info)

        # Save the xml tree as data
        text_data = ElementTree.tostring(element)

        # Write the xml tree data in a file
        tmp_file = self._generate_tmp_file()
        with open(tmp_file, "wb") as f:
            f.write(text_data)

        print("Exported : {}".format(tmp_file))
        return tmp_file
