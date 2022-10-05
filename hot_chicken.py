from flask import Flask, request, jsonify
import sqlite3 as sql
import json

DB = "./database.db"
app = Flask(__name__)

# GET endpoint.
@app.route("/")
def welcome_screen():
    return "<p>Hot chicken rankings!</p>"

# GET endpoint.
@app.route('/leaderboard')
def loaderboard():
    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("create table if not exists Meals (RATING real, DISH text, RESTURAUNT text, LOCATION text)")
    cur.execute("select * from Meals")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps( [dict(x) for x in rows] )

# POST endpoint.
@app.route('/bounties')
def bounties():
    input_json = request.get_json(force = True)
    dictToReturn = {'text':input_json['text']}
    return jsonify(dictToReturn)

# PUT endpoint.
@app.route('/judge', methods = ['POST'])
def judge():
    input_json = request.get_json(force = True)
    dictToReturn = {'text':input_json['text']}
    return jsonify(dictToReturn)

# POST endpoint.
@app.route('/suggest')
def suggest():
    input_json = request.get_json(force = True)
    dictToReturn = {'text':input_json['test']}
    return jsonify(dictToReturn)
    
if __name__ == '__main__':
    app.run(debug = True)
