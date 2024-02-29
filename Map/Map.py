import json
from Map.Position import Position


class Map:
    def __init__(self, map_name = "Map"):
        self.file_path = "./Data/Map/" + map_name + ".json"
        self.pos = Position()
        self.map_data = self.read_map_from_json()
        min_x, max_x, min_y, max_y = self.get_map_bounds()

        map_width = max_x - min_x + 1
        map_height = max_y - min_y + 1

        self.map_matrix = [[[] for _ in range(map_width)] for _ in range(map_height)]
        self.name2pos = {}

        for tile in self.map_data["tileProperties"]:
            x = tile["tileCoordinate"]["x"] - min_x
            y = tile["tileCoordinate"]["y"] - min_y
            grid_type = tile["gridType"] 
            self.map_matrix[y][x].append(grid_type)

            if "-entrance" in grid_type:
                self.name2pos[grid_type[:-len("-entrance")]] = (x + min_x, y + min_y)
        
        self.offest = (min_x, min_y)

    def read_map_from_json(self):
        with open(self.file_path, "r") as file:
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

    def get_map(self):
        return self.map_matrix, self.offest, self.name2pos
    
    def get_surrounding(self, uid, y_extent, x_extent, ban_list = ["obstacle"]):
        pos_list = self.pos.get_pos()
        min_x_map, min_y_map = self.offest
        center_x, center_y = pos_list[uid]
        min_x = max(center_x - x_extent, min_x_map)
        max_x = min(center_x + x_extent, len(self.map_matrix[0]) + min_x_map - 1)
        min_y = max(center_y - y_extent, min_y_map)
        max_y = min(center_y + y_extent, len(self.map_matrix) + min_y_map - 1)

        surrounding = [[], []]

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                for grid_type in self.map_matrix[y - min_y_map][x - min_x_map]:
                    if "-" in grid_type:
                        grid_type = grid_type.split("-")[0]
                    if grid_type not in ban_list:
                        surrounding[0].append(grid_type)
    
        for uid_key, pos in pos_list.items():
            if uid_key != uid and pos[0] >= min_x and pos[0] <= max_x and pos[1] >= min_y and pos[1] <= max_y:
                surrounding[1].append(uid_key)
    
        surrounding = [list(set(surrounding[0])), list(set(surrounding[1]))]
        
        return surrounding
