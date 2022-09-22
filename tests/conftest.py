import os
import shutil
import subprocess

from pytest import fixture
from tomlkit import TOMLDocument
from tomlkit.toml_file import TOMLFile


@fixture(scope="session", autouse=True)
def prepare_tests():
    os.chdir("tests")


@fixture(autouse=True)
def yield_example():
    shutil.copy2("pyproject.toml.example", "pyproject.toml")
    try:
        os.remove("poetry.lock")
    except FileNotFoundError:
        pass
    subprocess.run(["poetry", "install"])
    yield
    subprocess.run(
        ["python", "-m", "poetry", "remove", "--group", "types", "types-requests"]
    )
    # os.remove("pyproject.toml")


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
