from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS to allow external requests

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_data(data):
    received_data = load_data()
    received_data.append(data)
    with open(DATA_FILE, "w") as file:
        json.dump(received_data, file)

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        save_data(data)
        return jsonify({"message": "Data received successfully!"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/display', methods=['GET'])
def display_data():
    received_data = load_data()

    if not received_data:
        return "<h1>No data received yet.</h1>"

    last_entry = received_data[-1]
    result = "<h1>Received Data</h1>"
    result += f"<p>Name: {last_entry.get('name', 'N/A')}, Email: {last_entry.get('email', 'N/A')}</p>"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
