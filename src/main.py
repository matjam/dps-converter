import click
from src.dps import Map, Location, Size, TextureSet
from src.dungeon import Tile, load_donjon_tsv
import random


@click.command()
@click.argument("input_filename")
@click.argument("output_filename")
def main(input_filename: str, output_filename: str):
    random.seed()

    click.echo(f"attempting to convert {input_filename} to {output_filename}")
    dungeon = load_donjon_tsv(input_filename)

    click.echo(f"map is {dungeon.height} high and {dungeon.width} wide")

    # initialize textures
    map = Map()
    textures = TextureSet(map, "fa_dungeon_textures.json")
    floor_bunch_id = map.add_bunch("Floor")
    wall_bunch_id = map.add_bunch("Wall")
    floor_id = textures.get("floor")

    for y in range(dungeon.height):
        for x in range(dungeon.width):
            tile = dungeon.get_tile(x, y)
            if tile is Tile.ROOM:
                map.add_plot(
                    Location(x * 2, y * 2), Size(2, 2), floor_id, floor_bunch_id,
                )
            if (
                tile is Tile.SECRET_DOOR_HORIZONTAL
                or tile is Tile.SECRET_DOOR_VERTICAL
                or tile is Tile.STAIRS_DOWN_BOTTOM
                or tile is Tile.STAIRS_DOWN_TOP
                or tile is Tile.STAIRS_UP_BOTTOM
                or tile is Tile.STAIRS_UP_TOP
            ):
                map.add_plot(
                    Location(x * 2, y * 2),
                    Size(2, 2),
                    textures.get("floor_other"),
                    floor_bunch_id,
                )
            if tile is Tile.DOOR_HORIZONTAL:
                map.add_plot(
                    Location(x * 2, y * 2), Size(2, 2), floor_id, floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 0.5, y * 2 + 0.5),
                    textures.get("door"),
                    wall_bunch_id,
                )
            if tile is Tile.DOOR_VERTICAL:
                map.add_plot(
                    Location(x * 2, y * 2), Size(2, 2), floor_id, floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 1.5, y * 2 + 0.5),
                    textures.get("door"),
                    wall_bunch_id,
                    angle=90,
                )

            # corners
            if dungeon.is_corner_out_down_left(x, y):
                map.add_plot(
                    Location(x * 2, y * 2 + 1.5),
                    Size(0.5, 0.5),
                    floor_id,
                    floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 0.5, y * 2 + 1.5),
                    textures.get("corner_out"),
                    wall_bunch_id,
                    angle=90,
                )
            if dungeon.is_corner_out_up_left(x, y):
                map.add_plot(
                    Location(x * 2, y * 2), Size(0.5, 0.5), floor_id, floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 0.5, y * 2 + 0.5),
                    textures.get("corner_out"),
                    wall_bunch_id,
                    angle=180,
                )

            if dungeon.is_corner_out_down_right(x, y):
                map.add_plot(
                    Location(x * 2 + 1.5, y * 2 + 1.5),
                    Size(0.5, 0.5),
                    floor_id,
                    floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 1.5, y * 2 + 1.5),
                    textures.get("corner_out"),
                    wall_bunch_id,
                    angle=0,
                )

            if dungeon.is_corner_out_up_right(x, y):
                map.add_plot(
                    Location(x * 2 + 1.5, y * 2),
                    Size(0.5, 0.5),
                    floor_id,
                    floor_bunch_id,
                )
                map.add_obstacle(
                    Location(x * 2 + 1.5, y * 2 + 0.5),
                    textures.get("corner_out"),
                    wall_bunch_id,
                    angle=270,
                )

            # walls
            if dungeon.is_wall_vertical_down_left(x, y):
                map.add_obstacle(
                    Location(x * 2 - 0.5, y * 2 + 1.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=270,
                )

            if dungeon.is_wall_vertical_up_left(x, y):
                map.add_obstacle(
                    Location(x * 2 - 0.5, y * 2 + 0.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=270,
                )

            if dungeon.is_wall_vertical_down_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 2.5, y * 2 + 1.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=90,
                )

            if dungeon.is_wall_vertical_up_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 2.5, y * 2 + 0.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=90,
                )

            if dungeon.is_wall_horizontal_up_left(x, y):
                map.add_obstacle(
                    Location(x * 2 + 0.5, y * 2 - 0.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=0,
                )

            if dungeon.is_wall_horizontal_up_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 1.5, y * 2 - 0.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=0,
                )

            if dungeon.is_wall_horizontal_down_left(x, y):
                map.add_obstacle(
                    Location(x * 2 + 0.5, y * 2 + 2.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=180,
                )

            if dungeon.is_wall_horizontal_down_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 1.5, y * 2 + 2.5),
                    textures.get("wall"),
                    wall_bunch_id,
                    angle=180,
                )

            if dungeon.is_corner_in_up_left(x, y):
                map.add_obstacle(
                    Location(x * 2 - 0.5, y * 2 - 0.5),
                    textures.get("corner_in"),
                    wall_bunch_id,
                    angle=0,
                )

            if dungeon.is_corner_in_up_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 2.5, y * 2 - 0.5),
                    textures.get("corner_in"),
                    wall_bunch_id,
                    angle=90,
                )

            if dungeon.is_corner_in_down_left(x, y):
                map.add_obstacle(
                    Location(x * 2 - 0.5, y * 2 + 2.5),
                    textures.get("corner_in"),
                    wall_bunch_id,
                    angle=270,
                )

            if dungeon.is_corner_in_down_right(x, y):
                map.add_obstacle(
                    Location(x * 2 + 2.5, y * 2 + 2.5),
                    textures.get("corner_in"),
                    wall_bunch_id,
                    angle=180,
                )

            if dungeon.is_in_room(x, y):
                if random.randint(1, 10) == 5:
                    what = random.randint(1, 10)

                    if what < 4:
                        map.add_obstacle(
                            Location(x * 2, y * 2),
                            textures.get("blood"),
                            floor_bunch_id,
                            angle=random.randrange(0, 359),
                        )
                    elif what < 6:
                        map.add_obstacle(
                            Location(x * 2, y * 2),
                            textures.get("skeleton"),
                            floor_bunch_id,
                            angle=random.randrange(0, 359),
                        )
                    else:
                        map.add_obstacle(
                            Location(x * 2, y * 2),
                            textures.get("broken_weapon"),
                            floor_bunch_id,
                            angle=random.randrange(0, 359),
                        )

    with open(output_filename, "w") as f:
        f.write(map.get_json())


if __name__ == "__main__":
    main()
