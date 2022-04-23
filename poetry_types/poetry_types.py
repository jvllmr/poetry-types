from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import TERMINATE
from poetry.console.application import Application
from poetry.console.commands.add import AddCommand
from poetry.console.commands.remove import RemoveCommand
from poetry.console.commands.update import UpdateCommand
from poetry.plugins import ApplicationPlugin

from poetry_types.commands import (
    AddTypesCommand,
    RemoveTypesCommand,
    UpdateTypesCommand,
)


class PoetryTypes(ApplicationPlugin):
    def activate(self, app: Application):
        app.event_dispatcher.add_listener(TERMINATE, self.onCommand)
        app.command_loader.register_factory("types add", AddTypesCommand.factory)
        app.command_loader.register_factory("types remove", RemoveTypesCommand.factory)
        app.command_loader.register_factory("types update", UpdateTypesCommand.factory)

    def onCommand(self, event: ConsoleCommandEvent, *_):
        command = event.command

        io = event.io

        io.write_line("")

        if isinstance(command, UpdateCommand):
            UpdateTypesCommand().run_after(io, command)
        elif isinstance(command, AddCommand):
            AddTypesCommand().run_after(io, command)
        elif isinstance(command, RemoveCommand):
            RemoveTypesCommand().run_after(io, command)
