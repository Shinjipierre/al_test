"""Module to define adapters and a registry for them"""
# Python imports
from abc import abstractmethod, ABCMeta
import os
import tempfile

from al_test.addressee import Addressee


class AdapterRegistryBase(ABCMeta):
    """Base adapter registry, to know which adapters are available"""

    REGISTRY = {}

    def __new__(
        cls, name: str, bases, namespace: str, **kwargs
    ) -> "AdapterRegistryBase":
        """
        Register class when child metaclass is instanced,
        arguments passed from ABCMeta
        """
        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        entry = "{}/{}".format(new_cls.NAME, new_cls.VARIANT)
        cls.REGISTRY[entry.lower()] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls) -> dict:
        """Get all the classes added in the registry"""
        return cls.REGISTRY

    @classmethod
    def get_importers(cls) -> dict:
        """Get all the importers with an extension"""
        return {
            adapter.EXTENSION: adapter
            for adapter in cls.REGISTRY.values()
            if adapter.EXTENSION
        }

    @classmethod
    def get_exporters(cls) -> dict:
        """Get all the possible exporters"""
        return {
            name: adapter
            for name, adapter in cls.REGISTRY.items()
            if "deserialize" not in adapter.__abstractmethods__
        }

    @classmethod
    def get_needed_importer(cls, filepath: str) -> "AdapterRegistryBaseClass" or None:
        """Get the wanted importer from the extension of the file"""
        _basename, extension = os.path.splitext(filepath)
        if not extension:
            return None

        return cls.get_importers().get(extension[1:], None)

    @classmethod
    def get_needed_exporter(
        cls, name: str, variant: str
    ) -> "AdapterRegistryBaseClass" or None:
        """Get the wanted exporter from the extension of the file"""
        wanted_exporter = "{}/{}".format(name, variant)
        return cls.get_exporters().get(wanted_exporter.lower(), None)


class AdapterRegistryBaseClass(metaclass=AdapterRegistryBase):
    """
    Base adapter class,
    adds abstract methods for the necessary serialize/deserialize
    """

    NAME = "base"
    EXTENSION = None
    VARIANT = "default"

    def __repr__(self):
        """Printing"""
        return "<{}> extension : .{}".format(self.__class__.__name__, self.EXTENSION)

    def _generate_tmp_file(self) -> str:
        """Generate a tmp file with the wanted extension"""
        return tempfile.NamedTemporaryFile(suffix=".{}".format(self.EXTENSION)).name

    @abstractmethod
    def serialize(self, filepath: str) -> Addressee:
        """Serialize the given file to an Addressee"""
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, addressee: Addressee) -> str:
        """Deserialize the given addressee"""
        raise NotImplementedError
