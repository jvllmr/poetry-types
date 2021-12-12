from poetry.console.commands.remove import RemoveCommand
from poetry.plugins import ApplicationPlugin
from poetry.console.application import Application

from poetry.console.commands.update import UpdateCommand
from poetry.console.commands.add import AddCommand

from cleo.events.console_events import COMMAND
from cleo.events.console_command_event import ConsoleCommandEvent
from poetry_types.commands import (
    AddTypesCommand,
    RemoveTypesCommand,
    UpdateTypesCommand,
)


class PoetryTypes(ApplicationPlugin):
    def activate(self, app: Application):
        app.event_dispatcher.add_listener(COMMAND, self.onCommand)
        app.command_loader.register_factory("types add", AddTypesCommand.factory)
        app.command_loader.register_factory("types remove", RemoveTypesCommand.factory)
        app.command_loader.register_factory("types update", UpdateTypesCommand.factory)

    def onCommand(self, event: ConsoleCommandEvent, *_):
        command = event.command
        io = event.io

        if command.run(io):
            return
        event.disable_command()
        io.write_line("")

        if isinstance(command, UpdateCommand):
            UpdateTypesCommand().run_after(io, command)
        elif isinstance(command, AddCommand):
            AddTypesCommand().run_after(io, command)
        elif isinstance(command, RemoveCommand):
            RemoveTypesCommand().run_after(io, command)
