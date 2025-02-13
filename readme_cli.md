# CoppeliaSim Robotic Arm CLI



### Installation Requirements

```sh
pip install requests tqdm colorama
```

### Running the CLI

```sh
python script.py
```

### Getting IP from Localhost in Web Browser (Host Machine)
To find the IP address of your host machine when running a local server:
1. Run the following command:
   ```sh
   ipconfig  # Windows
   ifconfig  # Linux/macOS (or use ip a)
   ```
2. Look for an entry labeled **IPv4 Address** (e.g., `192.168.1.100`). Get the IP address and the port of the host machine.
3. Open a web browser and enter:
   ```
   http://<your-ip>:<port>
   ```
   Example: `http://192.168.1.100:8000`


## Command Syntax

Pick an Object
```sh
pick -o [Cuboid|Cylinder|Prism]
```

Stack an Object
```sh
stack -o [Cuboid|Cylinder|Prism]
```


Move the Robot
```sh
move -m [F|B|R|L] -mag [step_size]
```

Rotate a Joint
```sh
revolute -j [joint1|joint2|...|joint6] -deg [angle]
```


Move in a Specific Path
```sh
path -ml [circle|square|heart|hexagon]
```


Stack Multiple Objects
```sh
multistack -o [Cuboid|Cylinder|Prism] [Cuboid|Cylinder|Prism]
```


Exit Command
To exit the CLI, type:
```sh
exit
```
This will put the robot "back to sleep."
