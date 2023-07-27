"""Module to define a JSON adapter"""
# Python import
import json

# Local import
from al_test.adapters import base
from al_test.addressee import Addressee


class JsonAdapter(base.AdapterRegistryBaseClass):
    """Adapter for Json"""

    NAME = "JSON"
    EXTENSION = "json"

    def serialize(self, filepath: str) -> Addressee:
        """Load a json file and create an Addressee class from it"""
        with open(filepath) as f:
            data = json.load(f)

        # Return an addressee class
        return Addressee(
            name=data.get("name", ""),
            address=data.get("address", ""),
            phone=data.get("phone", ""),
        )

    def deserialize(self, addressee: Addressee) -> str:
        """Deserialize the given addressee to a json file"""
        tmp_file = self._generate_tmp_file()
        with open(tmp_file, "w") as f:
            json.dump(addressee.to_dict(), f)

        print("Exported : {}".format(tmp_file))
        return tmp_file
