# poetry-types

This is a plugin to poetry for the upcoming poetry 1.2 plugin feature.
It automatically installs/removes typing stubs when adding, removing or updating packages via commands.
Additionally, there are commands you can use to trigger this plugins behaviour:

- `poetry types add <package names>`
- `poetry types remove <package names>`
- `poetry types update`

## Installation

Run `poetry plugin add poetry-plugin`

Note: With poetry version 1.2.0a2 poetry removes all dependencies when using `poetry remove` and so does
`poetry types remove`. Using poetry from the git repo is recommended when testing this plugin.

## TODO:

- Add tests
- Make command-line output more beautiful maybe?
