from __future__ import annotations

import contextlib
import typing as t

import poetry.core.semver.helpers as semver
import poetry.factory as poetry_factory
import tomlkit
from packaging.utils import canonicalize_name
from poetry.console.commands.init import InitCommand
from poetry.console.commands.installer_command import InstallerCommand

from poetry_types.packages_map import PACKAGES_MAP

if t.TYPE_CHECKING:
    import tomlkit.items as tomlkit_items

GROUP_NAME = "types"


class TypesCommand(InitCommand, InstallerCommand):
    def pyproject_content(self) -> tomlkit.TOMLDocument:
        return self.poetry.file.read()

    def pyproject_poetry_content(self):
        return self.pyproject_content()["tool"]["poetry"]

    @t.overload
    def get_types_section(
        self, create_if_not_exists: t.Literal[False]
    ) -> tomlkit_items.Table | None:
        ...

    @t.overload
    def get_types_section(self) -> tomlkit_items.Table:
        ...

    @t.overload
    def get_types_section(
        self, create_if_not_exists: t.Literal[True]
    ) -> tomlkit_items.Table:
        ...

    def get_types_section(
        self, create_if_not_exists: bool = True
    ) -> tomlkit_items.Table:
        content = self.pyproject_content()

        try:
            return content["tool"]["poetry"]["group"][GROUP_NAME]["dependencies"]
        except KeyError:
            if create_if_not_exists:
                return self.create_types_section()
            return None

    def create_types_section(self):
        content = self.pyproject_content()

        path = ("tool", "poetry", "group", GROUP_NAME, "dependencies")
        section = content
        for n, key in enumerate(path):
            if key not in section:
                section[key] = (
                    tomlkit.table(is_super_table=True)
                    if n < len(path) - 1
                    else tomlkit.table()
                )
            section = section[key]
        self.poetry.file.write(content)
        return section

    def convert_to_type_packages_names(self, packages: list[str]):
        return [
            package
            if package.startswith("types-")
            else f"types-{package}"
            if package not in PACKAGES_MAP
            else PACKAGES_MAP[package]
            for package in packages
        ]

    def get_existing_type_packages(
        self, packages: list[str] | None = None, canonicalized=False
    ):
        """Filter type packages in pyproject.toml by names"""
        types_section = self.get_types_section(False)

        if types_section is None:
            return []
        if packages:
            return [
                package if not canonicalized else canonicalize_name(package)
                for package in packages
                for key in types_section
                if canonicalize_name(key) == canonicalize_name(package)
            ]

        return [
            package if not canonicalized else canonicalize_name(package)
            for package in types_section
        ]

    def add_constraints_to_toml(self, constraints: list[dict[str, str]]):

        types_section = self.get_types_section()

        content = self.pyproject_content()
        poetry_content = content["tool"]["poetry"]

        for constraint in constraints:
            name = constraint["name"]
            version = constraint["version"]
            types_section[name] = version

        poetry_content["group"][GROUP_NAME]["dependencies"] = types_section

        self.poetry.file.write(content)

    def remove_packages_from_toml(self, packages: list[str]):
        content = self.pyproject_content()
        poetry_content = content["tool"]["poetry"]
        types_section = self.get_types_section()

        if types_section is None:
            return {}

        removed: dict[str, str] = {}
        for package in packages:
            removed[package] = types_section[package]
            del types_section[package]

        if not types_section and GROUP_NAME in poetry_content["group"]:
            del poetry_content["group"][GROUP_NAME]["dependencies"]
        else:
            poetry_content["group"][GROUP_NAME]["dependencies"] = types_section
        self.poetry.file.write(content)
        return removed

    def find_packages(self, packages: list[str]):
        found_packages = []
        for package in packages:
            try:
                found_packages.append(self._find_best_version_for_package(package)[0])
            except ValueError:
                pass
        return found_packages

    def install_packages(self, packages: list[str], prepare_only=False):
        section = self.get_types_section()

        content = self.pyproject_content()

        packages = self.find_packages(packages)

        requirements = self._determine_requirements(packages)

        for _constraint in requirements:
            version = _constraint.get("version")
            if version is not None:
                assert isinstance(version, str)
                semver.parse_constraint(version)

            constraint: dict[str, t.Any] = tomlkit.inline_table()
            for name, value in _constraint.items():
                if name == "name":
                    continue

                constraint[name] = value

            if len(constraint) == 1 and "version" in constraint:
                constraint = constraint["version"]

            constraint_name = _constraint["name"]
            assert isinstance(constraint_name, str)
            section[constraint_name] = constraint

            with contextlib.suppress(ValueError):
                self.poetry.package.dependency_group(GROUP_NAME).remove_dependency(
                    constraint_name
                )

            self.poetry.package.add_dependency(
                poetry_factory.Factory.create_dependency(
                    constraint_name,
                    constraint,
                    groups=[GROUP_NAME],
                    root_dir=self.poetry.file.parent,
                )
            )
        if not prepare_only:
            status = self.installer_action(
                [requirement["name"] for requirement in requirements]
            )

            if status == 0:

                assert isinstance(content, tomlkit.TOMLDocument)

                self.add_constraints_to_toml(requirements)

            return status

        return requirements

    def remove_packages(self, packages: list[str], prepare_only=False):
        removed = self.remove_packages_from_toml(packages)
        group = self.poetry.package.dependency_group(GROUP_NAME)
        for package in packages:
            group.remove_dependency(package)
        if not prepare_only:
            return self.installer_action(packages)
        return removed

    def installer_action(self, packages: list[str]):
        self.poetry.set_locker(
            self.poetry.locker.__class__(
                self.poetry.locker.lock.absolute().as_posix(),
                self.pyproject_poetry_content(),
            )
        )
        self.installer.set_locker(self.poetry.locker)

        self.installer.set_package(self.poetry.package)
        self.installer.update(True)
        self.installer.whitelist(packages)

        return self.installer.run()

    def sanitize_types_section(self):
        types_section = self.get_types_section(False)

        if types_section is None:
            return

        content = self.pyproject_content()

        for package in types_section.copy():
            new_names = self.find_packages([package])
            version = types_section[package]

            if new_names and new_names[0] != package:
                types_section[new_names[0]] = version
                del types_section[package]
            elif not new_names:
                del types_section[package]

        content["tool"]["poetry"]["group"][GROUP_NAME]["dependencies"] = types_section
        self.poetry.file.write(content)

    @classmethod
    def factory(cls):
        return cls()
