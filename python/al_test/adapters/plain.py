"""Module to define a PLAIN adapter"""
import colorama

# Local import
from al_test.adapters import base
from al_test.addressee import Addressee


class PlainAdapter(base.AdapterRegistryBaseClass):
    """Adapter for plain text"""

    NAME = "PLAIN"

    def serialize(self, filepath):
        return NotImplementedError

    def deserialize(self, addressee: Addressee) -> str:
        """Deserialize the given addressee to a plain text"""
        message = "Name: {name}\nAddress: {address}\nPhone: {phone}".format(
            **addressee.to_dict()
        )
        print(message)
        return message


class RedPlainAdapter(PlainAdapter):
    """Adapter for plain text"""

    VARIANT = "red"

    def deserialize(self, addressee: Addressee) -> str:
        """Deserialize the given addressee to a red text"""
        colorama.init()

        message = "{}Name: {name}\nAddress: {address}\nPhone: {phone}".format(
            colorama.Fore.RED, **addressee.to_dict()
        )
        print(message)
        return message
