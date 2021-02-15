# Third party imports
import pytest

# Local imports
from al_test.addressee import Addressee
from al_test.exceptions import MissingInformation


@pytest.mark.parametrize(
    "name, address, phone, expected",
    [
        (
            "Remi",
            "1600 west 5th Avenue",
            "604 111 1111",
            {
                "name": "Remi",
                "address": "1600 west 5th Avenue",
                "phone": "604 111 1111",
            },
        ),
        (
            "Tatyana",
            "1500 east 2nd Avenue",
            "604 000 0000",
            {
                "name": "Tatyana",
                "address": "1500 east 2nd Avenue",
                "phone": "604 000 0000",
            },
        ),
    ],
)
def test_addressee_to_dict(name, address, phone, expected):
    addressee_class = Addressee(name=name, address=address, phone=phone)
    assert expected == addressee_class.to_dict()


@pytest.mark.parametrize(
    "name, address, phone",
    [
        ("", "", ""),
        ("name", "", ""),
        ("name", "address", ""),
    ],
)
def test__validate__fail(name, address, phone):
    with pytest.raises(MissingInformation):
        Addressee(name=name, address=address, phone=phone)

