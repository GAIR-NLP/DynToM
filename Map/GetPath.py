from collections import deque
from Map.GetMap import GetMap

class GetPath:
    def __init__(self, map_name, start, end):
        self.map_name = map_name
        self.start = start
        self.end = end
        self.map, self.offset = GetMap(map_name).convert_to_matrix()
        self.path = self.find_path()

    def find_path(self):
        sx, sy = self.start
        ex, ey = self.end
        sx -= self.offset[0]
        sy -= self.offset[1]
        ex -= self.offset[0]
        ey -= self.offset[1]
        queue = deque([(sx, sy, [])])
        visited = set([(sx, sy)])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            x, y, path = queue.popleft()
            if (x, y) == (ex, ey):
                return [(px + self.offset[0], py + self.offset[1]) for px, py in path + [(x, y)]]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.map[0]) and 0 <= ny < len(self.map) and self.map[ny][nx] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))

        return []
    
    def get_path(self):
        return self.path