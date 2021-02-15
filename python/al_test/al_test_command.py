"""Command line tool for animal logic's test"""
# Python imports
import argparse

# Local imports
from al_test.exceptions import MissingInput, WrongFiletype, WrongExporter
from al_test.adapters import base
from al_test.adapters import *  # noqa: F403,F401


def parse_arguments():
    """Parses the given arguments

    Returns:
        argparse.ArgumentParser: The parsed arguments
    """
    description = (
        "Animal Logic's coding test, \n"
        "Serialize/deserialize name/address/phone number"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i",
        "--input",
        dest="input",
        type=str,
        help="The file to serialize and deserialize",
    )
    parser.add_argument(
        "-f",
        "--formats",
        action="store_true",
        help="Shows the available formats",
    )
    parser.add_argument(
        "-e",
        "--export",
        dest="export",
        default="XML",
        type=str,
        help="Export to the following format",
    )
    parser.add_argument(
        "-v",
        "--variant",
        dest="variant",
        default="default",
        type=str,
        help="Use the following variant",
    )
    return parser.parse_args()


def _show_available_formats():
    """ Prints the available importers/exporters"""
    importers = base.AdapterRegistryBase.get_importers()
    print("Available importers : {}".format([key for key in importers.keys()]))

    exporters = base.AdapterRegistryBase.get_exporters()
    print("Available exporters : {}".format([key for key in exporters.keys()]))


def main():
    """Main function, parses the arguments"""
    arguments = parse_arguments()

    # If -f, show available formats, ignore other options
    if arguments.formats:
        _show_available_formats()
        return

    # -i input file needed
    if not arguments.input:
        raise MissingInput("You need to specify the input file")

    # Try to fetch an adapter for the given file (using extension)
    importer = base.AdapterRegistryBase.get_needed_importer(arguments.input)
    if not importer:
        raise WrongFiletype("The given filepath cannot be imported")

    # Serialize the input file
    addressee = importer().serialize(arguments.input)

    # Deserialize to the wanted export/variant
    exporter = base.AdapterRegistryBase.get_needed_exporter(
        arguments.export, arguments.variant
    )
    if not exporter:
        raise WrongExporter("The given filepath cannot be imported")

    exporter().deserialize(addressee)


if __name__ == "__main__":
    main()
