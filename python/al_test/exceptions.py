"""Module to create the necessary exceptions for the test"""


class AddresseeException(Exception):
    pass


class MissingInformation(AddresseeException):
    pass


class MissingInput(AddresseeException):
    pass


class WrongFiletype(AddresseeException):
    pass


class WrongExporter(AddresseeException):
    pass
