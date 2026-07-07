from typing import List

from .entities import Bullet, Enemy, Player


class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 30
    PLAYER_SPEED = 6
    ENEMY_WIDTH = 40
    ENEMY_HEIGHT = 30
    ENEMY_ROWS = 5
    ENEMY_COLS = 8
    ENEMY_START_X = 80
    ENEMY_START_Y = 50
    ENEMY_SPACING_X = 80
    ENEMY_SPACING_Y = 50
    ENEMY_DIRECTION_X = 2
    ENEMY_DROP_Y = 15
    MAX_BULLETS = 4
    BULLET_WIDTH = 6
    BULLET_HEIGHT = 15
    BULLET_SPEED = -8


class GameState:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.player = Player(
            (config.SCREEN_WIDTH - config.PLAYER_WIDTH) // 2,
            config.SCREEN_HEIGHT - 50,
            config.PLAYER_WIDTH,
            config.PLAYER_HEIGHT,
            config.PLAYER_SPEED,
            config.SCREEN_WIDTH,
        )
        self.bullets: List[Bullet] = []
        self.enemies: List[Enemy] = []
        self.score = 0
        self.enemy_direction_x = config.ENEMY_DIRECTION_X
        self.enemy_drop_y = config.ENEMY_DROP_Y
        self.game_over = False
        self.victory = False
        self.paused = False
