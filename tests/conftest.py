import os
import shutil

from pytest import fixture
from tomlkit import TOMLDocument
from tomlkit.toml_file import TOMLFile


@fixture(scope="session", autouse=True)
def prepare_tests():
    os.chdir("tests")


@fixture(autouse=True)
def yield_example():
    shutil.copy2("pyproject.toml.example", "pyproject.toml")
    yield
    os.remove("pyproject.toml")
    try:
        os.remove("poetry.lock")
    except FileNotFoundError:
        pass


class CustomTOMLFile(TOMLFile):
    @property
    def poetry(self) -> TOMLDocument:
        content = self.read()
        return content["tool"]["poetry"]

    def write_poetry(self, doc: TOMLDocument):
        content = self.read()
        content["tool"]["poetry"] = doc
        self.write(content)


@fixture()
def toml_file():
    return CustomTOMLFile("pyproject.toml")
