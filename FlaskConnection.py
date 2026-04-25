from flask import Flask, jsonify
from flask_cors import CORS
from game_codev2 import intro, tutorial

app = Flask(__name__)
CORS(app)

@app.route('/intro')
def intro_route():
    return jsonify(intro())

@app.route('/tutorial')
def tutorial_route():
    return jsonify(tutorial())


if __name__ == '__main__':
    app.run(debug=True)
