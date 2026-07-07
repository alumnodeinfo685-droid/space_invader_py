from src.domain.game_state import GameConfig, GameState
from src.infrastructure.pygame_infrastructure import (
    PygameGameLoopAdapter,
    PygameInputAdapter,
    PygameOutputAdapter,
)
from src.use_cases.game_engine import GameEngine


def main() -> None:
    config = GameConfig()
    state = GameState(config)
    engine = GameEngine(state)
    engine.create_enemies()

    input_adapter = PygameInputAdapter(state, engine)
    output_adapter = PygameOutputAdapter(state)
    game_loop = PygameGameLoopAdapter(input_adapter, output_adapter, engine)
    game_loop.run()


if __name__ == "__main__":
    main()
