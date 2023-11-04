from random import randint
import wx

from punch.entities.entity import Entity
from ..timer import Timer
from ..key_event import KeyEvent
from ..consts import EVT_KEY_DOWN, EVT_KEY_UP
from ..world_map import WorldMap, TileType
from ..entities.enemy import Enemy
from .state import State


class Gameplay(State):
    def on_push(self):
        super().on_push()
        self.initialize_map()
        game = self.get_root_state()
        self.ambience = game.audio.new_sound("ambience.ogg", looping=True, direct=True)
        self.enemies: list[Enemy] = []
        self.enimy_spawn_timer = Timer()
        self.enemy_spawn_time = 1000
        self.max_enemies = 3
        self.player = Entity(self.world_map, 1, 0, 0, game.audio.new_sound_group())

    def initialize_map(self):
        self.world_map = WorldMap(3, 10, 1)
        self.world_map.set_tiles_in(0, 2, 0, 9, 0, 0, TileType.rocks)

    def on_enter(self):
        super().on_enter()
        self.get_root_state().audio.set_listener_position(1, 0, 0)
        self.ambience.play()

    def on_exit(self):
        super().on_exit()
        self.ambience.pause()

    def on_pop(self):
        super().on_pop()
        self.ambience.stop()

    def update(self, key_events: list[KeyEvent]) -> None:
        super().update(key_events)
        for enemy in self.enemies.copy():
            if enemy._destroied:
                self.enemies.remove(enemy)
                continue
            enemy.update()
        if len(self.enemies) < self.max_enemies:
            if self.enimy_spawn_timer.elapsed >= self.enemy_spawn_time:
                self.enimy_spawn_timer.restart()
                self.enemies.append(
                    Enemy(
                        self.world_map,
                        self.player,
                        randint(0, 2),
                        9,
                        350,
                        self.get_root_state().audio.new_sound_group(),
                    )
                )
        for event in key_events:
            if event.type == EVT_KEY_DOWN:
                if event.key_code == wx.WXK_ESCAPE and self.parent:
                    self.parent.pop()
