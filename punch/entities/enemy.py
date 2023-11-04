from ..audio.sound_group import SoundGroup
from ..world_map import WorldMap
from ..timer import Timer
from .entity import Entity


class Enemy(Entity):
    """enemies will try to run to the target's y and kill the target"""

    def __init__(
        self,
        world_map: WorldMap,
        target: Entity,
        x: int,
        y: int,
        time_per_step: int,
        sound_group: SoundGroup,
    ):
        super().__init__(world_map, x, y, 0, sound_group)
        self.target = target
        self.movement_timer = Timer()
        self.time_per_step = time_per_step

    def update(self):
        super().update()
        if self.movement_timer.elapsed >= self.time_per_step:
            self.movement_timer.restart()
            if self.y > self.target.y:
                self.move(self.x, self.y - 1, 0, True)
            elif self.y < self.target.y:
                self.move(self.x, self.y + 1, self.z, True)
            if self.y == self.target.y:
                # hit the target
                self.destroy()
