from flask import Flask, jsonify
from transector import Transector
import os

transector = Transector()
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"foods": transector.get_all_foods()})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))