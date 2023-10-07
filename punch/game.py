import wx
from .key_event import KeyEvent
from .consts import *


class Game(wx.Frame):
    """The main game object. Only one instance of this class should be created at a time"""

    def __init__(self, title: str = "Punch!", fps: int = 60):
        super().__init__(None, title=title)
        self.key_events: list[KeyEvent] = []
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.fps = fps
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update)

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
        events = self.get_key_events()

    def start(self):
        """Starts the game loop."""
        self.timer.Start(int((1 / self.fps) * 1000))
