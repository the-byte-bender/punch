import itertools
from enum import Enum


class TileType(Enum):
    air = 0
    rocks = 1


class WorldMap:
    """A simple 3d tile map"""

    def __init__(self, width: int, height: int, depth: int):
        self.width = width
        self.height = height
        self.depth = depth
        self.tiles = [
            [[TileType.air for _ in range(depth)] for _ in range(height)]
            for _ in range(width)
        ]

    def set_tile_at(self, x: int, y: int, z: int, type: TileType):
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            self.tiles[x][y][z] = type

    def get_tile_at(self, x: int, y: int, z: int) -> TileType:
        """Returns the tile at the given coordinates, otherwise returns TileType.air"""
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.tiles[x][y][z]
        return TileType.air  # Out of bounds so its all nothing

    def set_tiles_in(
        self,
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
        min_z: int,
        max_z: int,
        type: TileType = TileType.air,
    ):
        for x, y, z in itertools.product(
            range(min_x, max_x + 1), range(min_y, max_y + 1), range(min_z, max_z + 1)
        ):
            self.set_tile_at(x, y, z, type)
