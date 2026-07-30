from enum import Enum, auto

import pygame

from maze_muncher.audio import AudioManager
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
    draw_pause_screen,
)


FPS = 60
LIFE_LOST_DISPLAY_MS = 900
GAME_OVER_MUSIC_DELAY_MS = 1200
ENEMY_MOVE_INTERVAL_MS = 400

ENEMY_MOVE_EVENT = pygame.USEREVENT + 1


class AppState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LIFE_LOST = auto()
    WON = auto()
    GAME_OVER = auto()


class MenuAction(Enum):
    START = auto()
    QUIT = auto()


class EndScreenAction(Enum):
    REPLAY = auto()
    MENU = auto()


class PauseOption(Enum):
    MUSIC = auto()
    SFX = auto()


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

    audio = AudioManager.load()

    pygame.time.set_timer(
        ENEMY_MOVE_EVENT,
        ENEMY_MOVE_INTERVAL_MS,
    )

    clock = pygame.time.Clock()
    app_state = AppState.MENU

    life_lost_until = 0
    game_over_music_starts_at = 0
    game_over_music_started = False

    skip_frightened_move = False

    pause_option = PauseOption.MUSIC

    running = True

    audio.start_menu_music()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == ENEMY_MOVE_EVENT:
                if app_state is not AppState.PLAYING:
                    continue

                if game.is_powered_up:
                    skip_frightened_move = not skip_frightened_move

                    if skip_frightened_move:
                        continue
                else:
                    skip_frightened_move = False

                previous_score = game.score
                previous_lives = game.lives

                moved = game.move_enemy()

                if not moved:
                    continue

                if game.state is GameState.GAME_OVER:
                    audio.stop_music()
                    audio.play(audio.game_over)

                    app_state = AppState.GAME_OVER
                    game_over_music_starts_at = (
                        pygame.time.get_ticks()
                        + GAME_OVER_MUSIC_DELAY_MS
                    )
                    game_over_music_started = False

                elif game.lives < previous_lives:
                    audio.play(audio.life_lost)

                    app_state = AppState.LIFE_LOST
                    life_lost_until = (
                        pygame.time.get_ticks()
                        + LIFE_LOST_DISPLAY_MS
                    )

                else:
                    audio.play_score_gain(
                        game.score - previous_score,
                        enemy_move=True,
                    )

                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_m:
                audio.toggle_mute()
                continue

            if app_state is AppState.MENU:
                action = menu_action_for_key(event.key)

                if action is MenuAction.START:
                    audio.stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING

                    audio.play_game_start()

                elif action is MenuAction.QUIT:
                    running = False


            elif app_state is AppState.PLAYING:
                if event.key in (
                        pygame.K_p,
                        pygame.K_ESCAPE,
                ):
                    app_state = AppState.PAUSED
                    continue

                direction = direction_for_key(event.key)

                if direction is None:
                    continue

                previous_score = game.score
                previous_lives = game.lives

                moved = game.move_player(direction)

                if not moved:
                    continue

                if game.state is GameState.GAME_OVER:
                    audio.stop_music()
                    audio.play(audio.game_over)

                    app_state = AppState.GAME_OVER
                    game_over_music_starts_at = (
                        pygame.time.get_ticks()
                        + GAME_OVER_MUSIC_DELAY_MS
                    )
                    game_over_music_started = False

                elif game.lives < previous_lives:
                    audio.play(audio.life_lost)

                    app_state = AppState.LIFE_LOST
                    life_lost_until = (
                        pygame.time.get_ticks()
                        + LIFE_LOST_DISPLAY_MS
                    )

                else:
                    audio.play_score_gain(
                        game.score - previous_score
                    )

                    if game.state is GameState.WON:
                        audio.stop_music()
                        audio.play(audio.victory)
                        app_state = AppState.WON


            elif app_state is AppState.PAUSED:
                if event.key in (
                        pygame.K_p,
                        pygame.K_ESCAPE,
                ):
                    app_state = AppState.PLAYING
                    continue

                if event.key in (
                        pygame.K_UP,
                        pygame.K_DOWN,
                ):
                    pause_option = (
                        PauseOption.SFX
                        if pause_option is PauseOption.MUSIC
                        else PauseOption.MUSIC
                    )
                    continue

                if event.key not in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                ):
                    continue

                volume_change = (
                    0.1
                    if event.key == pygame.K_RIGHT
                    else -0.1
                )

                if pause_option is PauseOption.MUSIC:
                    audio.set_music_volume(
                        audio.music_volume + volume_change
                    )
                else:
                    audio.set_sfx_volume(
                        audio.sfx_volume + volume_change
                    )

            elif app_state in (
                AppState.WON,
                AppState.GAME_OVER,
            ):
                action = end_screen_action_for_key(
                    event.key
                )

                if action is EndScreenAction.REPLAY:
                    audio.stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING
                    game_over_music_started = False

                    audio.play_game_start()

                elif action is EndScreenAction.MENU:
                    audio.stop_music()

                    game = create_game()
                    app_state = AppState.MENU
                    game_over_music_started = False

                    audio.start_menu_music()

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
            audio.start_game_over_music()
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

        elif app_state is AppState.PAUSED:
            draw_pause_screen(
                screen,
                game,
                title_font,
                menu_font,
                hud_font,
                audio.music_volume,
                audio.sfx_volume,
                pause_option.name,
            )
            pygame.display.set_caption(
                "Maze Muncher | Paused"
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
    audio.stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
    