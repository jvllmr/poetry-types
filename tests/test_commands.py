from __future__ import annotations

import subprocess

import pytest
from .conftest import CustomTOMLFile


def test_update(toml_file: CustomTOMLFile):
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
    old_content = toml_file.poetry
    content = toml_file.poetry

    content["dependencies"].add("requests", "^2.27.1")  # type:ignore
    del content["dependencies"]["colorama"]  # type:ignore
    toml_file.write_poetry(content)
    subprocess.run(["python", "-m", "poetry", "--verbose", "types", "update"])
    assert (
        "types-colorama" not in toml_file.poetry["group"]["types"]["dependencies"]  # type:ignore
    )
    assert (
        "types-sqlalchemy" not in toml_file.poetry["group"]["types"]["dependencies"]  # type:ignore
    )
    assert (
        "types-requests" in toml_file.poetry["group"]["types"]["dependencies"]  # type:ignore
    )
    assert (
        "xlsxwriter" in toml_file.poetry["group"]["types"]["dependencies"]  # type:ignore
    )

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
    toml_file.write_poetry(old_content)
    subprocess.run(["python", "-m", "poetry", "--verbose", "types", "update"])


@pytest.mark.parametrize(
    "package",
    [
        "requests",
    ],
)
def test_add(package: str, toml_file: CustomTOMLFile):
    types_package = f"types-{package}"
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", types_package]
        ).returncode
        != 0
    )

    subprocess.run(["python", "-m", "poetry", "--verbose", "types", "add", package])
    assert "types-requests" in toml_file.poetry["group"]["types"]["dependencies"]  # type: ignore
    assert "xlsxwriter" in toml_file.poetry["group"]["types"]["dependencies"]  # type: ignore

    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", types_package]
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "--verbose", "types", "remove", package]
        ).returncode
        == 0
    )


@pytest.mark.parametrize(
    "package",
    ["colorama"],
)
def test_remove(package: str, toml_file: CustomTOMLFile):
    types_package = f"types-{package}"
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", types_package]
        ).returncode
        == 0
    )

    subprocess.run(["python", "-m", "poetry", "-vvv", "types", "remove", package])
    assert "types-colorama" not in toml_file.poetry["group"]["types"]["dependencies"]  # type: ignore
    assert "xlsxwriter" in toml_file.poetry["group"]["types"]["dependencies"]  # type: ignore

    assert (
        subprocess.run(
            ["python", "-m", "poetry", "run", "pip", "show", types_package]
        ).returncode
        != 0
    )
    assert (
        subprocess.run(
            ["python", "-m", "poetry", "--verbose", "types", "add", package]
        ).returncode
        == 0
    )
