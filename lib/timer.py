from wx import StopWatch


class Timer:
    """A timer."""

    def __init__(self):
        self.w = StopWatch()

    @property
    def elapsed(self) -> int:
        """The elapsed time in milliseconds."""
        return self.w.Time()

    @elapsed.setter
    def elapsed(self, ms: int):
        self.w.Start(ms)

    def restart(self):
        self.elapsed = 0

    def pause(self):
        self.w.Pause()

    def resume(self):
        self.w.Resume()
