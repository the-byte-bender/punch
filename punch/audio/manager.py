import cyal
from .pool import Pool
from .sound import Sound
from .sound_group import SoundGroup, sound_factory_type


class AudioManager:
    """Manages and coordinates the context, buffers and  sources"""

    def __init__(
        self, device: cyal.Device | None = None, base_sound_path: str = "sounds/"
    ):
        self.device = device or cyal.Device()
        self.context = cyal.Context(self.device, make_current=True, hrtf_soft=1)
        self.pool = Pool(self.context, base_sound_path)
        self.current_oneshot_sounds: list[Sound] = []

    def new_sound(self, file_path: str, oneshot=False, **kwargs):
        """Returns a new sound object. The buffer for the sound is either loaded from cache or cached from disk first on first request. If one_shot is True, the sound is considered to be a one-shot sound and will be kept in memory untill its stopped. One-shot sounds are also automaticly played when this function is called."""
        s = Sound(self.context, self.pool.get(file_path), **kwargs)
        if oneshot:
            s.play()
            self.current_oneshot_sounds.append(s)
        return s

    def new_oneshot_sound(self, file_path, **kwargs):
        """Alias for new_sound with oneshot set to true"""
        return self.new_sound(file_path, True, **kwargs)

    def new_sound_group(
        self, sound_factory: sound_factory_type | None = None, **defaults
    ):
        """Creates and returns a new sound group object. sound_factory is optional and will default to self.new_oneshot_sound, which should be appropriate for most applications. Any other keyword arguments will be passed as defaults for any new sound objects initialized by the created group."""
        if sound_factory is None:
            sound_factory = self.new_oneshot_sound
        return SoundGroup(sound_factory, **defaults)

    def try_clean_oneshot_sounds(self):
        """Cleans any stopped/finished one shot sounds. Must be called periodicly to prevent memory leaks"""
        for sound in self.current_oneshot_sounds.copy():
            if sound.is_stopped:
                self.current_oneshot_sounds.remove(sound)
