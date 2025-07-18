# randomize sounds
from random import randint
import pygame
import data.globalvars as globalvars
from behavior.utils.timer import Timer


class AudioManger:
    def __init__(self):
        self.sounds = {}
        self.is_playing = False

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            self.is_playing = False
        else:
            raise Exception(f"Sound '{sound_name}' not found!")

    def fadeout_sound(self, sound: str, duration: int):
        self.sounds[sound].fadeout(duration)

    def play_loop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play(loops=-1)
            self.is_playing = True
        else:
            raise Exception(f"Sound '{sound_name}' not found!")

    def stop(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
            self.is_playing = False

    # Volume: 0.0 (mute) to 1.0 (full volume)
    def set_volume(self, sound_name, volume):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume * (100 / 100))


# Manage music tracks
class MusicManager(AudioManger):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        try:
            pygame.mixer.init()
            self.sounds = {
                "main": pygame.mixer.Sound(
                    "resources/audio/music/main-theme.ogg"  # changed to wav
                )
            }
        except pygame.error:
            print("Warning: Audio mixer failed to initialize or load sounds.")
            self.sounds = {}


# Manages all sounds
class SoundManager(AudioManger):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        try:
            pygame.mixer.init()
            self.sounds = {
                "new_high_score": pygame.mixer.Sound("resources/audio/sound/new_high_score.ogg"),
                "achievement": pygame.mixer.Sound("resources/audio/sound/achievement.ogg"),
            }
        except pygame.error:
            print("Warning: Audio mixer failed to initialize or load sounds.")
            self.sounds = {}

    def play_randomize_sound(self, path: str, limit: int) -> str:
        num: int = randint(1, limit)
        sound_key: str = f"{path}_{num}"

        if sound_key in self.sounds:
            self.sounds[sound_key].play()