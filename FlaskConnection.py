from flask import Flask, jsonify
from flask_cors import CORS
from game_codev2 import (intro, tutorial,
                         get_current_passenger_data,
                         get_current_passenger_passport,
                         get_current_status,
                         get_current_passenger_age,
                         get_current_ticket_data,
                         handle_decision,
                         get_boost_status,
                         use_boost, get_current_passenger_full_data)

app = Flask(__name__)
CORS(app)

@app.route('/intro')
def intro_route():
    return jsonify(intro())
@app.route('/tutorial')
def tutorial_route():
    return jsonify(tutorial())
@app.route('/description')
def description_route():
    return jsonify(get_current_passenger_data())

@app.route('/passport')
def passport_route():
    return jsonify(get_current_passenger_passport())

@app.route('/status')
def status_route():
    return jsonify(get_current_status())

@app.route('/ticket')
def ticket_rouse():
    return jsonify(get_current_ticket_data())
@app.route('/age')
def age_route():
    return jsonify(get_current_passenger_age())
@app.route('/approve')
def approve_route():
    return jsonify(handle_decision("approve"))
@app.route('/deny')
def deny_route():
    return jsonify(handle_decision("deny"))
@app.route('/boost')
def boost_route():
    return jsonify(get_boost_status())

@app.route('/current-passenger')
def current_passenger_route():
    return jsonify(get_current_passenger_full_data())
@app.route('/use-boost')
def use_boost_route():
    return jsonify(use_boost())


if __name__ == '__main__':
    app.run(debug=True)

