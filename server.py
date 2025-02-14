from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import socket
app = Flask(__name__)
CORS(app)
from T import *
#obj=cuboid,prism,cylinder

# Assume these methods are already defined


curr_object=""

@app.route('/')
def get_client_ip():
    # Get the local IP address of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connects to an external server
        ip = s.getsockname()[0]  # Gets the assigned IP
    except Exception:
        ip = "127.0.0.1"  # Fallback
    finally:
        s.close()
    return ip+":8000"

@app.route('/verify/')
def verify():
    return {'message' : "InteractiveRobotics"}

@app.route('/pickup', methods=['POST'])
def api_pickup():
    global curr_object
    if curr_object:
        drop()
    curr_object=""
    print(request)
    data = request.json
    print(data)
    obj = data.get("object") 
    obj=obj.capitalize()
    print(obj)  
    if obj :
        curr_object=obj
        obj="/"+obj
        print(obj)
        print("reachedhere")
        pickup(obj)
        print("2")
        result = "successful"
        return jsonify({"result": result})
    elif (not obj):
        return jsonify({"error": "Missing object in request"}), 400

@app.route('/drop', methods=['POST'])
def api_drop():
    global curr_object
    if (curr_object):
        drop()
        curr_object=""
        result = "successful"
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Pls pick an object first"}),400


@app.route('/stack', methods=['POST'])
def api_stack():
    global curr_object
    print(curr_object+"hello")
    data = request.json
    second_object = data.get("object")
    if curr_object:
        drop()
    if second_object:
        print(2)
        if second_object!=curr_object:
            print(3)
            second_object="/"+second_object
            stack(second_object)
            curr_object=""
            result = "successful" 
            return jsonify({"result": result})
        else:
            return jsonify({"error": "select different object"}), 400

    else:
        return jsonify({"error": "Missing 'second_object' in request"}), 400


@app.route('/move', methods=['POST'])
def api_move():
    data = request.json
    direction = data.get("direction")
    m = data.get("magnitude")
    if direction not in ["F","B","R","L"]:
        return jsonify({"error": "Wrong direction"}), 400
    x,y,z=map(float,getTipPosition())
    if(direction=="F"):
        y=y+m*y/(math.sqrt(x*x+y*y))
        x=x+m*x/(math.sqrt(x*x+y*y))
    elif(direction=="B"):
        y=y-m*y/(math.sqrt(x*x+y*y))
        x=x-m*x/(math.sqrt(x*x+y*y))
    elif(direction=="L"):
        x=x-m*y/(math.sqrt(x*x+y*y))
        y=y+m*x/(math.sqrt(x*x+y*y))
    elif(direction=="R"):
        x=x+m*y/(math.sqrt(x*x+y*y))
        y=y-m*x/(math.sqrt(x*x+y*y))
    
    moveLine([x,y,z])
    result = "successful"
    return jsonify({"result": result})
    
        

@app.route('/joint1', methods=['POST'])
def api_joint1():
    data = request.json
    print("reachedhere")
    degree = data.get("degree")
    if degree is None:      
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(1, degree)
    result = "successful"
    return jsonify({"result": result})

@app.route('/joint2', methods=['POST'])
def api_joint2():
    data = request.json
    degree = data.get("degree")
    if degree is None:
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(2, degree)
    result = "successful"
    return jsonify({"result": result})

@app.route('/joint3', methods=['POST'])
def api_joint3():
    data = request.json
    degree = data.get("degree")
    if degree is None:
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(3, degree)
    result = "successful"
    return jsonify({"result": result})

@app.route('/joint4', methods=['POST'])
def api_joint4():
    data = request.json
    degree = data.get("degree")
    if degree is None:
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(4, degree)
    result = "successful"
    return jsonify({"result": result})

@app.route('/joint5', methods=['POST'])
def api_joint5():
    data = request.json
    degree = data.get("degree")
    if degree is None:
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(5, degree)
    return jsonify({"result": "successful"})

@app.route('/joint6', methods=['POST'])
def api_joint6():
    data = request.json
    degree = data.get("degree")
    if degree is None:
        return jsonify({"error": "Missing 'degree' field"}), 400
    moveJoint(6, degree)    
    result = "successful"
    return jsonify({"result": result})


@app.route('/movebycoordinates', methods=['POST'])
def api_movebycoordinates():
    data = request.json
    # Retrieve list input and scale each element by dividing by 100
    x, y, z = data.get("l")
    x = float(x) / 100
    y = float(y) / 100
    z = float(z) / 100
    x1, y1, z1 = getTipPosition()
    if ((x*x1 + y*y1) > 0):
        moveLine([x, y, z])
    else:
        moveArc([x, y, z])
    result = "successful"
    return jsonify({"result": result})

def moveinpath( path_type, radius,centre):
    if path_type == "circle":
        drawCircle(centre,radius)
    elif path_type == "square":
        drawSquare(centre,radius)
    elif path_type=="hexagon":
        drawHexagon(centre,radius)
        return "Unsupported path type"
    return "successful"

@app.route('/moveinpath', methods=['POST'])
def api_moveinpath():
    data = request.json
    path_type = data.get("path")
    x,y,z=getTipPosition()
    r = 0.2
    centre=[0,0.5,0.4]
    if path_type is None:
        return jsonify({"error": "Missing path"}), 400
    if path_type == "circle":
            r=0.15
            moveinpath(path_type, r, centre)
    elif path_type == "square":
        moveinpath( path_type, r,centre)
    elif path_type == "hexagon":
        r=0.15

        moveinpath(path_type, r, centre)

    elif path_type == "heart":
        drawHeart()

    else:
        return jsonify({"error": "Unsupported path type"}), 400
    return jsonify({"result": "successful"})



@app.route('/alljoints', methods=['POST'])
def api_alljoints():
    data = request.json
    degree = data.get("degree")
    print(degree)
    moveJoints(degree)
    return {"result": "successful"}

@app.route('/getcoordinates', methods=['POST'])
def api_getcoordinates():
    data = request.json
    target = data.get("target")
    if not target:
        return jsonify({"error": "Missing 'target' field"}), 400

    # If target is a joint (e.g., "joint1"), use a simple static mapping.
    if target.startswith("joint"):
        i=int(target[5])-48
        l=getJointPositions
        if i in range(1,7):
            coordinates = l[i]
        else:
            return jsonify({"error": "Invalid joint target"}), 400
    else:
        obj =  "/" + target
        coordinates = getObjectPosition(obj)
    result = "successful"
    return jsonify({"coordinates": coordinates})



@app.route('/stacktheobjects', methods=['POST'])
def api_stacktheobjects():
    global curr_object
    data = request.json
    obj = data.get("objects")
    if curr_object:
        drop()
        curr_object=""
    for i in range(1,len(obj)):
        obj[i]=obj[i].capitalize()
        obj[i-1]=obj[i-1].capitalize()
        stacktheobjects(f"/{obj[i]}",f"/{obj[i-1]}")
    result="successful"
    return jsonify({"result": result})

@app.route('/getalljoints', methods=['GET'])
def api_getalljoints():
    joint_positions = getJointPositions()  
    result = "successful"
    jointPosDeg = list(map(lambda x : round(x*180/3.14159, 2), joint_positions))
    return jsonify({"result": result, "joint_positions": jointPosDeg})

@app.route('/getalljoints2', methods=['GET'])
def api_getalljoints2():
    joint_positions = getJointPositions()  
    result = "successful"
    jointPosDeg = list(map(lambda x : round(x*180/3.14159, 2), joint_positions))
    jointPosDeg.append(round(getFingerAngle(), 2))
    jointPosDeg.append(getGripperState())

    return jsonify({"result": result, "joint_positions": jointPosDeg})

@app.route('/moveobject', methods=['POST'])
def api_moveobject11():
    global curr_object
    data = request.json
    obj = data.get("object")
    obj.capitalize()
    obj = "/" + obj
    # Retrieve list input and scale each element by dividing by 100
    x, y, z = data.get("l")
    x = float(x) / 100
    y = float(y) / 100
    z = float(z) / 100
    if curr_object:
        drop()
        curr_object = ""
    pickup(obj)
    x1, y1, z1 = getTipPosition()
    if ((x*x1 + y*y1) > 0):
        moveLine([x, y, z])
    else:
        moveArc([x, y, z])
    result = "successful"
    return jsonify({"result": result})

@app.route('/gripperclose', methods=['POST'])
def api_gripperclose():
    gripperClose()  
    result = "successful"
    return jsonify({"result": result})

@app.route('/gripperopen', methods=['POST'])
def api_gripperopen():
    gripperOpen() 
    result = "successful"
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=False)



