import wx
from ..key_event import KeyEvent
from ..consts import EVT_KEY_DOWN, EVT_KEY_UP
from ..world_map import WorldMap, TileType
from .state import State


class Gameplay(State):
    def on_push(self):
        super().on_push()
        self.initialize_map()
        game = self.get_root_state()
        self.ambience = game.audio.new_sound("ambience.ogg", looping=True, direct=True)

    def initialize_map(self):
        self.world_map = WorldMap(3, 10, 1)
        self.world_map.set_tiles_in(0, 2, 0, 9, 0, 0, TileType.rocks)

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
                if event.key_code == wx.WXK_ESCAPE and self.parent:
                    self.parent.pop()
