# poetry-types

This is a plugin to poetry for the upcoming poetry 1.2 plugin feature.
It automatically installs/removes typing stubs when adding, removing or updating packages via commands.
Additionally, there are commands you can use to trigger this plugins behaviour:

- `poetry types add <package names>`
- `poetry types remove <package names>`
- `poetry types update`

## Installation

Run `poetry plugin add poetry-types` for global install or run `poetry add -D poetry-types` to use this plugin with your project.
