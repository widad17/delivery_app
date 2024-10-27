from pytest import fixture

from src.services.command.abstract_command import AbstractCommand
from src.services.command.command_service import CommandService

INITIAL_VALUE = 5


class MyState:
    value = INITIAL_VALUE


class IncrementCommand(AbstractCommand):
    __state: MyState

    def __init__(self, state: MyState) -> None:
        super().__init__("Increment")
        self.__state = state

    def execute(self) -> None:
        self.__state.value += 1

    def undo(self) -> None:
        self.__state.value -= 1


class TestCommandService:
    service: CommandService
    state: MyState

    @fixture(autouse=True)
    def setup(self):
        self.service = CommandService.instance()
        self.state = MyState()

        yield

        CommandService.reset()
        self.service = None
        self.state = None

    def test_should_create(self):
        assert self.service is not None

    def test_should_execute(self):
        command = IncrementCommand(self.state)

        self.service.execute(command)

        assert self.state.value == INITIAL_VALUE + 1

    def test_should_undo(self):
        command = IncrementCommand(self.state)

        self.service.execute(command)
        self.service.undo()

        assert self.state.value == INITIAL_VALUE

    def test_should_redo(self):
        command = IncrementCommand(self.state)

        self.service.execute(command)
        self.service.undo()
        self.service.redo()

        assert self.state.value == INITIAL_VALUE + 1

    def test_should_not_undo_when_root(self):
        command = IncrementCommand(self.state)

        self.service.execute(command)
        self.service.undo()
        self.service.undo()

        assert self.state.value == INITIAL_VALUE

    def test_should_not_redo_when_detached(self):
        command = IncrementCommand(self.state)

        self.service.execute(command)
        self.service.undo()
        self.service.redo()
        self.service.redo()

        assert self.state.value == INITIAL_VALUE + 1
