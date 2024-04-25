# poetry-types

[![PyPI version](https://badge.fury.io/py/poetry-types.svg)](https://badge.fury.io/py/poetry-types)
[![GitHub license](https://img.shields.io/github/license/jvllmr/poetry-types)](https://github.com/jvllmr/poetry-types/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/jvllmr/poetry-types)](https://github.com/jvllmr/poetry-types/issues)
![PyPI - Downloads](https://img.shields.io/pypi/dd/poetry-types)
![Tests](https://github.com/jvllmr/poetry-types/actions/workflows/main.yml/badge.svg)

## Description

This is a plugin to poetry for the upcoming poetry 1.2 plugin feature.
It installs/removes/updates typing stubs via following commands:

- `poetry types add <package names>`
- `poetry types remove <package names>`
- `poetry types update <package names>`

## Usage examples

- `poetry types add openpyxl` adds `openpyxl` to your project
- `poetry types update` adds `types-openpyxl` if `openpyxl` is present, but `types-openpyxl` is not
- `poetry types update` removes `types-openpyxl` if `types-openpyxl` is present, but `openpyxl` is not

## Installation

Run `poetry self add poetry-types` for global install or run `poetry add -D poetry-types` to use this plugin with your project.

## Usage with pre-commit

```yaml
- repo: https://github.com/jvllmr/poetry-types
  rev: v0.5.1
  hooks:
    - id: poetry-types
```

### poetry-types has to be skipped with pre-commit.ci

```yaml
ci:
  skip: [poetry-types]
```
