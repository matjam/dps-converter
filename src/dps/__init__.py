import json
import random


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Map:
    def __init__(self):
        self._data = get_template()

    def get_json(self):
        return json.dumps(self._data, indent=2)

    # Add a Bunch to the root Bunch and return its ID
    def add_bunch(self, name):
        layer_id = self.get_next_bunch_id()

        layer = {
            "choosingPreset": False,
            "id": layer_id,
            "invisible": False,
            "layers": [],
            "name": name,
            "opacity": 100,
            "parent": 1,
        }
        self._data["tables"]["Bunch"].append(layer)
        root = self.get_bunch_by_id(1)
        root["layers"].append(layer_id)
        return layer_id

    # Add a plot to the Plots and return its ID
    def add_plot(
        self, location: Location, size: Size, texture_id: int, parent_bunch_id: int
    ):
        # create the plot

        plot_id = self.get_next_object_id()
        plot = {
            "helper": texture_id,
            "id": plot_id,
            "isLocked": False,
            "lockedX": 0,
            "lockedY": 0,
            "points": [
                {"x": location.x, "y": location.y},
                {"x": location.x + size.width, "y": location.y + size.height},
            ],
            "seed": 0,
            "textureRotation": 0,
            "textureScale": 1,
            "textureShiftX": 0,
            "textureShiftY": 0,
        }
        self._data["tables"]["Plot"].append(plot)
        self.add_object_to_layer(parent_bunch_id, plot_id, "plot")

        return plot_id

    def add_obstacle(
        self, location: Location, texture_id: int, parent_bunch_id: int, **kwargs
    ):
        angle = kwargs.get("angle", 0)

        obstacle_id = self.get_next_object_id()
        obstacle = {
            "angle": angle,
            "begin": {"x": location.x, "y": location.y},
            "flipH": False,
            "flipV": False,
            "helper": texture_id,
            "id": obstacle_id,
            "points": [],
            "scale": 1,
            "seed": 0,
            "textureIndex": 0,
            "ver": 1,
            "x": 0,
            "y": 0,
        }

        self._data["tables"]["Obstacle"].append(obstacle)
        self.add_object_to_layer(parent_bunch_id, obstacle_id, "obstacle")

        return obstacle_id

    def add_object_to_layer(self, parent_bunch_id, object_id, layer_name):
        # create a layer and add the object to it
        layer_id = self.get_next_bunch_id()
        layer = {
            "choosingPreset": False,
            "data": object_id,
            "id": layer_id,
            "invisible": False,
            "name": f"{layer_name} {object_id}",
            "opacity": 100,
            "parent": parent_bunch_id,
        }
        self._data["tables"]["Layer"].append(layer)

        # add the layer to the bunch
        bunch = self.get_bunch_by_id(parent_bunch_id)
        bunch["layers"].append(layer_id)

    # add a texture helper and return it's ID
    def add_texture(self, path):
        texture_id = self.get_next_helper_id()
        texture = {
            "id": texture_id,
            "path": path,
        }
        self._data["tables"]["TextureItemHelper"].append(texture)
        return texture_id

    def get_bunch_by_id(self, bunch_id):
        for bunch in self._data["tables"]["Bunch"]:
            if bunch["id"] == bunch_id:
                return bunch

        raise Exception(f"could not find bunch id {bunch_id}")

    # bunch IDs are drawn from the same pool as layer IDs.
    def get_next_bunch_id(self):
        ids = set([0])
        for bunch in self._data["tables"]["Bunch"]:
            ids.add(bunch["id"])

        for layer in self._data["tables"]["Layer"]:
            ids.add(layer["id"])

        # I think if you have a million objects you have a problem
        for i in range(1000000):
            if i not in ids:
                return i

        raise Exception("ran out of possible Bunch IDs")

    # object IDs are drawn from Plot and Obstacle
    def get_next_object_id(self):
        ids = set([0])
        for plot in self._data["tables"]["Plot"]:
            ids.add(plot["id"])

        for obstacle in self._data["tables"]["Obstacle"]:
            ids.add(obstacle["id"])

        for i in range(1000000):
            if i not in ids:
                return i

        raise Exception("ran out of possible Object IDs")

    def get_next_helper_id(self):
        ids = set([0])
        for plot in self._data["tables"]["TextureItemHelper"]:
            ids.add(plot["id"])

        for i in range(1000000):
            if i not in ids:
                return i

        raise Exception("ran out of possible TextureItemHelper IDs")


class RandomTexture:
    def __init__(self):
        self.textures = list()

    def add(self, texture_id: int):
        self.textures.append(texture_id)

    def get(self):
        return self.textures[random.randrange(0, len(self.textures))]

    def dumps(self):
        return json.dumps(self.textures)


class TextureSet:
    def __init__(self, map: Map, filename: str):
        self.textures = dict()

        with open(filename) as f:
            data = json.load(f)

        for name, files in data.items():
            self.textures[name] = RandomTexture()
            for f in files:
                self.textures[name].add(map.add_texture(f))

    def get(self, name):
        return self.textures[name].get()

    def dump(self):
        for k, v in self.textures.items():
            print(f"{k}: {v.dumps()}")


def get_template():
    template = """{
    "tables": {
        "AbsFx": [],
        "AbsLayer": [],
        "AbsMapObject": [],
        "AbsMapObjectTextured": [],
        "Arc": [],
        "BevelFx": [
            {
                "angle": 73,
                "blur": 6,
                "distance": 4,
                "highlightAlpha": 0.25,
                "highlightColor": 16777215,
                "id": 17,
                "isEnabled": true,
                "parent": 4,
                "shadowAlpha": 0.5,
                "shadowColor": 0,
                "strength": 2
            }
        ],
        "BorderFx": [],
        "Brush": [],
        "Bunch": [
            {
                "choosingPreset": false,
                "id": 1,
                "invisible": false,
                "layers": [],
                "name": "root",
                "opacity": 100
            }
        ],
        "DropShadowFx": [
            {
                "alpha": 0.8,
                "angle": 40,
                "blur": 14,
                "color": 0,
                "distance": 8,
                "id": 5,
                "inner": false,
                "isEnabled": true,
                "parent": 1
            },
            {
                "alpha": 0.3,
                "angle": 40,
                "blur": 4,
                "color": 0,
                "distance": 6,
                "id": 10,
                "inner": false,
                "isEnabled": true,
                "parent": 2
            },
            {
                "alpha": 0.2,
                "angle": 40,
                "blur": 2,
                "color": 0,
                "distance": 3,
                "id": 15,
                "inner": false,
                "isEnabled": true,
                "parent": 3
            }
        ],
        "Elipse": [],
        "Figure": [],
        "FxPreset": [
            {
                "fxs": [
                    4,
                    5
                ],
                "id": 1,
                "isOpen": false,
                "name": "long shadow"
            },
            {
                "fxs": [
                    10
                ],
                "id": 2,
                "isOpen": false,
                "name": "middle shadow"
            },
            {
                "fxs": [
                    15
                ],
                "id": 3,
                "isOpen": false,
                "name": "short shadow"
            },
            {
                "fxs": [
                    17
                ],
                "id": 4,
                "isOpen": false,
                "name": "bevel"
            },
            {
                "fxs": [
                    24
                ],
                "id": 5,
                "isOpen": false,
                "name": "yellow glow"
            },
            {
                "fxs": [
                    26
                ],
                "id": 6,
                "isOpen": false,
                "name": "orange light"
            }
        ],
        "GlowInnerFx": [],
        "GlowOutFx": [
            {
                "alpha": 0.75,
                "blur": 6,
                "color": 0,
                "id": 4,
                "isEnabled": true,
                "parent": 1,
                "strength": 1.7
            },
            {
                "alpha": 0.9,
                "blur": 8,
                "color": 8617275,
                "id": 24,
                "isEnabled": true,
                "parent": 5,
                "strength": 5
            }
        ],
        "Inscription": [],
        "Layer": [],
        "Light": [],
        "Linea": [],
        "Location": [
            {
                "backColor": 2631720,
                "cellSize": 1,
                "coors": true,
                "currentBunch": 1,
                "dpi": 70,
                "exportGrid": true,
                "gridAlpha": 0.1,
                "gridColor": 16777164,
                "hBold": 5,
                "half": false,
                "id": 1,
                "lastGroupNumber": 2,
                "lastLayerNumber": 1,
                "name": "map",
                "pageSize": 1,
                "root": 1,
                "selectedLayers": [],
                "selectedLu": {
                    "x": 0,
                    "y": 0
                },
                "selectedRd": {
                    "x": 0,
                    "y": 0
                },
                "snap": true,
                "transparentBack": true,
                "useDots": false,
                "useHex": false,
                "vBold": 5,
                "zoom": 100
            }
        ],
        "ObjBrush": [],
        "Obstacle": [],
        "Plot": [],
        "Polygon": [],
        "Puddle": [],
        "Spline": [],
        "Template": [],
        "TextureItemHelper": [],
        "TintFx": [
            {
                "color": 16752384,
                "id": 26,
                "intensity": 100,
                "isEnabled": true,
                "parent": 6
            }
        ],
        "Token": [],
        "Wall": []
    }
}"""
    return json.loads(template)
