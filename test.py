from Map.Navigate import Navigate
from Map.GetPos import GetPos
import time

if __name__ == "__main__":
    GetPos(0).get_pos()
    time.sleep(1)
    Navigate("NPCObstacle", (14, -2), (-20,-15)).navigate()


# cd /usr/local/bin && 