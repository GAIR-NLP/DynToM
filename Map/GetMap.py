import json

class GetMap:
    def __init__(self, map_name="NPCObstacle"):
        self.file_path = "./Data/Map/" + map_name + ".json"
        self.map_data = self.read_map_from_json()

    def read_map_from_json(self):
        with open(self.file_path, 'r') as file:
            map_data = json.load(file)
        return map_data

    def get_map_bounds(self):
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')

        for tile in self.map_data["tileProperties"]:
            x = tile["tileCoordinate"]["x"]
            y = tile["tileCoordinate"]["y"]
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)

        return min_x, max_x, min_y, max_y

    def convert_to_matrix(self):
        min_x, max_x, min_y, max_y = self.get_map_bounds()

        map_width = max_x - min_x + 1
        map_height = max_y - min_y + 1

        map_matrix = [[0 for _ in range(map_width)] for _ in range(map_height)]

        for tile in self.map_data["tileProperties"]:
            x = tile["tileCoordinate"]["x"] - min_x
            y = tile["tileCoordinate"]["y"] - min_y
            map_matrix[y][x] = 1

        return map_matrix, (min_x, min_y)