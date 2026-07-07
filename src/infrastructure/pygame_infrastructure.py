import pygame
import sys
from typing import Optional

from src.adapters.interfaces import GameInputAdapter, GameOutputAdapter, GameLoopAdapter
from src.domain.game_state import GameState
from src.use_cases.game_engine import GameEngine


class PygameInputAdapter(GameInputAdapter):
    def __init__(self, state: GameState, engine: GameEngine) -> None:
        self.state = state
        self.engine = engine

    def handle_input(self, state: GameState) -> int:
        move_direction = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not state.game_over and not state.victory and not state.paused:
                    self.engine.shoot()
                elif event.key == pygame.K_r and (state.game_over or state.victory):
                    self.engine.reset()
                elif event.key == pygame.K_p and not state.game_over and not state.victory:
                    state.paused = not state.paused

        keys = pygame.key.get_pressed()
        if not state.paused:
            if keys[pygame.K_LEFT]:
                move_direction = -1
            elif keys[pygame.K_RIGHT]:
                move_direction = 1

        return move_direction


class PygameOutputAdapter(GameOutputAdapter):
    def __init__(self, state: GameState) -> None:
        self.state = state
        self._initialize_pygame()

    def _initialize_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.state.config.SCREEN_WIDTH, self.state.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders Clon")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, state: GameState) -> None:
        self.screen.fill((0, 0, 0))
        self._draw_player(state)
        self._draw_bullets(state)
        self._draw_enemies(state)
        self._draw_score(state)
        self._draw_status_message(state)
        pygame.display.flip()
        self.clock.tick(60)

    def _draw_player(self, state: GameState) -> None:
        rect = state.player.rect
        pygame.draw.rect(self.screen, (0, 255, 0), (rect.x, rect.y, rect.width, rect.height))
        pygame.draw.rect(self.screen, (0, 255, 0), (rect.x + rect.width // 2 - 5, rect.y - 10, 10, 10))

    def _draw_bullets(self, state: GameState) -> None:
        for bullet in state.bullets:
            rect = bullet.rect
            pygame.draw.rect(self.screen, (255, 255, 0), (rect.x, rect.y, rect.width, rect.height))

    def _draw_enemies(self, state: GameState) -> None:
        for enemy in state.enemies:
            rect = enemy.rect
            pygame.draw.rect(self.screen, (255, 50, 50), (rect.x, rect.y, rect.width, rect.height))
            pygame.draw.rect(self.screen, (255, 255, 255), (rect.x + 8, rect.y + 8, 6, 6))
            pygame.draw.rect(self.screen, (255, 255, 255), (rect.x + rect.width - 14, rect.y + 8, 6, 6))

    def _draw_score(self, state: GameState) -> None:
        score_text = self.font.render(f"Puntaje: {state.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def _draw_status_message(self, state: GameState) -> None:
        if state.game_over:
            self._render_text("¡GAME OVER! Presiona 'R' para reiniciar", (255, 50, 50))
        elif state.victory:
            self._render_text("¡VICTORIA! Presiona 'R' para jugar de nuevo", (0, 255, 0))
        elif state.paused:
            self._render_text("PAUSA - Presiona 'P' para continuar", (255, 255, 0))

    def _render_text(self, text: str, color: tuple[int, int, int]) -> None:
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (self.state.config.SCREEN_WIDTH // 2 - rendered.get_width() // 2, self.state.config.SCREEN_HEIGHT // 2))


class PygameGameLoopAdapter(GameLoopAdapter):
    def __init__(self, input_adapter: GameInputAdapter, output_adapter: GameOutputAdapter, engine: GameEngine) -> None:
        self.input_adapter = input_adapter
        self.output_adapter = output_adapter
        self.engine = engine

    def run(self) -> None:
        while True:
            move_direction = self.input_adapter.handle_input(self.engine.state)
            self.engine.update(move_direction)
            self.output_adapter.draw(self.engine.state)
