# Evolvable-Agent-in-Social-Scene

## Architecture

![](https://s2.loli.net/2024/04/18/VOIc78Lr1yQKFUM.png)



## How to Start

1. **Clone the Repository**
   Start by cloning the repository and installing the required Python packages.

   ```shell
   git clone https://github.com/GAIR-NLP/evolvable-agent-in-social-scene
   cd evolvable-agent-in-social-scene
   pip install -r requirements.txt
   ```

2. **Set Language Model**

   - For OpenAI API

   	Set the environment variable `OPENAI_API_KEY` in your workplace

   	```bash
   	export OPENAI_API_KEY=your_openai_key
   	```

   	You can also create a `.env` file, including your key

   	```
   	OPENAI_API_KEY=your_openai_key
   	```

   - For Remote Hugging Face Model
   - For Local Hugging Face Model

3. **Start MongoDB**

   ```bash
   sudo mongodb
   ```

   You can use `systemctl status mongod` to check if MongoDB has started successfully

   To restart, run:

   ```bash
   sudo service mongod restart
   ```

4. **Start WebSocket Server**

   First, set the environment variable `IP_ADDRESS` using the same method in 2, for example:

   ```
   export IP_ADDRESS=127.0.0.1
   ```

   Then, launch the WebSocket server

   ```shell
   python WebSocket/Server.py
   ```

   It will run on port 8000 of the `IP_ADDRESS`.

5. **Run main.py**

   ```python
   python main.py
   ```

6. **Configure Nginx**
   Modify the `nginx.conf` file to make the `root` directive points to your WebGL app location. 

   The location of `nginx.conf` depends on your operating system:

   - Mac    `/usr/local/etc/nginx/nginx.conf` or `/opt/homebrew/etc/nginx/nginx.conf`
   - Linux  `  /etc/nginx/nginx.conf`
   - Windows  `  C:\nginx\conf\nginx.conf`

   ```nginx
   listen       8080;
   server_name  localhost;
   location / {
   	root   /path/to/your/WebGL; # Eg. ~/Desktop/evolvable-agent-in-social-scene/Unity;
   	index  index.html;
   }
   ```

7. **Deploy Unity WebGL App Using Nginx**
   Start the Nginx server to deploy the Unity WebGL application. 

   ```shell
   sudo nginx
   ```
   To reload, use:
   ```shell
   sudo nginx -s reload
   ```

8. **Access the application**
   Open`localhost:8080` in a web browser.



## For Developers (Linux)

### Deployment

```zsh
ssh yifeng@10.22.31.26 
password: 123456

sudo rm -rf evolvable-agent-in-social-scene

git clone git@github.com:GAIR-NLP/evolvable-agent-in-social-scene.git
cd evolvable-agent-in-social-scene

screen -ls | grep Detached | cut -d. -f1 | awk '{print $1}' | xargs -I {} screen -X -S {} quit
sudo systemctl stop mongod
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock 
sudo service mongod restart
sudo systemctl status mongod

screen
python3.11 WebSocket/Server.py
Ctrl+A
D

screen
python3.11 main.py
sudo nginx -s reload
```

### Test
```zsh
ssh yifeng@10.22.31.26 
password:123456

http://10.22.31.26:8080/

cd evolvable-agent-in-social-scene
python3.11 test.py
```
