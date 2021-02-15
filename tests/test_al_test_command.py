# Python import
import os
import subprocess

# Third party import
import pytest

# Local imports
from al_test import al_test_command


PYTHON_COMMAND_LINE = al_test_command.__file__
TEST_FILE = os.path.join(os.path.dirname(__file__), "test_inputs", 'correct.json')
HTML_FILE = os.path.join(os.path.dirname(__file__), "test_inputs", 'correct.html')
NOT_A_FILE = os.path.join(os.path.dirname(__file__), "test_inputs", 'not_a_file')


@pytest.mark.parametrize(
    "commands",
    [
        (['-f']),
        (['-i', TEST_FILE]),
        (['-i', TEST_FILE, '-e', 'json']),
        (['-i', TEST_FILE, '-e', 'plain']),
        (['-i', TEST_FILE, '-e', 'plain', '-v', 'red']),
    ],
)
def test_al_test_command__success(commands):
    full_command = ['python', PYTHON_COMMAND_LINE]
    full_command += commands
    p = subprocess.Popen(' '.join(full_command))
    p.communicate()

@pytest.mark.parametrize(
    "commands, expected",
    [
        (['-e', 'json'], 'MissingInput'),
        (['-i', NOT_A_FILE], 'WrongFiletype'),
        (['-i', HTML_FILE], 'WrongFiletype'),
        (['-i', TEST_FILE, '-e', 'nonexistent'], 'WrongExporter'),
    ],
)
def test_al_test_command__error(commands, expected):
    full_command = ['python', PYTHON_COMMAND_LINE]
    full_command += commands
    p = subprocess.Popen(' '.join(full_command), stderr=subprocess.PIPE)
    output, error = p.communicate()
    assert expected in str(error)
