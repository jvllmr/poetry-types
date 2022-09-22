from __future__ import annotations

from cleo.helpers import argument

from poetry_types.commands.base import TypesCommand


class AddTypesCommand(TypesCommand):
    name = "types add"

    description = "Adds type stub dependencies for given packages."

    arguments = [
        argument("packages", "The packages to add the typing stubs for", multiple=True)
    ]

    help = (
        "<c1>types add sqlalchemy</c1> adds <c1>types-sqlalchemy</c1> to your project"
    )

    def handle(self) -> int:
        self.sanitize_types_section()
        packages = self.argument("packages")
        packages = self.find_packages(self.convert_to_type_packages_names(packages))
        existing_packages = self.get_existing_type_packages(packages)

        packages = [package for package in packages if package not in existing_packages]

        if not packages:
            self.line("No new type packages to add.")
            return 0

        return self.install_packages(packages)
