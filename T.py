from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math
import time
import json

# for 7-DOF robot

PICKUP_PRESETS = {
    '': (0,0,0),
    '/Cuboid': (0.05, 0, 0.1),
    '/Cup': (0.07, 30, 0.05),
    '/Bowl': (0.08, 30, 0.1),
    '/Prism': (0.1, 15, 0.15),
    '/Cross': (0.1, 15, 0.15),
    '/Cylinder': (0.03, 0, 0.1),
    '/Pot': (0.09, 20, 0.1),
    '/Saucer': (0.06, 20, 0.04)
}


client = RemoteAPIClient()
sim = client.require('sim')
simIK = client.require('simIK')


target = sim.getObject('/manipulationSphere')
tip = sim.getObject('/tip')
GRIPPER = sim.getObject('/BarrettHand')
GRIPPER_CONT = sim.getScript(sim.scripttype_simulation, '/BarrettHand/GripperController')
IK_SCRIPT = sim.getScript(sim.scripttype_simulation, '/IRB140/IKScript')
CONNECTOR = sim.getObject('/BarrettHand/attachPoint')
CURRENT_PICKED_OBJECT = -1


def easeInOutSquare(cur, target, t):
    """
    Easing function for smooth acceleration and deceleration.

    :param t: normalized time value between 0 and 1
    :return: eased time value between 0 and 1
    """

    p = t*t / (t*t + (1 - t)*(1 - t))
    res = []
    for i in range(3):
        res.append(cur[i] + (target[i] - cur[i])*p)
    
    return res

def ikOn():
    sim.setObjectPosition(target, -1, sim.getObjectPosition(tip, -1))
    sim.setObjectOrientation(target, -1, sim.getObjectOrientation(tip, -1))
    sim.callScriptFunction('ikOn', IK_SCRIPT)

def ikOff():
    sim.callScriptFunction('ikOff', IK_SCRIPT)

def moveLine(TARGET_POS, delay = 0, stepsPerUnit = 500):
    ikOn()
    # Get the current position of the target dummy
    CURRENT_POS = sim.getObjectPosition(tip, -1)
    
    print(type(CURRENT_POS[0]))
    print(type(TARGET_POS[0]))
    # Compute the path
    dist = math.sqrt(sum([(TARGET_POS[i] - CURRENT_POS[i])**2 for i in range(3)]))
    steps = int(stepsPerUnit * dist)
    path = [easeInOutSquare(CURRENT_POS, TARGET_POS, i/steps) for i in range(steps)]
    # Follow the path
    for i in range(len(path)):
        sim.setObjectPosition(target, -1, path[i])
        time.sleep(delay / steps)

def moveArc(POS, delay=0, stepsPerUnit=500):
    if(abs(POS[0]) < 0.0001):
        angle = math.pi/2 if POS[1] > 0 else -math.pi/2
    else:
        angle = math.tanh(POS[1]/POS[0])
    moveJoint(1, angle*180/math.pi)
    time.sleep(1)
    moveLine(POS, delay=0.2, stepsPerUnit=stepsPerUnit)



def pickup(name, delay=0, stepsPerUnit=500, fingerAngle=30):
    # Get the current position of the target dummy
    moveJoints([None, 0, 0, 0, -90, None])
    z, fingerAngle, ctocdist = PICKUP_PRESETS[name]
    sim.callScriptFunction('fingerAngle', GRIPPER_CONT, fingerAngle)
    obj = sim.getObject(name)
    POS = sim.getObjectPosition(obj, -1)
    POS[2] = POS[2] + z
    moveArc(POS)
    sim.callScriptFunction('close', GRIPPER_CONT)
    time.sleep(1)
    sim.setObjectParent(sim.getObject(name), CONNECTOR, True)
    POS[2] = POS[2] + 0.2
    moveLine(POS)

    global CURRENT_PICKED_OBJECT
    CURRENT_PICKED_OBJECT = name

def drop():
    global CURRENT_PICKED_OBJECT
    sim.callScriptFunction('open', GRIPPER_CONT)
    if(CURRENT_PICKED_OBJECT != -1):
        sim.setObjectParent(sim.getObject(CURRENT_PICKED_OBJECT), -1)
        CURRENT_PICKED_OBJECT = -1
    time.sleep(0.5)

def stack(onObjName):
    moveJoints([None, 0, 0, 0, -90, None])
    onObj = sim.getObject(onObjName)
    moveJoints([None, 0, 0, 0, -90, None])
    POS = sim.getObjectPosition(onObj, -1)
    POS[2] = POS[2] + 0.21
    moveArc(POS)
    drop()
    POS[2] = POS[2] + PICKUP_PRESETS[onObjName][2] + 0.11 - PICKUP_PRESETS[CURRENT_PICKED_OBJECT][2]

    moveLine(POS)

def stacktheobjects(name, onObjName):
    obj = sim.getObject(name)
    onObj = sim.getObject(onObjName)
    pickup(name)
    moveJoints([None, 0, 0, 0, -90, None])
    POS = sim.getObjectPosition(onObj, -1)
    POS[2] = POS[2] + PICKUP_PRESETS[name][0] + PICKUP_PRESETS[onObjName][2] + 0.01
    moveArc(POS)
    drop()
    POS[2] = POS[2] + 0.2
    moveLine(POS)
    

def moveJoint(joint_num, desired_angle):
    ikOff()
    joint_handle = sim.getObjectHandle(f'IRB140_joint{joint_num}')
    d_a_r=desired_angle*math.pi/180
    sim.setJointTargetPosition(joint_handle,d_a_r)

def moveJoints(desired_angles):
    for i in range(6):
        if(desired_angles[i] != None):
            moveJoint(i+1, desired_angles[i])

def moveJointBy(joint_num, angle):
    joint_handle = sim.getObjectHandle(f'IRB140_joint{joint_num}')
    des_A = sim.getJointPosition(joint_handle)*180/math.pi + angle
    moveJoint(joint_num, des_A)

def getJointPositions():
    joint_handles = [sim.getObjectHandle(f'IRB140_joint{i+1}') for i in range(6)]
    return [sim.getJointPosition(j) for j in joint_handles]

def getTipPosition():
    return sim.getObjectPosition(tip, -1)

def getObjectPosition(name):
    return sim.getObjectPosition(sim.getObject(name), -1)

def gripperClose():
    sim.callScriptFunction('close', GRIPPER_CONT)

def gripperOpen():
    sim.callScriptFunction('open', GRIPPER_CONT)

def drawCircle(center, radius):
    ikOn()
    CURRENT_POS = sim.getObjectPosition(tip, -1)
    START_POS = [center[0] + radius, center[1], center[2]]
    moveArc(START_POS)
    path = []
    steps = 360
    for i in range(steps + 1):
        angle = 2 * math.pi * i / steps
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        z = center[2]
        path.append([x, y, z])
    # Follow the path
    for i in range(len(path)):
        sim.setObjectPosition(target, -1, path[i])
        time.sleep(0.01)

# def drawVerticalCircle(center, radius):
#     ikOn()
#     CURRENT_POS = sim.getObjectPosition(tip, -1)
#     START_POS = [center[0] + radius, center[1], center[2]]
#     moveArc(START_POS)
#     path = []
#     steps = 360
#     for i in range(steps + 1):
#         angle = 2 * math.pi * i / steps
#         x = center[0] 
#         y = center[1] + radius * math.sin(angle)
#         z = center[2] + radius * math.cos(angle)
#         path.append([x, y, z])
#     # Follow the path
#     for i in range(len(path)):
#         sim.setObjectPosition(target, -1, path[i])

def drawSquare(center, length):
    moveArc([center[0] + length/2, center[1] + length/2, center[2]], delay=0.2)
    moveLine([center[0] - length/2, center[1] + length/2, center[2]], delay=0.2)
    moveLine([center[0] - length/2, center[1] - length/2, center[2]], delay=0.2)
    moveLine([center[0] + length/2, center[1] - length/2, center[2]], delay=0.2)
    moveLine([center[0] + length/2, center[1] + length/2, center[2]], delay=0.2)

def drawHexagon(center, radius):
    moveArc([center[0] + radius, center[1], center[2]])
    for i in [1,2,3,4,5,0]:
        moveLine([center[0] + radius * math.cos(i * math.pi / 3), center[1] + radius * math.sin(i * math.pi / 3), center[2]], delay=0.15)

def drawHeart():
    ikOn()
    CURRENT_POS = sim.getObjectPosition(tip, -1)
    center = CURRENT_POS
    path = []
    steps = 1000
    for i in range(steps + 1):
        t = i / steps * 2 * math.pi
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        path.append([center[0] + x * 0.01, center[1] + y * 0.01, center[2]])
    # Follow the path
    for i in range(len(path)):
        sim.setObjectPosition(target, -1, path[i])
        time.sleep(0.001)

sim.callScriptFunction('open', GRIPPER_CONT)
# pickup('/Cuboid', fingerAngle=0)
# moveLine([0, 0.5, 0.3])
# drop()


# moveJointBy(1, 90)
# time.sleep(1)
# moveJointBy(1, -90)
# time.sleep(1)
# moveJointBy(2, 90)
# time.sleep(1)
# moveJointBy(2, -90)
# time.sleep(1)
# moveJointBy(3, 90)
# time.sleep(1)
# moveJointBy(3, -90)
# time.sleep(1)
# moveJointBy(4, 90)
# time.sleep(1)
# moveJointBy(4, -90)
# time.sleep(1)
# moveJointBy(5, 90)
# time.sleep(1)
# moveJointBy(5, -90)
# time.sleep(1)
# moveJointBy(6, 90)
# time.sleep(1)
# moveJointBy(6, -90)
# time.sleep(1)

# stack('/Cuboid', '/Cylinder')
# stack('/Prism', '/Cuboid')
# print(getJointPositions())
# drawCircle([0.3, 0.4, 0.5], 0.2)