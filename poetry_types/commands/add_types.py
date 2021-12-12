from cleo.io.inputs.argv_input import ArgvInput


from cleo.io.outputs.output import Verbosity
from poetry.console.commands.add import AddCommand
import sys
from poetry_types.commands.base import TypesCommand


class AddTypesCommand(TypesCommand):

    name = "types add"

    def handle(self) -> int:
        io = self.io

        packages = self.find_packages(io.input.argument("packages"))
        if self._run_after:
            io.write("Installing missing type stubs...")
            io.set_verbosity(Verbosity.QUIET)

        io.set_input(
            ArgvInput(
                sys.argv[:2] + packages + ["-G", "types"],
            )
        )
        cmd = AddCommand()
        cmd.set_application(self.get_application())
        cmd.set_installer(self.installer)
        cmd.set_env(self.env)
        cmd.set_poetry(self.poetry)
        cmd.run(io)
        io.set_verbosity(Verbosity.NORMAL)
        if self._run_after:
            installed_packages = list(
                filter(
                    lambda p: p
                    in self.poetry.file.read()["tool"]["poetry"]["group"]["types"][
                        "dependencies"
                    ].keys()
                    and p not in self._before_packages,
                    packages,
                )
            )
            if installed_packages:
                io.write_line("\rInstalled the following type stubs:" + 20 * " ")
                io.write_line("")
                for package in installed_packages:
                    io.write_line(f"  \U00002022 {package}")
            else:
                io.write_line("\rNo type stubs were installed." + 20 * " ")
        io.write_line("")
