from Map.Map import Map
from Map.Position import Position
from WebSocket.Client import WebSocketClient 
import json
import asyncio
from collections import deque

class Navigate:
    def __init__(self, map_name = "Map"):  
        self.map_name = map_name
        self.client = WebSocketClient()
        self.map, self.offset, self.name2pos = Map(self.map_name).get_map()
        self.pos = Position()

    def get_directions(self):
        if not self.path or len(self.path) < 2:
            return []
        directions = []
        current_direction = self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1]
        count = 1

        for i in range(2, len(self.path)):
            x1, y1 = self.path[i - 1]
            x2, y2 = self.path[i]
            direction = x2 - x1, y2 - y1

            if direction == current_direction:
                count += 1
            else:
                directions.append((current_direction[0]*count, current_direction[1]*count))
                current_direction = direction
                count = 1

        directions.append((current_direction[0]*count, current_direction[1]*count))
        return directions

    async def send_path_commands(self):
        commands = []
        directions = self.get_directions()
        for (x, y) in directions:
            command = json.dumps({"command": "Move", "uid" : self.uid, "x": x, "y": y})
            commands.append(command)
        # asyncio.create_task(self.client.send_commands(commands))
        await self.client.send_commands(commands)
            
    async def bfs(self):
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
            print(f"Current position: {x}, {y}")
            if (x, y) == (ex, ey):
                return [(px + self.offset[0], py + self.offset[1]) for px, py in path + [(x, y)]]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
               
                if 0 <= nx < len(self.map[0]) and 0 <= ny < len(self.map) and "obstacle" not in self.map[ny][nx] and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))

        return []
    
    async def get_path(self):
        if isinstance(self.start, str):
            if self.start in self.name2pos:
                self.start = self.name2pos[self.start]
            else:
                raise ValueError(f"Invalid start name: {self.start}")
        if isinstance(self.end, str):
            if self.end in self.name2pos:
                self.end = self.name2pos[self.end]
            else:
                raise ValueError(f"Invalid end name: {self.end}")
            
        if isinstance(self.start, int):
            self.start = await self.pos.get_pos(self.start)
            print(f"\n\n\n\n\n\nStart position: {self.start}")
                        
        print(f"Moving from {self.start} to {self.end}")
        self.path = await self.bfs()
        
        if (self.path == []):
            print("Error: No path found")
        else:
            print(f"Path founded: {self.path}")
            
        return self.path
            
    async def __call__(self, uid, end):
        """
        Args:
            uid (int): user_id         
            end (int, string, or tuple(int, int)): Identity's Positon with ID(int), Positon with scene name(string), or Positon with coordinate(tuple(int, int))
        """
        self.uid = uid
        self.start = uid
        self.end = end
        self.path = await self.get_path()
        if self.path:
            await self.send_path_commands()
        else:
            print("Error: fail navigate to the destination")
