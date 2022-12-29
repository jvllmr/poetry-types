from __future__ import annotations

from cleo.helpers import argument

from poetry_types.commands.base import GROUP_NAME, TypesCommand


class UpdateTypesCommand(TypesCommand):
    name = "types update"

    description = "Adds/Removes type stubs according to pyproject.toml."

    arguments = [
        argument(
            "packages",
            "The packages to update the type stubs for.",
            multiple=True,
            optional=True,
        )
    ]

    help = "<c1>types update</c1> adds/removes type stubs for every dependency in the project"

    def collect_all_packages_not_in_types_section(self) -> dict[str, str]:
        poetry_content = self.pyproject_poetry_content()
        packages = {}
        if "dependencies" in poetry_content:
            packages.update(poetry_content["dependencies"])

        if "group" in poetry_content:
            for group in poetry_content["group"]:
                if group == GROUP_NAME:
                    continue
                group_content = poetry_content["group"][group]
                if "dependencies" in group_content:
                    packages.update(group_content["dependencies"])

        return packages

    def handle(self):
        packages = self.argument("packages")

        whitelist = {}
        self.sanitize_types_section()
        all_packages_not_in_types_section = (
            self.collect_all_packages_not_in_types_section()
        )
        pypi_type_packages = set(
            self.find_packages(
                self.convert_to_type_packages_names(all_packages_not_in_types_section)
            )
        )
        type_section_packages = set(self.get_existing_type_packages())

        to_add = pypi_type_packages.difference(type_section_packages)

        to_remove = {
            package
            for package in type_section_packages.difference(pypi_type_packages)
            if self.is_package_type_package_name(package)
        }

        if to_add:
            requirements = self.install_packages(to_add, True)
            whitelist.update(
                {
                    requirement["name"]: requirement["version"]
                    for requirement in requirements
                }
            )
        if to_remove:
            whitelist.update(self.remove_packages(to_remove, True))

        if packages:
            whitelist.update(
                {name: "*" for name in self.convert_to_type_packages_names(packages)}
            )

        self.installer.whitelist(whitelist)

        self.installer.only_groups([GROUP_NAME])

        self.installer.update(True)

        status = self.installer.run()

        if status == 0 and to_add:
            self.add_constraints_to_toml(requirements)

        return status
