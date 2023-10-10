import wx
from ..key_event import KeyEvent
from ..consts import EVT_KEY_DOWN, EVT_KEY_UP
from .state import State


class Gameplay(State):
    def on_push(self):
        super().on_push()
        game = self.get_root_state()
        self.ambience = game.audio.new_sound("ambience.ogg", looping=True, direct = True)

    def on_enter(self):
        super().on_enter()
        self.ambience.play()

    def on_exit(self):
        super().on_exit()
        self.ambience.pause()

    def on_pop(self):
        super().on_pop()
        self.ambience.stop()

    def update(self, key_events: list[KeyEvent]) -> None:
        super().update(key_events)
        for event in key_events:
            if event.type == EVT_KEY_DOWN:
                if event.key_code == wx.WXK_ESCAPE:
                    if self.parent:
                        self.parent.pop()
