import pygame

from maze_muncher.board import Position
from maze_muncher.game import Game


TILE_SIZE = 32

BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (30, 70, 220)
PELLET_COLOR = (240, 240, 200)
POWER_PELLET_COLOR = (255, 255, 255)
PLAYER_COLOR = (255, 220, 0)
TEXT_COLOR = (255, 255, 255)
ENEMY_COLOR = (255, 60, 80)
FRIGHTENED_ENEMY_COLOR = (70, 120, 255)


def draw_game(
    screen: pygame.Surface,
    game: Game,
    hud_font: pygame.font.Font,
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
                    pygame.Rect(x, y, TILE_SIZE, TILE_SIZE),
                )

            elif game.board.has_power_pellet(position):
                pygame.draw.circle(
                    screen,
                    POWER_PELLET_COLOR,
                    (
                        x + TILE_SIZE // 2,
                        y + TILE_SIZE // 2,
                    ),
                    7,
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

    enemy_color = (
        FRIGHTENED_ENEMY_COLOR
        if game.is_powered_up
        else ENEMY_COLOR
    )

    for enemy in game.enemies:
        enemy_x = enemy.position.column * TILE_SIZE
        enemy_y = enemy.position.row * TILE_SIZE

        pygame.draw.circle(
            screen,
            enemy_color,
            (
                enemy_x + TILE_SIZE // 2,
                enemy_y + TILE_SIZE // 2,
            ),
            TILE_SIZE // 2 - 4,
        )

    score_text = hud_font.render(
        f"SCORE {game.score}",
        True,
        TEXT_COLOR,
    )
    lives_text = hud_font.render(
        f"LIVES {game.lives}",
        True,
        TEXT_COLOR,
    )

    screen.blit(
        score_text,
        score_text.get_rect(midleft=(8, TILE_SIZE // 2)),
    )
    screen.blit(
        lives_text,
        lives_text.get_rect(
            midright=(
                screen.get_width() - 8,
                TILE_SIZE // 2,
            )
        ),
    )

    if game.is_powered_up:
        power_text = hud_font.render(
            f"POWER {game.powered_moves_remaining}",
            True,
            POWER_PELLET_COLOR,
        )

        screen.blit(
            power_text,
            power_text.get_rect(
                center=(
                    screen.get_width() // 2,
                    TILE_SIZE // 2,
                )
            ),
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
        title.get_rect(center=(center_x, 100)),
    )
    screen.blit(
        start,
        start.get_rect(center=(center_x, 190)),
    )
    screen.blit(
        quit_text,
        quit_text.get_rect(center=(center_x, 230)),
    )


def draw_life_lost_screen(
    screen: pygame.Surface,
    game: Game,
    title_font: pygame.font.Font,
    menu_font: pygame.font.Font,
    hud_font: pygame.font.Font,
) -> None:
    draw_game(screen, game, hud_font)

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
        title.get_rect(center=(center_x, 90)),
    )
    screen.blit(
        score,
        score.get_rect(center=(center_x, 155)),
    )
    screen.blit(
        replay,
        replay.get_rect(center=(center_x, 215)),
    )
    screen.blit(
        menu,
        menu.get_rect(center=(center_x, 255)),
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
    