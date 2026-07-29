from enum import Enum, auto
from pathlib import Path

import pygame

from maze_muncher.board import Board, Position
from maze_muncher.enemy import Enemy
from maze_muncher.game import Game, GameState
from maze_muncher.movement import Direction
from maze_muncher.player import Player


TILE_SIZE = 32
FPS = 60
LIFE_LOST_DISPLAY_MS = 900
GAME_OVER_MUSIC_DELAY_MS = 1200

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (30, 70, 220)
PELLET_COLOR = (240, 240, 200)
PLAYER_COLOR = (255, 220, 0)
TEXT_COLOR = (255, 255, 255)
ENEMY_COLOR = (255, 60, 80)

MENU_MUSIC = Path("assets/audio/menu_theme.mp3")
GAME_OVER_MUSIC = Path("assets/audio/gameover_theme.mp3")

ENEMY_MOVE_SFX = Path("assets/audio/sfx/enemy_move.mp3")
GAME_OVER_SFX = Path("assets/audio/sfx/game_over.mp3")
LIFE_LOST_SFX = Path("assets/audio/sfx/life_lost.mp3")
MEANIE_SPAWN_SFX = Path("assets/audio/sfx/meanie_spawn.mp3")
PICKUP_SFX = Path("assets/audio/sfx/pickup_sound.mp3")
PLAYER_START_SFX = Path("assets/audio/sfx/player_start.mp3")
VICTORY_SFX = Path("assets/audio/sfx/victory_sound.mp3")


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
        enemy=Enemy(Position(7, 7)),
    )


def load_sound(path: Path) -> pygame.mixer.Sound | None:
    if not path.exists():
        return None

    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None


def play_sound(
    sound: pygame.mixer.Sound | None,
) -> None:
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


def draw_game(
    screen: pygame.Surface,
    game: Game,
) -> None:
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
                    pygame.Rect(
                        x,
                        y,
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
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

    player_x = (
        game.player.position.column * TILE_SIZE
    )
    player_y = (
        game.player.position.row * TILE_SIZE
    )

    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        (
            player_x + TILE_SIZE // 2,
            player_y + TILE_SIZE // 2,
        ),
        TILE_SIZE // 2 - 3,
    )

    if game.enemy is not None:
        enemy_x = (
            game.enemy.position.column * TILE_SIZE
        )
        enemy_y = (
            game.enemy.position.row * TILE_SIZE
        )

        pygame.draw.circle(
            screen,
            ENEMY_COLOR,
            (
                enemy_x + TILE_SIZE // 2,
                enemy_y + TILE_SIZE // 2,
            ),
            TILE_SIZE // 2 - 4,
        )


def draw_menu(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
) -> None:
    screen.fill(BACKGROUND_COLOR)

    title = title_font.render(
        "MAZE MUNCHER",
        True,
        PLAYER_COLOR,
    )
    start = menu_font.render(
        "ENTER OR SPACE TO START",
        True,
        TEXT_COLOR,
    )
    quit_text = menu_font.render(
        "ESC TO QUIT",
        True,
        TEXT_COLOR,
    )

    center_x = screen.get_width() // 2

    screen.blit(
        title,
        title.get_rect(
            center=(center_x, 100)
        ),
    )
    screen.blit(
        start,
        start.get_rect(
            center=(center_x, 190)
        ),
    )
    screen.blit(
        quit_text,
        quit_text.get_rect(
            center=(center_x, 230)
        ),
    )


def draw_life_lost_screen(
    screen: pygame.Surface,
    game: Game,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
) -> None:
    draw_game(screen, game)

    overlay = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA,
    )
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title = title_font.render(
        "LIFE LOST!",
        True,
        ENEMY_COLOR,
    )
    lives = menu_font.render(
        f"LIVES REMAINING: {game.lives}",
        True,
        TEXT_COLOR,
    )

    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2

    screen.blit(
        title,
        title.get_rect(
            center=(
                center_x,
                center_y - 25,
            )
        ),
    )
    screen.blit(
        lives,
        lives.get_rect(
            center=(
                center_x,
                center_y + 25,
            )
        ),
    )


def draw_end_screen(
    screen: pygame.Surface,
    game: Game,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
    title_text: str,
    title_color: tuple[int, int, int],
) -> None:
    screen.fill(BACKGROUND_COLOR)

    title = title_font.render(
        title_text,
        True,
        title_color,
    )
    score = menu_font.render(
        f"FINAL SCORE: {game.score}",
        True,
        TEXT_COLOR,
    )
    replay = menu_font.render(
        "ENTER OR SPACE TO PLAY AGAIN",
        True,
        TEXT_COLOR,
    )
    menu = menu_font.render(
        "ESC TO RETURN TO MENU",
        True,
        TEXT_COLOR,
    )

    center_x = screen.get_width() // 2

    screen.blit(
        title,
        title.get_rect(
            center=(center_x, 90)
        ),
    )
    screen.blit(
        score,
        score.get_rect(
            center=(center_x, 155)
        ),
    )
    screen.blit(
        replay,
        replay.get_rect(
            center=(center_x, 215)
        ),
    )
    screen.blit(
        menu,
        menu.get_rect(
            center=(center_x, 255)
        ),
    )


def draw_win_screen(
    screen: pygame.Surface,
    game: Game,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
) -> None:
    draw_end_screen(
        screen=screen,
        game=game,
        title_font=title_font,
        menu_font=menu_font,
        title_text="YOU WON!",
        title_color=PLAYER_COLOR,
    )


def draw_game_over_screen(
    screen: pygame.Surface,
    game: Game,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
) -> None:
    draw_end_screen(
        screen=screen,
        game=game,
        title_font=title_font,
        menu_font=menu_font,
        title_text="GAME OVER",
        title_color=ENEMY_COLOR,
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

    enemy_move_sound = load_sound(
        ENEMY_MOVE_SFX
    )
    game_over_sound = load_sound(
        GAME_OVER_SFX
    )
    life_lost_sound = load_sound(
        LIFE_LOST_SFX
    )
    meanie_spawn_sound = load_sound(
        MEANIE_SPAWN_SFX
    )
    pickup_sound = load_sound(
        PICKUP_SFX
    )
    player_start_sound = load_sound(
        PLAYER_START_SFX
    )
    victory_sound = load_sound(
        VICTORY_SFX
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

            if event.type != pygame.KEYDOWN:
                continue

            if app_state is AppState.MENU:
                action = menu_action_for_key(
                    event.key
                )

                if action is MenuAction.START:
                    stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING

                    play_sound(
                        player_start_sound
                    )
                    play_sound(
                        meanie_spawn_sound
                    )

                elif action is MenuAction.QUIT:
                    running = False

            elif app_state is AppState.PLAYING:
                direction = direction_for_key(
                    event.key
                )

                if direction is None:
                    continue

                previous_score = game.score
                previous_lives = game.lives
                previous_enemy_position = (
                    game.enemy.position
                    if game.enemy is not None
                    else None
                )

                moved = game.move_player(
                    direction
                )

                if not moved:
                    continue

                enemy_moved = (
                    game.enemy is not None
                    and previous_enemy_position
                    is not None
                    and game.enemy.position
                    != previous_enemy_position
                )

                if (
                    game.state
                    is GameState.GAME_OVER
                ):
                    stop_music()
                    play_sound(game_over_sound)

                    app_state = (
                        AppState.GAME_OVER
                    )

                    game_over_music_starts_at = (
                        pygame.time.get_ticks()
                        + GAME_OVER_MUSIC_DELAY_MS
                    )
                    game_over_music_started = (
                        False
                    )

                elif (
                    game.lives
                    < previous_lives
                ):
                    play_sound(
                        life_lost_sound
                    )

                    app_state = (
                        AppState.LIFE_LOST
                    )
                    life_lost_until = (
                        pygame.time.get_ticks()
                        + LIFE_LOST_DISPLAY_MS
                    )

                else:
                    if game.score > previous_score:
                        play_sound(
                            pickup_sound
                        )

                    if enemy_moved:
                        play_sound(
                            enemy_move_sound
                        )

                    if (
                        game.state
                        is GameState.WON
                    ):
                        stop_music()
                        play_sound(
                            victory_sound
                        )
                        app_state = (
                            AppState.WON
                        )

            elif app_state in (
                AppState.WON,
                AppState.GAME_OVER,
            ):
                action = (
                    end_screen_action_for_key(
                        event.key
                    )
                )

                if (
                    action
                    is EndScreenAction.REPLAY
                ):
                    stop_music()

                    game = create_game()
                    app_state = AppState.PLAYING
                    game_over_music_started = False

                    play_sound(
                        player_start_sound
                    )
                    play_sound(
                        meanie_spawn_sound
                    )

                elif (
                    action
                    is EndScreenAction.MENU
                ):
                    stop_music()

                    game = create_game()
                    app_state = AppState.MENU
                    game_over_music_started = False

                    start_menu_music()

        current_time = pygame.time.get_ticks()

        if (
            app_state is AppState.LIFE_LOST
            and current_time
            >= life_lost_until
        ):
            app_state = AppState.PLAYING

        if (
            app_state is AppState.GAME_OVER
            and not game_over_music_started
            and current_time
            >= game_over_music_starts_at
        ):
            start_game_over_music()
            game_over_music_started = True

        if app_state is AppState.MENU:
            draw_menu(
                screen,
                title_font,
                menu_font,
            )
            pygame.display.set_caption(
                "Maze Muncher"
            )

        elif app_state is AppState.PLAYING:
            draw_game(
                screen,
                game,
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

    stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
    