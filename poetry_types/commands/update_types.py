from cleo.io.inputs.argv_input import ArgvInput

from poetry_types.commands.add_types import AddTypesCommand
from poetry_types.commands.remove_types import RemoveTypesCommand
from poetry_types.commands.base import TypesCommand
import sys


class UpdateTypesCommand(TypesCommand):
    name = "types update"

    arguments = []

    def handle(self):
        content = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        deps = poetry_content["dependencies"].keys()
        try:
            type_deps = poetry_content["group"]["types"]["dependencies"].keys()
        except KeyError:
            type_deps = []

        to_be_installed = self.find_packages(
            filter(
                lambda dep: dep.lower()
                not in map(
                    lambda s: s[6:].lower(),
                    filter(lambda s: s.startswith("types-"), type_deps),
                ),
                deps,
            )
        )
        to_be_removed = list(
            map(
                lambda s: "types-" + s,
                filter(
                    lambda s: s not in map(lambda dep: dep.lower(), deps),
                    map(
                        lambda s: s[6:].lower(),
                        filter(lambda s: s.startswith("types-"), type_deps),
                    ),
                ),
            )
        )
        io = self.io

        if to_be_installed:
            new_argv = (
                sys.argv[:2] + to_be_installed
                if not self.io.input.has_argument("packages")
                else self.find_packages(self.argument("packages"))
            )
            io.set_input(ArgvInput(new_argv))

            AddTypesCommand().run_after(io, self)

        if to_be_removed:
            new_argv = (
                sys.argv[:2] + to_be_removed
                if not self.io.input.has_argument("packages")
                else self.find_packages(self.argument("packages"))
            )
            io.set_input(ArgvInput(new_argv))

            RemoveTypesCommand().run_after(io, self)
