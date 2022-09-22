from __future__ import annotations

from cleo.helpers import argument
from poetry.console.commands.remove import RemoveCommand

from poetry_types.commands.base import TypesCommand


class RemoveTypesCommand(TypesCommand, RemoveCommand):
    name = "types remove"

    description = "Removes a type stub package from project dependencies."

    arguments = [
        argument(
            "packages", "The packages to remove the type stubs for.", multiple=True
        )
    ]

    help = "<c1>types remove sqlalchemy</c1> removes <c1>types-sqlalchemy</c1> to your project"

    def handle(self) -> int:
        packages = self.argument("packages")
        self.sanitize_types_section()
        packages = set(
            self.find_packages(self.convert_to_type_packages_names(packages))
        )

        existing_packages = self.get_existing_type_packages()

        to_remove = packages.intersection(existing_packages)

        if not to_remove:
            self.line("No type packages to be removed.")
            return 0

        return self.remove_packages(to_remove)
