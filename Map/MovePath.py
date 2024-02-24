from WebSocket.client import WebSocketClient
import json

class MovePath:
    def __init__(self, path):
        self.path = path
        self.client = WebSocketClient()

    def get_directions(self):
        if not self.path:
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

    def send_path_commands(self):
        commands = []
        directions = self.get_directions()
        for (x, y) in directions:
            command = json.dumps({"action": "Move", "x": x, "y": y})
            commands.append(command)
        self.client.run_forever(commands)
        