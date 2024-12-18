from flask import Flask, jsonify
import os
from lightfm import LightFM

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "LIghtFM"})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))