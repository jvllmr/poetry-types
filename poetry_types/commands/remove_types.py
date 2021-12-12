from cleo.io.outputs.output import Verbosity
from poetry.console.commands.remove import RemoveCommand
import sys
from poetry_types.commands.base import TypesCommand

from cleo.io.inputs.argv_input import ArgvInput


class RemoveTypesCommand(TypesCommand):
    name = "types remove"

    def handle(self) -> int:
        io = self.io
        if self._run_after:
            io.write("Removing removable type stubs...")
            io.set_verbosity(Verbosity.QUIET)
        packages = self.find_packages(io.input.argument("packages"))

        io.set_input(
            ArgvInput(
                sys.argv[:2] + packages + ["-G", "types"],
            )
        )

        cmd = RemoveCommand()
        cmd.set_application(self.get_application())
        cmd.set_installer(self.installer)
        cmd.set_env(self.env)
        cmd.set_poetry(self.poetry)
        cmd.run(io)
        io.set_verbosity(Verbosity.NORMAL)
        if self._run_after:
            removed_packages = list(
                filter(
                    lambda p: p
                    not in self.poetry.file.read()["tool"]["poetry"]["group"]["types"][
                        "dependencies"
                    ].keys()
                    and p in self._before_packages,
                    packages,
                )
            )
        if removed_packages:
            io.write_line("\rRemoved the following type stubs:" + 20 * " ")
            io.write_line("")
            for package in removed_packages:
                io.write_line(f"  \U00002022 {package}")
        else:
            io.write_line("\rNo type stubs were removed.")

        io.write_line("")
