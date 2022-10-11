from flask import Flask, request, jsonify
import sqlite3 as sql
import json

DB = "./database.db"
app = Flask(__name__)

def get_con_cur():
    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("create table if not exists Ratings (RATING real, DISH text, RESTURAUNT text, LOCATION test)")
    return con, cur

# GET endpoint that just lists the purpose of the app and its different endpoints.
@app.route("/")
def welcome_screen():
    return "<p>Hot chicken ratings!</p>"

# GET endpoint to list all current ratings of chickens.
@app.route('/hot_chickens')
def hot_chickens():
    con, cur = get_con_cur()
    cur.execute("select * from Ratings")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps( [dict(x) for x in rows] )

# POST endpoint to add a new chicken dish to the list to be rated by everyone.
# $ curl -X POST -H "Content-type: application/json" -d "{\"RATING\" : 9.2, \"DISH\" : \"Nashville's Hottest Chicken\", \"RESTURAUNT\" : \"Mr. Cluckers\", \"LOCATION\" : \"Nashville, TN\"}" "localhost:5000/new_chicken_rate"
@app.route('/new_chicken_rate', methods = ['POST'])
def new_chicken_rate():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        con, cur = get_con_cur()
        if not ("RATING" in json and "DISH" in json and "RESTURAUNT" in json and "LOCATION" in json):
            return "Please provide a RATING, DISH, RESTURAUNT, and LOCATION to add a new chicken rating.\n"
        chicken = (json["RATING"], json['DISH'], json['RESTURAUNT'], json['LOCATION'])
        sql = ''' INSERT INTO Ratings(RATING,DISH,RESTURAUNT,LOCATION) VALUES(?,?,?,?) '''     
        cur.execute(sql, chicken)
        con.commit()
        
        return "Thanks for your chicken rating! Use the endpoint '/hot_chickens' to see how it compares to the competition!\n"
    else:
        return 'Content-Type not supported!'

# PUT endpoint to judge existing ranked chicken meals that have already been rated before.
@app.route('/rate_exisitng_chicken', methods = ['PUT'])
def rate_existing_chicken():
    input_json = request.get_json(force = True)
    dictToReturn = {'text':input_json['text']}
    return jsonify(dictToReturn)

# POST endpoint to alert the community to the presence of a new hot chicken to consume.
# $ curl -X POST -H "Content-type: application/json" -d "{\"mealName\" : \"Nashville's Hottest Chicken\", \"resturaunt\" : \"Mr. Cluckers\", \"location\" : \"Nashville, TN\"}" "localhost:5000/chicken_alert"
@app.route('/chicken_alert', methods = ['POST'])
def chicken_alert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

# GET endpoint to list all alerts of new chicken dishes to eat and rate.
@app.route('/list_chicken_alerts')
def list_chicken_alerts():
    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("create table if not exists Alerts (RATING real, DISH text, RESTURAUNT text, LOCATION text)")
    cur.execute("select * from Alerts")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps( [dict(x) for x in rows] )

# GET Endpoint that returns the rating for a specific chicken dish from a specific resturaunt..
@app.route('/get_specific_chicken', methods = ['GET'])
def get_specific_chicken():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
    
if __name__ == '__main__':
    app.run(debug = True)
