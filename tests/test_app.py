import pygame
import pytest

from maze_muncher.app import (
    MenuAction,
    WinAction,
    direction_for_key,
    menu_action_for_key,
    win_action_for_key,
)

from maze_muncher.movement import Direction


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        (pygame.K_UP, Direction.UP),
        (pygame.K_DOWN, Direction.DOWN),
        (pygame.K_LEFT, Direction.LEFT),
        (pygame.K_RIGHT, Direction.RIGHT),
        (pygame.K_w, Direction.UP),
        (pygame.K_s, Direction.DOWN),
        (pygame.K_a, Direction.LEFT),
        (pygame.K_d, Direction.RIGHT),
    ],
)
def test_direction_for_key(
    key: int,
    expected: Direction,
) -> None:
    assert direction_for_key(key) is expected


def test_unknown_key_has_no_direction() -> None:
    assert direction_for_key(pygame.K_SPACE) is None


@pytest.mark.parametrize(
    "key",
    [
        pygame.K_RETURN,
        pygame.K_SPACE,
    ],
)
def test_menu_start_keys(key: int) -> None:
    assert menu_action_for_key(key) is MenuAction.START


def test_escape_quits_from_menu() -> None:
    assert menu_action_for_key(pygame.K_ESCAPE) is MenuAction.QUIT


def test_unknown_menu_key_has_no_action() -> None:
    assert menu_action_for_key(pygame.K_a) is None


@pytest.mark.parametrize(
    "key",
    [
        pygame.K_RETURN,
        pygame.K_SPACE,
    ],
)
def test_win_screen_replay_keys(key: int) -> None:
    assert win_action_for_key(key) is WinAction.REPLAY


def test_escape_returns_to_menu_from_win_screen() -> None:
    assert win_action_for_key(pygame.K_ESCAPE) is WinAction.MENU


def test_unknown_win_screen_key_has_no_action() -> None:
    assert win_action_for_key(pygame.K_a) is None