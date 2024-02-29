## WebSocket

### WebSocket.WebSocketClient

**Construct** 

```python
def __init(self, url : Optional[str] = f"ws://{os.getenv('IP_ADDRESS')}:8000/ws")
```

**Methods**

- ```python
  async def send_commands(self, commands: List[str]) -> None
  ```

  Connect to WebSocket Server send the provided list of commands. After all commands have been sent, the connection is closed.



## Map

### Map.Position

**Construct** 

```python
def __init__(self)
```

**Methods**

- ```python
  def update_pos(self, uid : int, x : int, y : int) -> None
  ```

  Update the position of the uid as uid in MongoDB to (x, y)

- ```python
  async def get_pos(self, uid : Optional[int] = None)
  ```

​	Retrieve the position of uid if uid is provided, otherwise return the positions of all uid.



### Map.Map

**Construct**

```python
def __init__(self, map_name : Optional[str] = "Map")
```

**Methods**

- ```python
  def get_map(self) -> Tuple[List[List[List[Str]]], Tuple[int, int], Dict[str, Tuple[int, int]]]
  ```
  
  Return
  
  - A map matrix starting from 0, map_matrix(x, y) is a string list containing all types of (x, y)
  - Offset coordinates for mapping the coordinates into position in Unity
  - A dictionary mapping type string to coordinates.
  
  Type example: obstalce, Classroom-scope, Gym-1-entrance, Library-2-entrance (1, 2 are uid)
  
- ```python
  def get_surrounding(self, uid: int, y_extent: int, x_extent: int, ban_list: Optional[List[str]] = ["obstacle"]) -> List[List[Union[str, int]]]
  ```

  Retrieve the surrounding area of a given uid within a specified extent, excluding the types in the ban_list and return a list of two lists. 

  The first list contains the types of grids in the surrounding area, and the second list contains the uids of other entities in the surrounding area.



### Map.Navigate

**Construct** 

```python
navigate = Navigate(map_name = "Map")
```

**Methods**

- ```python
  async def __call__(self, uid: int, end: Union[int, str, Tuple[int, int]]) -> None
  ```

  Navigate in Unity for uid. Destination(end) can be specified as an ID, a name, or a coordinate tuple. 



## Chat

### HandleChat

**Construct** 

```python
def __init__(self)
```

**Methods**

- ```python
  async def send_chat_to_unity(self, from_uid: int, to_uid: int, content: str) -> None
  ```

  Send a chat message to Unity and save the chat in MongoDB.

- ```python
  async def receive_message_from_unity(self, message: dict) -> None
  ```

  Invoked when client received a chat from Unity, save the chat in MongoDB, and distributed the chat.

  Key in message : from_uid, to_uid, content
  
- ```python
  def get_chats(self, from_uid: Optional[int] = None, to_uid: Optional[int] = None, start_time: Optional[int] = None, end_time: Optional[int] = None) -> List[dict]
  ```

  Retrieve chat from the MongoDB database according to the provided parameters.

- ```python
  async def distribute_chat(self, from_uid: int, to_uid: int, content: str) -> None
  ```

  Distribute a chat to the to_uid. NPCManager handles the distribution of the message.



## NPC

### NPCManager

**Construct** 

```python
def __init__(self)
```

It will Initialize the NPCManager with a dictionary of NPCs, with the key being the NPC's uid and the value being an instance of the NPC class.

**Methods**

- ```python
  def register_npc(self, uid: int, info: dict) -> None
  ```

  Register a new NPC with uid and a dictionary of information (info) about the NPC.

- ```python
  async def distribute_chat(self, from_uid: int, to_uid: int, content: str) -> None
  ```

  Distribute a chat message from from_uid to to_uid with the content of the message.



### NPC

**Construct**

```python
def __init__(self, uid : int, info : dict)
```

**Methods**

- ```python
  def receive_chat(self, from_uid : int, to_uid : int, content : str) -> None
  ```




### Agent

**Construct**

```python
def __init__(self, uid : Optional[int] = 0, info : dict)
```

**Methods**

- ```python
  
  ```

  