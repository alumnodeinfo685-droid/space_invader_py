from src.domain.game_state import GameConfig, GameState
from src.use_cases.game_engine import GameEngine
from src.adapters.pygame_adapter import PygameAdapter


def main() -> None:
    config = GameConfig()
    state = GameState(config)
    engine = GameEngine(state)
    engine.create_enemies()
    adapter = PygameAdapter(state, engine)
    adapter.run()


if __name__ == "__main__":
    main()
