from typing import Callable, Any
from weakref import WeakSet
from .sound import Sound

sound_factory_type = Callable[[str, Any], Sound]


class SoundGroup:
    """A soundGroup manages a set of sound objecs, enabling you to control all of them at once. It should be initialized with a callback to use for generating new sound objects. The callback should take a file path, and keyword arguments to initialize the sound object and returns the sound object."""

    def __init__(self, sound_factory: sound_factory_type, **defaults):
        self.sound_factory = sound_factory
        self.defaults = defaults
        self.sounds = WeakSet[Sound]()
        self._position = (0, 0, 0)
        self._destroied = False

    def __del__(self):
        if not self._destroied:
            self.destroy()

    def destroy(self):
        """Stops all sounds related to this group. This group should not be used after a call to destroy()"""
        if not self._destroied:
            self._destroied = True
            for sound in self.sounds:
                sound.stop()
            self.sounds.clear()

    def add_sound(self, sound: Sound):
        """Adds sound to this group, adjusting its properties to match"""
        self.sounds.add(sound)
        sound.position = self._position

    def play_sound(self, file_path: str, **kwargs) -> Sound:
        sound = self.sound_factory(file_path, **{**self.defaults, **kwargs})
        self.add_sound(sound)
        if not sound.is_playing:
            sound.play()
        return sound

    @property
    def position(self) -> tuple[float, float, float]:
        return self._position

    @position.setter
    def position(self, value: tuple[float, float, float]):
        self._position = value
        for sound in self.sounds:
            if not sound.direct:
                sound.position = value
