from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)

#obj=cuboid,prism,cylinder


curr_object=""

@app.route('/pickup', methods=['POST'])
def api_pickup():
    data = request.json
    obj = data.get("object")
    obj="/"+obj
    
    if obj and (not curr_object):
        curr_object=obj
        result = pickup(obj)
        return jsonify({"result": result})
    elif (not obj):
        return jsonify({"error": "Missing object in request"}), 400
    else:
        return jsonify({"error": "Already an object has been picked,first drop it"}),400

@app.route('/drop', methods=['POST'])
def api_drop():
    if (not curr_object):
        result = drop()
        curr_object=""
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Pls pick an object first"}),400


@app.route('/stack', methods=['POST'])
def api_stack():
    data = request.json
    second_object = data.get("second_object")
    if curr_object:
        if second_object:
            if second_object!=curr_object:
                second_object="/"+second_object
                result = stack(second_object)
                curr_object=""
                return jsonify({"result": result})
            else:
                return jsonify({"error": "select different object"}), 400

        else:
            return jsonify({"error": "Missing 'second_object' in request"}), 400
    else:
        return jsonify({"error": "pick an object first"}), 400

@app.route('/move', methods=['POST'])
def api_move():
    data = request.json
    direction = data.get("direction")
    if direction not in ["F","B","R","L"]:
        result = move(direction)
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Wrong direction"}), 400

@app.route('/joint1', methods=['POST'])
def api_joint1():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint1(direction)
    return jsonify({"result": result})

@app.route('/joint2', methods=['POST'])
def api_joint2():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint2(direction)
    return jsonify({"result": result})

@app.route('/joint3', methods=['POST'])
def api_joint3():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint3(direction)
    return jsonify({"result": result})

@app.route('/joint4', methods=['POST'])
def api_joint4():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint4(direction)
    return jsonify({"result": result})

@app.route('/joint5', methods=['POST'])
def api_joint5():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint5(direction)
    return jsonify({"result": result})

@app.route('/joint6', methods=['POST'])
def api_joint6():
    data = request.json
    direction = data.get("direction")
    if direction not in ("F", "B"):
        return jsonify({"error": "Missing or invalid 'direction'"}), 400
    result = joint6(direction)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)


