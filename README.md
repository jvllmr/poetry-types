
# poetry-types

This is a plugin to poetry for the upcoming poetry 1.2 plugin feature.
It installs/removes/updates typing stubs via following commands:

- `poetry types add <package names>`
- `poetry types remove <package names>`
- `poetry types update <package names>`

## Usage examples

- `poetry types add SQLAlchemy` adds `types-SQLAlchemy` to your project
- `poetry types update` adds `types-SQLAlchemy` if `SQLAlchemy` is present, but not `types-SQLAlchemy`
- `poetry types update` removes `types-SQLAlchemy` if `types-SQLAlchemy` is present, but not `SQLAlchemy`

## Installation

Run `poetry plugin add poetry-types` for global install or run `poetry add -D poetry-types` to use this plugin with your project.
