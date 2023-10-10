import wx
from .key_event import KeyEvent
from .consts import *
from .states.state import State
from .states.title_screen import TitleScreen
from .audio.manager import AudioManager


class Game(wx.Frame, State):
    """The main game object. Only one instance of this class should be created at a time"""

    def __init__(self, title: str = "Punch!", fps: int = 60):
        wx.Frame.__init__(self, None, title=title)
        State.__init__(self)
        self.audio = AudioManager()
        self.key_events: list[KeyEvent] = []
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.fps = fps
        self.Bind(wx.EVT_TIMER, self.on_update)
        self.timer = wx.Timer(self)
        self.title_screen = TitleScreen(self)

    def on_key_down(self, event):
        if not event.IsAutoRepeat():
            self.key_events.append(KeyEvent.from_wx_event(EVT_KEY_DOWN, event))
        event.Skip()

    def on_key_up(self, event):
        self.key_events.append(KeyEvent.from_wx_event(EVT_KEY_UP, event))
        event.Skip()

    def get_key_events(self) -> list[KeyEvent]:
        """Returns all key events since the last call to this function"""
        copy = self.key_events.copy()
        self.key_events.clear()
        return copy

    def on_update(self, event):
        self.audio.try_clean_oneshot_sounds()
        events = self.get_key_events()
        self.update(events)

    def start(self):
        """Starts the game loop. And enters the title screen"""
        self.timer.Start(int((1 / self.fps) * 1000))
        self.append(self.title_screen)
