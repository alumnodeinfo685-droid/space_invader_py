
from random import choice

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
        if len(self.state.player_bullets) < self.state.config.MAX_BULLETS:
            player_rect = self.state.player.rect
            bullet_x = player_rect.x + (player_rect.width - self.state.config.BULLET_WIDTH) // 2
            bullet_y = player_rect.y
            self.state.player_bullets.append(
                Bullet(bullet_x, bullet_y, self.state.config.BULLET_WIDTH, self.state.config.BULLET_HEIGHT, self.state.config.PLAYER_BULLET_SPEED)
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
        self.state.player_bullets.clear()
        self.state.enemy_bullets.clear()
        self.create_enemies()
        self.state.score = 0
        self.state.enemy_direction_x = self.state.config.ENEMY_DIRECTION_X
        self.state.enemy_last_shot_time_ms = 0
        self.state.enemy_next_shot_delay_ms = self._random_enemy_shot_delay()
        self.state.game_over = False
        self.state.victory = False
        self.state.paused = False

    def update(self, move_direction: int, current_time_ms: int) -> None:
        if self.state.game_over or self.state.victory or self.state.paused:
            return

        self.state.player.move(move_direction)

        for bullet in self.state.player_bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.state.player_bullets.remove(bullet)

        for bullet in self.state.enemy_bullets[:]:
            bullet.update()
            if bullet.rect.top > self.state.config.SCREEN_HEIGHT:
                self.state.enemy_bullets.remove(bullet)

        self._move_enemies()
        self._enemy_shoot(current_time_ms)
        self._resolve_collisions()

        if not self.state.enemies:
            self.state.victory = True

    def _move_enemies(self) -> None:
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

    def _enemy_shoot(self, current_time_ms: int) -> None:
        if current_time_ms - self.state.enemy_last_shot_time_ms < self.state.enemy_next_shot_delay_ms:
            return

        if not self.state.enemies:
            return

        # Agrupa al menos un enemigo por columna y elige uno entre los más abajo
        bottom_enemies = self._bottom_enemies_by_column()
        if not bottom_enemies:
            return

        shooter = choice(bottom_enemies)
        self.state.enemy_last_shot_time_ms = current_time_ms
        self.state.enemy_next_shot_delay_ms = self._random_enemy_shot_delay()
        bullet_x = shooter.rect.x + (shooter.rect.width - self.state.config.BULLET_WIDTH) // 2
        bullet_y = shooter.rect.y + shooter.rect.height
        self.state.enemy_bullets.append(
            Bullet(bullet_x, bullet_y, self.state.config.BULLET_WIDTH, self.state.config.BULLET_HEIGHT, self.state.config.ENEMY_BULLET_SPEED)
        )

    def _random_enemy_shot_delay(self) -> int:
        return choice(range(self.state.config.ENEMY_SHOOT_INTERVAL_MIN_MS, self.state.config.ENEMY_SHOOT_INTERVAL_MAX_MS + 1))

    def _bottom_enemies_by_column(self) -> list[Enemy]:
        columns: dict[int, Enemy] = {}
        for enemy in self.state.enemies:
            column_index = enemy.rect.x // self.state.config.ENEMY_SPACING_X
            existing = columns.get(column_index)
            if existing is None or enemy.rect.y > existing.rect.y:
                columns[column_index] = enemy
        return list(columns.values())

    def _resolve_collisions(self) -> None:
        for bullet in self.state.player_bullets[:]:
            for enemy in self.state.enemies[:]:
                if bullet.rect.intersects(enemy.rect):
                    self.state.player_bullets.remove(bullet)
                    self.state.enemies.remove(enemy)
                    self.state.score += 10
                    break

        for bullet in self.state.enemy_bullets[:]:
            if bullet.rect.intersects(self.state.player.rect):
                self.state.enemy_bullets.remove(bullet)
                self.state.game_over = True
                return
