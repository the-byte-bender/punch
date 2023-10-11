import cyal
from .utils import convert_to_openal_coordinates


class Sound:
    """A sound object encapsulates a cyal Source object, loaded with a buffer. It represents a single sound that can be individually manipulated"""

    def __init__(self, context: cyal.Context, buffer: cyal.Buffer, **kwargs):
        self.context = context
        self.buffer = buffer
        self.source = self.context.gen_source()
        self.source.buffer = buffer
        self.source.spatialize = True
        self._position = (0.0, 0.0, 0.0)
        self._direct = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def direct(self) -> bool:
        """If a sound is direct, it means this sound will be played directly on the matching channels and will not be able to set its position, roleoff factor and other positional parameters"""
        return self._direct

    @direct.setter
    def direct(self, value):
        if value != self._direct:  # To avoid any redundant changes
            if value:
                self.source.relative = True
                self.source.direct_channels = True
                self.position = (0.0, 0.0, 0.0)
                self._direct = True
            else:
                self.source.relative = False
                self.source.direct_channels = False
                self._direct = False

    @property
    def position(self) -> tuple[float, float, float]:
        """Modifying position is not allowed for direct sources"""
        return self._position

    @position.setter
    def position(self, value):
        if self.direct:
            raise ValueError("Unsupported for direct sources")
        self._position = value
        self.source.position = convert_to_openal_coordinates(*value)

    @property
    def rolloff_factor(self) -> float:
        return self.source.rolloff_factor

    @rolloff_factor.setter
    def rolloff_factor(self, value):
        self.source.rolloff_factor = value

    @property
    def pitch(self) -> float:
        return self.source.pitch

    @pitch.setter
    def pitch(self, value):
        self.source.pitch = value

    @property
    def looping(self) -> bool:
        return self.source.looping

    @looping.setter
    def looping(self, value):
        self.source.looping = value

    @property
    def gain(self) -> float:
        return self.source.gain

    @gain.setter
    def gain(self, value):
        self.source.gain = value

    @property
    def is_playing(self) -> bool:
        return self.source.state == cyal.SourceState.PLAYING

    @property
    def is_paused(self) -> bool:
        return self.source.state == cyal.SourceState.PAUSED

    @property
    def is_stopped(self) -> bool:
        return self.source.state in [
            cyal.SourceState.STOPPED,
            cyal.SourceState.INITIAL,
        ]

    def play(self):
        self.source.play()

    def pause(self):
        self.source.pause()

    def stop(self):
        self.source.stop()
