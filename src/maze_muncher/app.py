from enum import Enum, auto
from pathlib import Path

import pygame

from maze_muncher.board import Board, Position
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


TILE_SIZE = 32
FPS = 60

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (30, 70, 220)
PELLET_COLOR = (240, 240, 200)
PLAYER_COLOR = (255, 220, 0)
TEXT_COLOR = (255, 255, 255)

MENU_MUSIC = Path("assets/audio/menu_theme.mp3")


class AppState(Enum):
    MENU = auto()
    PLAYING = auto()


class MenuAction(Enum):
    START = auto()
    QUIT = auto()


def direction_for_key(key: int) -> Direction | None:
    return {
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT,
    }.get(key)


def menu_action_for_key(key: int) -> MenuAction | None:
    if key in (pygame.K_RETURN, pygame.K_SPACE):
        return MenuAction.START

    if key == pygame.K_ESCAPE:
        return MenuAction.QUIT

    return None


def create_game() -> Game:
    board = Board(
        [
            "###############",
            "#.............#",
            "#.###.###.###.#",
            "#.............#",
            "#.###.#.#.###.#",
            "#.....#.#.....#",
            "#####.#.#.#####",
            "#.............#",
            "#.###.###.###.#",
            "#.............#",
            "###############",
        ]
    )

    return Game(
        board=board,
        player=Player(Position(1, 1)),
    )


def draw_game(screen: pygame.Surface, game: Game) -> None:
    screen.fill(BACKGROUND_COLOR)

    for row in range(game.board.height):
        for column in range(game.board.width):
            position = Position(row, column)
            x = column * TILE_SIZE
            y = row * TILE_SIZE

            if game.board.is_wall(position):
                pygame.draw.rect(
                    screen,
                    WALL_COLOR,
                    pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                )
            elif game.board.has_pellet(position):
                pygame.draw.circle(
                    screen,
                    PELLET_COLOR,
                    (
                        x + TILE_SIZE // 2,
                        y + TILE_SIZE // 2,
                    ),
                    3,
                )

    player_x = game.player.position.column * TILE_SIZE
    player_y = game.player.position.row * TILE_SIZE

    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        (
            player_x + TILE_SIZE // 2,
            player_y + TILE_SIZE // 2,
        ),
        TILE_SIZE // 2 - 3,
    )


def draw_menu(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
) -> None:
    screen.fill(BACKGROUND_COLOR)

    title = title_font.render("MAZE MUNCHER", True, PLAYER_COLOR)
    start = menu_font.render("ENTER OR SPACE TO START", True, TEXT_COLOR)
    quit_text = menu_font.render("ESC TO QUIT", True, TEXT_COLOR)

    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
    start_rect = start.get_rect(center=(screen.get_width() // 2, 190))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, 230))

    screen.blit(title, title_rect)
    screen.blit(start, start_rect)
    screen.blit(quit_text, quit_rect)


def start_menu_music() -> None:
    if not MENU_MUSIC.exists():
        return

    try:
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def main() -> None:
    pygame.init()

    game = create_game()

    screen = pygame.display.set_mode(
        (
            game.board.width * TILE_SIZE,
            game.board.height * TILE_SIZE,
        )
    )

    pygame.display.set_caption("Maze Muncher")

    title_font = pygame.font.Font(None, 48)
    menu_font = pygame.font.Font(None, 26)

    clock = pygame.time.Clock()
    app_state = AppState.MENU
    running = True

    start_menu_music()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue

            if app_state is AppState.MENU:
                action = menu_action_for_key(event.key)

                if action is MenuAction.START:
                    pygame.mixer.music.stop()
                    app_state = AppState.PLAYING

                elif action is MenuAction.QUIT:
                    running = False

            elif app_state is AppState.PLAYING:
                direction = direction_for_key(event.key)

                if direction is not None:
                    game.move_player(direction)

        if app_state is AppState.MENU:
            draw_menu(screen, title_font, menu_font)
            pygame.display.set_caption("Maze Muncher")

        else:
            draw_game(screen, game)

            caption = f"Maze Muncher | Score: {game.score}"

            if game.state is GameState.WON:
                caption += " | YOU WON"

            pygame.display.set_caption(caption)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

