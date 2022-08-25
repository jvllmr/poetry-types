from poetry.console.application import Application
from poetry.plugins import ApplicationPlugin

from poetry_types.commands import (
    AddTypesCommand,
    RemoveTypesCommand,
    UpdateTypesCommand,
)


class PoetryTypes(ApplicationPlugin):
    def activate(self, app: Application):
        app.command_loader.register_factory("types add", AddTypesCommand.factory)
        app.command_loader.register_factory("types remove", RemoveTypesCommand.factory)
        app.command_loader.register_factory("types update", UpdateTypesCommand.factory)
