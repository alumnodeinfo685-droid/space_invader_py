
from src.domain.entities import Bullet, Enemy, Player
from src.domain.game_state import GameState


class GameEngine:
    def __init__(self, state: GameState) -> None:
        self.state = state

    def create_enemies(self) -> None:
        self.state.enemies.clear()
        for row in range(self.state.config.ENEMY_ROWS):
            for col in range(self.state.config.ENEMY_COLS):
                x = self.state.config.ENEMY_START_X + col * self.state.config.ENEMY_SPACING_X
                y = self.state.config.ENEMY_START_Y + row * self.state.config.ENEMY_SPACING_Y
                self.state.enemies.append(
                    Enemy(x, y, self.state.config.ENEMY_WIDTH, self.state.config.ENEMY_HEIGHT)
                )

    def shoot(self) -> None:
        if len(self.state.bullets) < self.state.config.MAX_BULLETS:
            player_rect = self.state.player.rect
            bullet_x = player_rect.x + (player_rect.width - self.state.config.BULLET_WIDTH) // 2
            bullet_y = player_rect.y
            self.state.bullets.append(
                Bullet(bullet_x, bullet_y, self.state.config.BULLET_WIDTH, self.state.config.BULLET_HEIGHT, self.state.config.BULLET_SPEED)
            )

    def reset(self) -> None:
        self.state.player = Player(
            (self.state.config.SCREEN_WIDTH - self.state.config.PLAYER_WIDTH) // 2,
            self.state.config.SCREEN_HEIGHT - 50,
            self.state.config.PLAYER_WIDTH,
            self.state.config.PLAYER_HEIGHT,
            self.state.config.PLAYER_SPEED,
            self.state.config.SCREEN_WIDTH,
        )
        self.state.bullets.clear()
        self.create_enemies()
        self.state.score = 0
        self.state.enemy_direction_x = self.state.config.ENEMY_DIRECTION_X
        self.state.game_over = False
        self.state.victory = False
        self.state.paused = False

    def update(self, move_direction: int) -> None:
        if self.state.game_over or self.state.victory or self.state.paused:
            return

        self.state.player.move(move_direction)

        for bullet in self.state.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.state.bullets.remove(bullet)

        move_down = False
        for enemy in self.state.enemies:
            if enemy.rect.right >= self.state.config.SCREEN_WIDTH or enemy.rect.left <= 0:
                move_down = True
                break

        if move_down:
            self.state.enemy_direction_x *= -1
            current_drop = self.state.enemy_drop_y
        else:
            current_drop = 0

        for enemy in self.state.enemies:
            enemy.move(self.state.enemy_direction_x, current_drop)
            if enemy.rect.bottom >= self.state.player.rect.top or enemy.rect.intersects(self.state.player.rect):
                self.state.game_over = True

        for bullet in self.state.bullets[:]:
            for enemy in self.state.enemies[:]:
                if bullet.rect.intersects(enemy.rect):
                    self.state.bullets.remove(bullet)
                    self.state.enemies.remove(enemy)
                    self.state.score += 10
                    break

        if not self.state.enemies:
            self.state.victory = True
