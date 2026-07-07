import pygame
import sys
from typing import Optional

from src.domain.game_state import GameState
from src.use_cases.game_engine import GameEngine


class PygameAdapter:
    def __init__(self, state: GameState, engine: GameEngine) -> None:
        self.state = state
        self.engine = engine
        self.config = state.config
        self._initialize_pygame()

    def _initialize_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders Clon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def _render_text(self, text: str, color: tuple[int, int, int]) -> None:
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (self.config.SCREEN_WIDTH // 2 - rendered.get_width() // 2, self.config.SCREEN_HEIGHT // 2))

    def _draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self._draw_player()
        self._draw_bullets()
        self._draw_enemies()
        self._draw_score()
        self._draw_status_message()
        pygame.display.flip()

    def _draw_player(self) -> None:
        rect = self.state.player.rect
        pygame.draw.rect(self.screen, (0, 255, 0), (rect.x, rect.y, rect.width, rect.height))
        pygame.draw.rect(self.screen, (0, 255, 0), (rect.x + rect.width // 2 - 5, rect.y - 10, 10, 10))

    def _draw_bullets(self) -> None:
        for bullet in self.state.bullets:
            rect = bullet.rect
            pygame.draw.rect(self.screen, (255, 255, 0), (rect.x, rect.y, rect.width, rect.height))

    def _draw_enemies(self) -> None:
        for enemy in self.state.enemies:
            rect = enemy.rect
            pygame.draw.rect(self.screen, (255, 50, 50), (rect.x, rect.y, rect.width, rect.height))
            pygame.draw.rect(self.screen, (255, 255, 255), (rect.x + 8, rect.y + 8, 6, 6))
            pygame.draw.rect(self.screen, (255, 255, 255), (rect.x + rect.width - 14, rect.y + 8, 6, 6))

    def _draw_score(self) -> None:
        score_text = self.font.render(f"Puntaje: {self.state.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def _draw_status_message(self) -> None:
        if self.state.game_over:
            self._render_text("¡GAME OVER! Presiona 'R' para reiniciar", (255, 50, 50))
        elif self.state.victory:
            self._render_text("¡VICTORIA! Presiona 'R' para jugar de nuevo", (0, 255, 0))
        elif self.state.paused:
            self._render_text("PAUSA - Presiona 'P' para continuar", (255, 255, 0))

    def _handle_input(self) -> Optional[int]:
        move_direction = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.state.game_over and not self.state.victory and not self.state.paused:
                    self.engine.shoot()
                elif event.key == pygame.K_r and (self.state.game_over or self.state.victory):
                    self.engine.reset()
                elif event.key == pygame.K_p and not self.state.game_over and not self.state.victory:
                    self.state.paused = not self.state.paused

        keys = pygame.key.get_pressed()
        if not self.state.paused:
            if keys[pygame.K_LEFT]:
                move_direction = -1
            elif keys[pygame.K_RIGHT]:
                move_direction = 1

        return move_direction

    def run(self) -> None:
        while True:
            move_direction = self._handle_input()
            self.engine.update(move_direction)
            self._draw()
            self.clock.tick(60)
