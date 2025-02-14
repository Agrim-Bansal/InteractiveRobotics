# Interactive Robotics
This is a project where a simulation running on coppleiasim is controlled by various interfaces.
The robot has 7 degrees of freedom and is controlled by a python script that sends commands to the robot. This script in turn accepts commands from various interfaces like a web interface, a voice interface and a terminal interface.


# Web Interface
## Getting Started
First install the dependencies:

```bash
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
The webapp has 5 tabs : Joint Control, Arm Control, Object Control, Stacking and Macros.
 - Joint Control: Allows you to control the robot's joints individually in degrees.
 - Arm Control: Allows you to control the robot's end effector in 3D space with coordinates.
 - Object Control: Allows you to manipulate the objects in the simulation - pick them up, move them somewhere or drop an object.
 - Stacking: Allows you to stack objects on top of each other.
 - Macros: Allows you to run the robot along a pre-defined path.