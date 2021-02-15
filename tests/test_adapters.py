# Python imports
from xml.etree.ElementTree import ParseError
import json
import os

# Thirst party imports
import pytest

# local imports
import al_test.adapters.json as json_adapter
import al_test.adapters.plain as plain_adapter
import al_test.adapters.xml as xml_adapter
from al_test.addressee import Addressee
from al_test.exceptions import MissingInformation


# Test files
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_inputs")

JSON_FILE_CORRECT = os.path.join(TEST_FILES_DIR, "correct.json")
JSON_FILE_MISSING_INFO = os.path.join(TEST_FILES_DIR, "missing_info.json")
JSON_FILE_TOO_MUCH_INFO = os.path.join(TEST_FILES_DIR, "too_much_info.json")
JSON_FILE_NO_INFO = os.path.join(TEST_FILES_DIR, "no_info.json")
JSON_FILE_NOT_A_JSON = os.path.join(TEST_FILES_DIR, "not_a_json.json")

XML_FILE_CORRECT = os.path.join(TEST_FILES_DIR, "correct.xml")
XML_FILE_MISSING_INFO = os.path.join(TEST_FILES_DIR, "missing_info.xml")
XML_FILE_TOO_MUCH_INFO = os.path.join(TEST_FILES_DIR, "too_much_info.xml")
XML_FILE_NO_INFO = os.path.join(TEST_FILES_DIR, "no_info.xml")
XML_FILE_NOT_A_JSON = os.path.join(TEST_FILES_DIR, "not_a_json.xml")

NOT_A_FILE = os.path.join(TEST_FILES_DIR, "not_a_file")


class TestJson:
    def setup(self):
        self.adapter = json_adapter.JsonAdapter()

    @pytest.mark.parametrize(
        "filepath, expected",
        [
            (JSON_FILE_NOT_A_JSON, json.JSONDecodeError),
            (NOT_A_FILE, FileNotFoundError),
            (JSON_FILE_NO_INFO, MissingInformation),
            (JSON_FILE_MISSING_INFO, MissingInformation),
        ],
    )
    def test_serialize__error(self, filepath, expected):
        with pytest.raises(expected):
            self.adapter.serialize(filepath)

    @pytest.mark.parametrize(
        "filepath, expected",
        [
            (
                JSON_FILE_CORRECT,
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
            ),
            (
                JSON_FILE_TOO_MUCH_INFO,
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
            ),
        ],
    )
    def test_serialize__correct(self, filepath, expected):
        result = self.adapter.serialize(filepath)
        assert result == expected

    @pytest.mark.parametrize(
        "addressee",
        [
            (Addressee("Remi", "1200 west 5th Avenue", "604 000 0000")),
        ],
    )
    def test_deserialize(self, addressee):
        result = self.adapter.deserialize(addressee)
        assert self.adapter.serialize(result) == addressee


class TestPlain:
    def setup(self):
        self.adapter = plain_adapter.PlainAdapter()

    @pytest.mark.parametrize(
        "addressee, expected",
        [
            (
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
                "Name: Remi\nAddress: 1200 west 5th Avenue\nPhone: 604 000 0000",
            ),
        ],
    )
    def test_deserialize(self, addressee, expected):
        result = self.adapter.deserialize(addressee)
        assert result == expected


class TestRedPlain:
    def setup(self):
        self.adapter = plain_adapter.RedPlainAdapter()

    @pytest.mark.parametrize(
        "addressee, expected",
        [
            (
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
                "Name: Remi\nAddress: 1200 west 5th Avenue\nPhone: 604 000 0000",
            ),
        ],
    )
    def test_deserialize(self, addressee, expected):
        result = self.adapter.deserialize(addressee)
        assert expected in result


class TestXml:
    def setup(self):
        self.adapter = xml_adapter.XmlAdapter()

    @pytest.mark.parametrize(
        "filepath, expected",
        [
            (JSON_FILE_CORRECT, ParseError),
            (NOT_A_FILE, FileNotFoundError),
            (XML_FILE_NO_INFO, MissingInformation),
            (XML_FILE_MISSING_INFO, MissingInformation),
        ],
    )
    def test_serialize__error(self, filepath, expected):
        with pytest.raises(expected):
            self.adapter.serialize(filepath)

    @pytest.mark.parametrize(
        "filepath, expected",
        [
            (
                XML_FILE_CORRECT,
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
            ),
            (
                XML_FILE_TOO_MUCH_INFO,
                Addressee("Remi", "1200 west 5th Avenue", "604 000 0000"),
            ),
        ],
    )
    def test_serialize__correct(self, filepath, expected):
        result = self.adapter.serialize(filepath)
        assert result == expected

    @pytest.mark.parametrize(
        "addressee",
        [
            (Addressee("Remi", "1200 west 5th Avenue", "604 000 0000")),
        ],
    )
    def test_deserialize(self, addressee):
        result = self.adapter.deserialize(addressee)
        assert self.adapter.serialize(result) == addressee
