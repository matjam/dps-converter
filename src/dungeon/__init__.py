# defines a dungeon map

from enum import Enum
import csv
from pathlib import Path


class Tile(Enum):
    EMPTY = 0
    ROOM = 1
    DOOR_HORIZONTAL = 2
    DOOR_VERTICAL = 3
    PORTCULLIS_HORIZONTAL = 4
    PORTCULLIS_VERTICAL = 5
    SECRET_DOOR_HORIZONTAL = 6
    SECRET_DOOR_VERTICAL = 7
    STAIRS_DOWN_TOP = 8
    STAIRS_DOWN_BOTTOM = 9
    STAIRS_UP_TOP = 10
    STAIRS_UP_BOTTOM = 11


class OutOfBoundsError(Exception):
    pass


class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._map = [[Tile.EMPTY for y in range(height)] for x in range(width)]
        print(f"created dungeon map width {self.width} height {self.height}")

    def _check_bounds(self, x: int, y: int):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            raise Exception(f"x:{x} y:{y} out of bounds")

    def set_tile(self, x: int, y: int, tile: Tile):
        self._check_bounds(x, y)
        try:
            self._map[x][y] = tile
        except Exception as e:
            print(f"exception x:{x} y:{y}")
            raise e

    def get_tile(self, x: int, y: int) -> Tile:
        self._check_bounds(x, y)
        return self._map[x][y]

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                if tile is Tile.ROOM:
                    print("= ", end="")
                elif (
                    tile is Tile.SECRET_DOOR_HORIZONTAL
                    or tile is Tile.SECRET_DOOR_VERTICAL
                ):
                    print("S ", end="")
                elif tile is Tile.DOOR_HORIZONTAL or tile is Tile.DOOR_VERTICAL:
                    print("D ", end="")
                elif (
                    tile is Tile.PORTCULLIS_HORIZONTAL
                    or tile is Tile.PORTCULLIS_VERTICAL
                ):
                    print("P ", end="")
                elif tile is Tile.STAIRS_UP_TOP:
                    print("U ", end="")
                elif tile is Tile.STAIRS_UP_BOTTOM:
                    print("u ", end="")
                elif tile is Tile.STAIRS_DOWN_BOTTOM:
                    print("x ", end="")
                elif tile is tile.STAIRS_DOWN_TOP:
                    print("X ", end="")
                else:
                    print("  ", end="")
            print()

    def tile(self, x: int, y: int, *args) -> bool:
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            raise OutOfBoundsError()

        tiles = set(args)

        tile = self._map[x][y]
        return tile in tiles

    def tile_empty(self, x: int, y: int) -> bool:
        return self.tile(
            x, y, Tile.EMPTY, Tile.SECRET_DOOR_HORIZONTAL, Tile.SECRET_DOOR_VERTICAL
        )

    def is_corner_out_down_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and not self.tile_empty(x - 1, y)
                and not self.tile_empty(x, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_out_up_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and not self.tile_empty(x, y - 1)
                and not self.tile_empty(x - 1, y)
            )
        except OutOfBoundsError:
            return False

    def is_corner_out_down_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and not self.tile_empty(x + 1, y)
                and not self.tile_empty(x, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_out_up_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and not self.tile_empty(x + 1, y)
                and not self.tile_empty(x, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_vertical_up_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x, y - 1)
                and not self.tile_empty(x - 1, y)
                and not self.tile_empty(x - 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_vertical_down_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x, y + 1)
                and not self.tile_empty(x - 1, y)
                and not self.tile_empty(x - 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_vertical_up_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x, y - 1)
                and not self.tile_empty(x + 1, y)
                and not self.tile_empty(x + 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_vertical_down_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x, y + 1)
                and not self.tile_empty(x + 1, y)
                and not self.tile_empty(x + 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_horizontal_up_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x - 1, y)
                and not self.tile_empty(x, y - 1)
                and not self.tile_empty(x - 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_horizontal_up_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x + 1, y)
                and not self.tile_empty(x, y - 1)
                and not self.tile_empty(x + 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_horizontal_down_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x - 1, y)
                and not self.tile_empty(x, y + 1)
                and not self.tile_empty(x - 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_wall_horizontal_down_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x + 1, y)
                and not self.tile_empty(x, y + 1)
                and not self.tile_empty(x + 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_in_up_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x - 1, y)
                and self.tile_empty(x, y - 1)
                and not self.tile_empty(x - 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_in_up_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x + 1, y)
                and self.tile_empty(x, y - 1)
                and not self.tile_empty(x + 1, y - 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_in_down_left(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x - 1, y)
                and self.tile_empty(x, y + 1)
                and not self.tile_empty(x - 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_corner_in_down_right(self, x: int, y: int) -> bool:
        try:
            return (
                self.tile_empty(x, y)
                and self.tile_empty(x + 1, y)
                and self.tile_empty(x, y + 1)
                and not self.tile_empty(x + 1, y + 1)
            )
        except OutOfBoundsError:
            return False

    def is_in_room(self, x: int, y: int) -> bool:
        try:
            return (
                not self.tile_empty(x, y)
                and not self.tile_empty(x - 1, y)
                and not self.tile_empty(x, y - 1)
                and not self.tile_empty(x + 1, y)
                and not self.tile_empty(x, y + 1)
            )
        except OutOfBoundsError:
            return False

    def debug(self, x, y):
        print(f"x pos {x} len {len(self._map)} y pos {y} len {len(self._map[0])}")


def load_donjon_tsv(filename: str) -> Dungeon:
    tmpArray = []
    if Path(filename).is_file():
        with open(filename) as fd:
            rd = csv.reader(fd, delimiter="\t")
            for row in rd:
                tmpArray.append(row)

    if len(tmpArray) == 0:
        raise Exception("donjon TSV file contains no data or was unable to be parsed")

    dungeon = Dungeon(len(tmpArray[0]), len(tmpArray))

    mapping = {
        "F": Tile.ROOM,
        "DR": Tile.DOOR_VERTICAL,
        "DL": Tile.DOOR_VERTICAL,
        "DT": Tile.DOOR_HORIZONTAL,
        "DB": Tile.DOOR_HORIZONTAL,
        "DSL": Tile.SECRET_DOOR_VERTICAL,
        "DSR": Tile.SECRET_DOOR_VERTICAL,
        "DST": Tile.SECRET_DOOR_HORIZONTAL,
        "DSB": Tile.SECRET_DOOR_HORIZONTAL,
        "DPT": Tile.PORTCULLIS_HORIZONTAL,
        "DPB": Tile.PORTCULLIS_HORIZONTAL,
        "DPL": Tile.PORTCULLIS_VERTICAL,
        "DPR": Tile.PORTCULLIS_VERTICAL,
        "SUU": Tile.STAIRS_UP_BOTTOM,
        "SU": Tile.STAIRS_UP_TOP,
        "SDD": Tile.STAIRS_DOWN_BOTTOM,
        "SD": Tile.STAIRS_DOWN_TOP,
    }

    for y, row in enumerate(tmpArray):
        for x, item in enumerate(row):
            if item in mapping:
                dungeon.set_tile(x, y, mapping[item])
            else:
                dungeon.set_tile(x, y, Tile.EMPTY)

    return dungeon
