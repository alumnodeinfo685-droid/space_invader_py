from collections.abc import Sequence
from typing import Optional, Protocol, TypeVar

from src.domain.game_state import GameState


T = TypeVar("T")


class RandomProvider(Protocol):
    def choice(self, sequence: Sequence[T]) -> T:
        ...

    def randint(self, a: int, b: int) -> int:
        ...


class GameInputAdapter(Protocol):
    def handle_input(self, state: GameState) -> int:
        ...


class GameOutputAdapter(Protocol):
    def draw(self, state: GameState) -> None:
        ...


class GameLoopAdapter(Protocol):
    def run(self) -> None:
        ...
