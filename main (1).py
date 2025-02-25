from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask("ESP32-INNOGREEN")

uri = "mongodb+srv://ESP32-INNOGREEN:samsungindonesia_bisa@esp32-innogreen.depxs.mongodb.net/?retryWrites=true&w=majority&appName=ESP32-INNOGREEN"
client = MongoClient(uri)
db = client.mydataubidots
collection = db.InnoGreen

@app.route("/")
def home():
    return "Server is running!"

@app.route("/", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()
        result = collection.insert_one(data)
        return jsonify({"status": "success", "inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET', 'POST'])
def get_all_data():
    if request.method == "POST":
        try:
            data = request.get_json()
            return jsonify({"status": "success", "received": data}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:  # GET
        try:
            data = list(collection.find({}))
            for item in data:
                item["_id"] = str(item["_id"])
            return jsonify({"status": "success", "data": data}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

