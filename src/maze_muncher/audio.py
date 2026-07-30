from dataclasses import dataclass
from pathlib import Path

import pygame


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


DEFAULT_MUSIC_VOLUME = 0.35
DEFAULT_SFX_VOLUME = 0.45


def _load_sound(
    path: Path,
) -> pygame.mixer.Sound | None:
    if not path.exists():
        return None

    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None


@dataclass
class AudioManager:
    enemy_move: pygame.mixer.Sound | None
    game_over: pygame.mixer.Sound | None
    life_lost: pygame.mixer.Sound | None
    meanie_spawn: pygame.mixer.Sound | None
    pickup: pygame.mixer.Sound | None
    player_start: pygame.mixer.Sound | None
    victory: pygame.mixer.Sound | None
    power_pellet: pygame.mixer.Sound | None
    enemy_eaten: pygame.mixer.Sound | None
    music_volume: float = DEFAULT_MUSIC_VOLUME
    sfx_volume: float = DEFAULT_SFX_VOLUME

    @classmethod
    def load(cls) -> "AudioManager":
        audio = cls(
            enemy_move=_load_sound(ENEMY_MOVE_SFX),
            game_over=_load_sound(GAME_OVER_SFX),
            life_lost=_load_sound(LIFE_LOST_SFX),
            meanie_spawn=_load_sound(MEANIE_SPAWN_SFX),
            pickup=_load_sound(PICKUP_SFX),
            player_start=_load_sound(PLAYER_START_SFX),
            victory=_load_sound(VICTORY_SFX),
            power_pellet=_load_sound(POWER_PELLET_SFX),
            enemy_eaten=_load_sound(ENEMY_EATEN_SFX),
        )

        audio.set_music_volume(DEFAULT_MUSIC_VOLUME)
        audio.set_sfx_volume(DEFAULT_SFX_VOLUME)

        return audio

    def sounds(
        self,
    ) -> tuple[pygame.mixer.Sound | None, ...]:
        return (
            self.enemy_move,
            self.game_over,
            self.life_lost,
            self.meanie_spawn,
            self.pickup,
            self.player_start,
            self.victory,
            self.power_pellet,
            self.enemy_eaten,
        )

    def set_music_volume(
        self,
        volume: float,
    ) -> None:
        self.music_volume = max(
            0.0,
            min(1.0, volume),
        )

        try:
            pygame.mixer.music.set_volume(
                self.music_volume
            )
        except pygame.error:
            pass

    def set_sfx_volume(
        self,
        volume: float,
    ) -> None:
        self.sfx_volume = max(
            0.0,
            min(1.0, volume),
        )

        for sound in self.sounds():
            if sound is not None:
                sound.set_volume(self.sfx_volume)

    @staticmethod
    def play(
        sound: pygame.mixer.Sound | None,
    ) -> None:
        if sound is not None:
            sound.play()

    def start_music(
        self,
        path: Path,
    ) -> None:
        if not path.exists():
            return

        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(
                self.music_volume
            )
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    @staticmethod
    def stop_music() -> None:
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def start_menu_music(self) -> None:
        self.start_music(MENU_MUSIC)

    def start_game_over_music(self) -> None:
        self.start_music(GAME_OVER_MUSIC)

    def play_game_start(self) -> None:
        self.play(self.player_start)
        self.play(self.meanie_spawn)

    def play_score_gain(
        self,
        score_gained: int,
        *,
        enemy_move: bool = False,
    ) -> None:
        from maze_muncher.game import Game

        if score_gained >= Game.ENEMY_SCORE:
            self.play(self.enemy_eaten)
        elif score_gained == Game.POWER_PELLET_SCORE:
            self.play(self.power_pellet)
        elif score_gained > 0:
            self.play(self.pickup)
        elif enemy_move:
            self.play(self.enemy_move)

