import asyncio
import time
from Map.Navigate import Navigate
from Map.Position import Position
from Chat.HandleChat import HandleChat

async def main():
    time.sleep(3)
    navigate_task = asyncio.create_task(Navigate()(1, "ArtClassroom-1"))
    await asyncio.gather(navigate_task)

if __name__ == "__main__":
    asyncio.run(main())