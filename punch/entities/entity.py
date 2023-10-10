from random import randint
from ..world_map import WorldMap
from ..audio.sound_group import SoundGroup
from ..audio.sound import Sound


class Entity:
    """An entity in the game world is anything that can be moved around, can play sounds, etc. An entity must be initialized with a SoundGroup to manage its sounds."""

    def __init__(
        self, world_map: WorldMap, x: int, y: int, z: int, sound_group: SoundGroup
    ):
        self.world_map = world_map
        self.x = x
        self.y = y
        self.z = z
        self.sound_group = sound_group
        self._destroied = False

    def __del__(self):
        self.destroy()

    def destroy(self):
        if not self._destroied:
            self._destroied = True
            self.sound_group.destroy()

    def update(self):
        """Will be called frequently, so do any update logic or entity behavior here."""
        pass

    def play_sound(self, sound_path: str, **kwargs) -> Sound:
        """Any extra keyword arguments will be passed to sound_group.play_sound"""
        return self.sound_group.play_sound(sound_path, **kwargs)

    def play_footstep(self) -> Sound:
        """Plays a random footstep sound appropriate for the tile type this entity is standing on."""
        return self.play_sound(
            f"steps/{self.world_map.get_tile_at(self.x, self.y, self.z).name}/{randint(1, 5)}.ogg"
        )

    def move(self, x: int, y: int, z: int, play_sound: bool):
        """Moves this entity to the given coordinates. If play_sound is True, will play a footstep as well."""
        self.x = x
        self.y = y
        self.z = z
        self.sound_group.position = (x, y, z)
        if play_sound:
            self.play_footstep()
