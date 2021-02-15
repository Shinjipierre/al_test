"""Module to define an addressee (name/address/phone)"""
# Local imports
from al_test.exceptions import MissingInformation


class Addressee(object):
    """Class that defines an addressee"""

    def __init__(self, name, address, phone):
        """Initialization method

        Args:
            name (str): The name of the person
            address (str): The address of the person
            phone (str): The phone number of the person
        """
        self.name = name
        self.address = address
        self.phone = phone
        self._validate()

    def __repr__(self):
        """ print statement"""
        return "Name: {name}\nAddress: {address}\nPhone: {phone}".format(
            **self.to_dict()
        )

    def __eq__(self, other):
        """ Check equality"""
        return self.to_dict() == other.to_dict()

    def _validate(self):
        """ Throw if none of the information is given """
        if not all(self.to_dict().values()):
            message = "name/address/phone need to be filled correctly"
            raise MissingInformation(message)

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
        }
