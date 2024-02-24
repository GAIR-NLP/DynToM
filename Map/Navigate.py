from Map.GetPath import GetPath
from Map.MovePath import MovePath

class Navigate:
    def __init__(self, map_name, start, end):
        self.map_name = map_name
        self.start = start
        self.end = end

    def navigate(self):
        path = GetPath("NPCObstacle", self.start, self.end).get_path()
        if path:
            MovePath(path).send_path_commands()
        else:
            print("No valid path found")