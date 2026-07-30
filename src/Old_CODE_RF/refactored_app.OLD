from enum import Enum, auto
from pathlib import Path

import pygame

from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player
from maze_muncher.renderer import (
    TILE_SIZE,
    draw_game,
    draw_game_over_screen,
    draw_life_lost_screen,
    draw_menu,
    draw_win_screen,
)


FPS = 60
LIFE_LOST_DISPLAY_MS = 900
GAME_OVER_MUSIC_DELAY_MS = 1200
ENEMY_MOVE_INTERVAL_MS = 400

ENEMY_MOVE_EVENT = pygame.USEREVENT + 1


MENU_MUSIC = Path("assets/audio/menu_theme.mp3")
GAME_OVER_MUSIC = Path("assets/audio/gameover_theme.mp3")

ENEMY_MOVE_SFX = Path("assets/audio/sfx/enemy_move.mp3")
GAME_OVER_SFX = Path("assets/audio/sfx/game_over.mp3")
LIFE_LOST_SFX = Path("assets/audio/sfx/life_lost.mp3")
MEANIE_SPAWN_SFX = Path("assets/audio/sfx/meanie_spawn.mp3")
PICKUP_SFX = Path("assets/audio/sfx/pickup_sound.mp3")
PLAYER_START_SFX = Path("assets/audio/sfx/player_start.mp3")
VICTORY_SFX = Path("assets/audio/sfx/victory_sound.mp3")
POWER_PELLET_SFX = Path("assets/audio/sfx/power_pellet.mp3")
ENEMY_EATEN_SFX = Path("assets/audio/sfx/enemy_eaten.mp3")


class AppState(Enum):
    MENU = auto()
    PLAYING = auto()
    LIFE_LOST = auto()
    WON = auto()
    GAME_OVER = auto()


class MenuAction(Enum):
    START = auto()
    QUIT = auto()


class EndScreenAction(Enum):
    REPLAY = auto()
    MENU = auto()


WinAction = EndScreenAction


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


def end_screen_action_for_key(
    key: int,
) -> EndScreenAction | None:
    if key in (pygame.K_RETURN, pygame.K_SPACE):
        return EndScreenAction.REPLAY

    if key == pygame.K_ESCAPE:
        return EndScreenAction.MENU

    return None


win_action_for_key = end_screen_action_for_key


def create_game() -> Game:
    board = Board(
        [
            "###############",
            "#o...........o#",
            "#.###.###.###.#",
            "#.............#",
            "#.###.#.#.###.#",
            "#.....#.#.....#",
            "#####.#.#.#####",
            "#.............#",
            "#.###.###.###.#",
            "#o...........o#",
            "###############",
        ]
    )

    return Game(
        board=board,
        player=Player(Position(1, 1)),
        enemies=[
            Enemy(Position(7, 7)),
            Enemy(Position(3, 13)),
        ],
    )


def load_sound(path: Path) -> pygame.mixer.Sound | None:
    if not path.exists():
        return None

    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None


def play_sound(sound: pygame.mixer.Sound | None) -> None:
    if sound is not None:
        sound.play()


def start_music(path: Path) -> None:
    if not path.exists():
        return

    try:
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def stop_music() -> None:
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass


def start_menu_music() -> None:
    start_music(MENU_MUSIC)


def start_game_over_music() -> None:
    start_music(GAME_OVER_MUSIC)


def main() -> None:
    pygame.init()

    game = create_game()

    screen = pygame.display.set_mode(
        (
            game.board.width * TILE_SIZE,
            game.board.height * TILE_SIZE,
        )
    )

    title_font = pygame.font.Font(None, 48)
    menu_font = pygame.font.Font(None, 26)
    hud_font = pygame.font.Font(None, 22)

    enemy_move_sound = load_sound(ENEMY_MOVE_SFX)
    game_over_sound = load_sound(GAME_OVER_SFX)
    life_lost_sound = load_sound(LIFE_LOST_SFX)
    meanie_spawn_sound = load_sound(MEANIE_SPAWN_SFX)
    pickup_sound = load_sound(PICKUP_SFX)
    player_start_sound = load_sound(PLAYER_START_SFX)
    victory_sound = load_sound(VICTORY_SFX)
    power_pellet_sound = load_sound(POWER_PELLET_SFX)
    enemy_eaten_sound = load_sound(ENEMY_EATEN_SFX)

    pygame.time.set_timer(
        ENEMY_MOVE_EVENT,
        ENEMY_MOVE_INTERVAL_MS,
    )

    clock = pygame.time.Clock()
    app_state = AppState.MENU

    life_lost_until = 0
    game_over_music_starts_at = 0
    game_over_music_started = False

    running = True

    start_menu_music()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == ENEMY_MOVE_EVENT:
                if app_state is not AppState.PLAYING:
                    continue

                previous_score = game.score
                previous_lives = game.lives

                moved = game.move_enemy()

                if not moved:
                    continue

                if game.state is GameState.GAME_OVER:
                    stop_music()
                    play_sound(game_over_sound)

                    app_state = AppState.GAME_OVER
                    game_over_music_starts_at = (
                        pygame.time.get_ticks()
                        + GAME_OVER_MUSIC_DELAY_MS
                    )
                    game_over_music_started = False

                elif game.lives < previous_lives:
                    play_sound(life_lost_sound)

                    app_state = AppState.LIFE_LOST
                    life_lost_until = (
                        pygame.time.get_ticks()
                        + LIFE_LOST_DISPLAY_MS
                    )

                else:
                    score_gained = game.score - previous_score

                    if score_gained >= Game.ENEMY_SCORE:
                        play_sound(enemy_eaten_sound)
                    else:
                        play_sound(enemy_move_sound)

                continue

            if event.type != pygame.KEYDOWN:
                continue

            if app_state is AppState.MENU:
                action = menu_action_for_key(event.key)

                if action is MenuAction.START:
                    stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING

                    play_sound(player_start_sound)
                    play_sound(meanie_spawn_sound)

                elif action is MenuAction.QUIT:
                    running = False

            elif app_state is AppState.PLAYING:
                direction = direction_for_key(event.key)

                if direction is None:
                    continue

                previous_score = game.score
                previous_lives = game.lives

                moved = game.move_player(direction)

                if not moved:
                    continue

                if game.state is GameState.GAME_OVER:
                    stop_music()
                    play_sound(game_over_sound)

                    app_state = AppState.GAME_OVER
                    game_over_music_starts_at = (
                        pygame.time.get_ticks()
                        + GAME_OVER_MUSIC_DELAY_MS
                    )
                    game_over_music_started = False

                elif game.lives < previous_lives:
                    play_sound(life_lost_sound)

                    app_state = AppState.LIFE_LOST
                    life_lost_until = (
                        pygame.time.get_ticks()
                        + LIFE_LOST_DISPLAY_MS
                    )

                else:
                    score_gained = game.score - previous_score

                    if score_gained >= Game.ENEMY_SCORE:
                        play_sound(enemy_eaten_sound)
                    elif score_gained == Game.POWER_PELLET_SCORE:
                        play_sound(power_pellet_sound)
                    elif score_gained > 0:
                        play_sound(pickup_sound)

                    if game.state is GameState.WON:
                        stop_music()
                        play_sound(victory_sound)
                        app_state = AppState.WON

            elif app_state in (
                AppState.WON,
                AppState.GAME_OVER,
            ):
                action = end_screen_action_for_key(event.key)

                if action is EndScreenAction.REPLAY:
                    stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING
                    game_over_music_started = False

                    play_sound(player_start_sound)
                    play_sound(meanie_spawn_sound)

                elif action is EndScreenAction.MENU:
                    stop_music()

                    game = create_game()
                    app_state = AppState.MENU
                    game_over_music_started = False

                    start_menu_music()

        current_time = pygame.time.get_ticks()

        if (
            app_state is AppState.LIFE_LOST
            and current_time >= life_lost_until
        ):
            app_state = AppState.PLAYING

        if (
            app_state is AppState.GAME_OVER
            and not game_over_music_started
            and current_time >= game_over_music_starts_at
        ):
            start_game_over_music()
            game_over_music_started = True

        if app_state is AppState.MENU:
            draw_menu(
                screen,
                title_font,
                menu_font,
            )
            pygame.display.set_caption("Maze Muncher")

        elif app_state is AppState.PLAYING:
            draw_game(
                screen,
                game,
                hud_font,
            )
            pygame.display.set_caption(
                f"Maze Muncher "
                f"| Score: {game.score} "
                f"| Lives: {game.lives}"
            )

        elif app_state is AppState.LIFE_LOST:
            draw_life_lost_screen(
                screen,
                game,
                title_font,
                menu_font,
                hud_font,
            )
            pygame.display.set_caption(
                f"Maze Muncher "
                f"| Life Lost "
                f"| Lives: {game.lives}"
            )

        elif app_state is AppState.WON:
            draw_win_screen(
                screen,
                game,
                title_font,
                menu_font,
            )
            pygame.display.set_caption(
                f"Maze Muncher "
                f"| You Won "
                f"| Final Score: {game.score}"
            )

        elif app_state is AppState.GAME_OVER:
            draw_game_over_screen(
                screen,
                game,
                title_font,
                menu_font,
            )
            pygame.display.set_caption(
                f"Maze Muncher "
                f"| Game Over "
                f"| Final Score: {game.score}"
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.time.set_timer(ENEMY_MOVE_EVENT, 0)
    stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
    
    