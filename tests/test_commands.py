from __future__ import annotations

import subprocess

import pytest

from conftest import CustomTOMLFile


@pytest.mark.parametrize("command", [["types", "update"]])
def test_update(command: list[str], toml_file: CustomTOMLFile):
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-requests"]
        ).returncode
        != 0
    )

    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-colorama"]
        ).returncode
        == 0
    )

    content = toml_file.poetry
    content["dependencies"].add("requests", "^2.27.1")
    del content["dependencies"]["colorama"]
    toml_file.write_poetry(content)
    subprocess.run(["python", "-m", "poetry", "--verbose", *command])
    assert "types-colorama" not in toml_file.poetry["group"]["types"]["dependencies"]
    assert "types-requests" in toml_file.poetry["group"]["types"]["dependencies"]

    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-requests"]
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-colorama"]
        ).returncode
        != 0
    )


@pytest.mark.parametrize("command", [["types", "add", "requests"]])
def test_add(command: list[str], toml_file: CustomTOMLFile):
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-requests"]
        ).returncode
        != 0
    )

    subprocess.run(["python", "-m", "poetry", "--verbose", *command])
    assert "types-requests" in toml_file.poetry["group"]["types"]["dependencies"]
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-requests"]
        ).returncode
        == 0
    )


@pytest.mark.parametrize("command", [["types", "remove", "colorama"]])
def test_remove(command: list[str], toml_file: CustomTOMLFile):
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-colorama"]
        ).returncode
        == 0
    )

    subprocess.run(["python", "-m", "poetry", "--verbose", *command])
    assert "types-colorama" not in toml_file.poetry["group"]["types"]["dependencies"]
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", "types-colorama"]
        ).returncode
        != 0
    )
