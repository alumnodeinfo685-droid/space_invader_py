from typing import Protocol, Optional

from src.domain.game_state import GameState


class GameInputAdapter(Protocol):
    def handle_input(self, state: GameState) -> int:
        ...


class GameOutputAdapter(Protocol):
    def draw(self, state: GameState) -> None:
        ...


class GameLoopAdapter(Protocol):
    def run(self) -> None:
        ...
