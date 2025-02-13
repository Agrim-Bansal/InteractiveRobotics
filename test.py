import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/send_post', methods=['GET'])
def send_post_request():
    l=[0.1,0.2,0.05]
    url = "http://127.0.0.1:8000/moveobject"  # Replace with the actual URL
    data = {"object": "Cylinder","l":l} # Data to send

    response = requests.post(url, json=data)  # Sending JSON data

    return jsonify({"status": response.status_code, "response": response.text})
@app.route('/send_post1', methods=['GET'])
def send_post_request1():
    l=["Cuboid","Cylinder","Prism"]
    url = "http://127.0.0.1:8000/pickup"  # Replace with the actual URL
    data = {"object": "Cylinder"}  # Data to send

    response = requests.post(url, json=data)  # Sending JSON data

    return jsonify({"status": response.status_code, "response": response.text})

if __name__ == '__main__':
    print("1")
    app.run(port="4000",debug=True)