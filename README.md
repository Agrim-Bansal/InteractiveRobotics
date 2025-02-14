# Interactive Robotics
### _Team: Tech Wale Thekedaar_
This is a project where a simulation running on coppleiasim is controlled by various interfaces.
The robot has 7 degrees of freedom and is controlled by a python script that sends commands to the robot. This script in turn accepts commands from various interfaces like a web interface, a voice interface and a terminal interface.

Note : Move to src directory and follow the commands for each respective interface.

# #CoppeliaSim Simulation - Setup
## Installation
Download and Install the CoppeliaSim from the official website: https://www.coppeliarobotics.com/downloads.
Load the scene InteractiveRobotics.ttt in CoppeliaSim.
Start the simulation by clicking on the play button.

## Server Setup
The server is a python http server-cum-script that listens for commands from the various interfaces and sends them to the CoppeliaSim simulation.
To run the server, install the required dependencies:
```bash
cd server
pip install -r requirements.txt
```
Then, run the server:
```bash
python server.py
```
The server will start running on port 8000. 

***To find the IP address of the server, visit http://localhost:8000 in your browser. The IP address will be displayed on the page.***

*** The Interfaces can run on any device on the same local network as the server. Following are the instructions to run the interfaces. ***s

# #Web Interface
## Getting Started
First move to the web-interface directory and install the dependencies:

```bash
cd web-interface
npm install
```

Second, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Usage
The web interface has a simple interface that allows you to control the robot.
At the very start, you will be asked to enter the IP address of the server running the CoppeliaSim simulation. 
Enter this in the box and click on the "Connect" button. (See above for finding IP address of the server)
The webapp has 5 tabs : Joint Control, Arm Control, Object Control, Stacking and Macros.
 - Joint Control: Allows you to control the robot's joints individually in degrees.
 - Arm Control: Allows you to control the robot's end effector in 3D space with coordinates.
 - Object Control: Allows you to manipulate the objects in the simulation - pick them up, move them somewhere or drop an object.
 - Stacking: Allows you to stack objects on top of each other.
 - Macros: Allows you to run the robot along a pre-defined path.

<br/>


# #CLI

Install the Dependencies
```sh
pip install requests tqdm colorama
```

Run the CLI

```sh
cd cli
python script.py
```

### Initiation
The program will ask for the IP address of the server running the CoppeliaSim simulation. Enter the IP address (See above on how to find it) and press Enter.

### Available Commands

| Command                | Syntax                                                                 |
|------------------------|-----------------------------------------------------------------------|
| Pick an Object         | `pick -o [Cuboid\|Cylinder\|Prism]`                                    |
| Stack an Object        | `stack -o [Cuboid\|Cylinder\|Prism]`                                   |
| Move the Robot         | `move -m [F\|B\|R\|L] -mag [step_size]`                                 |
| Rotate a Joint         | `revolute -j [joint1\|joint2\|...\|joint6] -deg [angle]`                |
| Move in a Specific Path| `path -ml [circle\|square\|heart\|hexagon]`                             |
| Stack Multiple Objects | `multistack -o [Cuboid\|Cylinder\|Prism] [Cuboid\|Cylinder\|Prism]`     |
| Exit Command           | `exit`                                                                 |


# #Voice Interface
## Installation & Setup

Move to directory and install Dependencies
```sh
pip install -r requirements.txt
```

Run the Streamlit App
```sh
cd voice-interface
streamlit run streamlit_app.py
```

1. The app will open in your default browser.
2. Enter your **API Key** in the sidebar.
3. Provide the **Flask Server URL**.
4. Click **Load Models** to start the system.

### **Voice/Typed Commands Supported**

| Command                                      | Description                                                                                           |
|----------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `JOINT{I} { "degree": <value> }`             | Moves joint I by the specified magnitude; positive means 'FORWARD', negative means 'BACKWARD'. |
| `PICKUP { "object": "Cuboid" , "Cylinder" , "Prism" , "Cup" , "Bowl" , "Pot" }` | Picks up the specified object. |
| `DROP {}`| Releases the currently held object.                                                                   |
| `STACK { "object": "<object_name>" }` | Stacks the given object on another.                                                                   |
| `MOVE { "direction": ["F", "B", "R", "L"], "magnitude": <value> }` | Moves the arm in the given direction(s) by the specified magnitude.                      |
| `MOVEINPATH { "path": "square" , "circle" , "hexagon" , "heart" }` | Moves the robotic arm along the specified path shape.                                      |
| `MOVEBYCOORDINATES { "l": [x, y, z] }`       | Moves the arm to the given (x, y, z) coordinates.                                                     |
| `MOVEOBJECT { "object": "Cuboid" , "Cylinder" , "Prism" , "Cup" , "Bowl" , "Pot", "l": [x, y, z] }` | Moves the specified object to the desired coordinates.  |
| `STACKTHEOBJECTS { "objects": [<list of objects>] }` | Stacks the objects one over the other in the specified order. |
