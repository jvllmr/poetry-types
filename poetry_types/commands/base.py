from cleo.helpers import argument

from cleo.io.io import IO

from poetry.console.commands.init import InitCommand


from poetry.console.commands.installer_command import InstallerCommand


class TypesCommand(InitCommand, InstallerCommand):
    name = None

    arguments = [
        argument(
            "packages",
            "The packages to add/remove the types for.",
            optional=True,
            multiple=True,
        )
    ]

    options = []

    _run_after = False

    def __init__(self) -> None:
        self._error_packages = []
        super().__init__()

    @property
    def runs_after(self) -> bool:
        return self._run_after

    def run_after(self, io: IO, cmd: InstallerCommand) -> int:

        self._application = cmd.application
        self._full_definition = None
        self._synopsis = cmd._synopsis
        self._installer = cmd._installer
        try:
            self._before_packages = self.poetry.file.read()["tool"]["poetry"]["group"][
                "types"
            ]["dependencies"].keys()
        except KeyError:
            self._before_packages = []

        self._run_after = True
        return self.run(io)

    def handle(self) -> int:
        raise NotImplementedError

    def type_packages(self, packages: list[str]) -> list[str]:
        def f(package: str):
            if package.startswith("types-"):
                return package
            return f"types-{package}"

        return list(map(f, packages))

    def find_packages(self, packages: list[str]) -> list[str]:
        ret = []
        for package in self.type_packages(packages):
            try:
                ret.append(self._find_best_version_for_package(package)[0])
            except ValueError:
                self._error_packages.append(package)
        return ret

    @classmethod
    def factory(cls):
        return cls()
