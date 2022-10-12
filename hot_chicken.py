from flask import Flask, request, jsonify
import sqlite3 as sql
import json

DB = "./database.db"
app = Flask(__name__)

def get_con_cur(table_name):
    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("create table if not exists {} (RATING real, DISH text, RESTURAUNT text, LOCATION test, NUM_RATINGS integer)".format(table_name))
    return con, cur

# GET endpoint that just lists the purpose of the app and its different endpoints.
@app.route("/")
def welcome_screen():
    return "<p>Hot chicken ratings!</p>"

# GET endpoint to list all current ratings of chickens.
@app.route('/hot_chickens', methods = ['GET'])
def hot_chickens():
    con, cur = get_con_cur("Ratings")
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

        con, cur = get_con_cur("Ratings")
        if not ("RATING" in json and "DISH" in json and "RESTURAUNT" in json and "LOCATION" in json):
            return "Please provide a RATING, DISH, RESTURAUNT, and LOCATION to add a new chicken rating.\n"
        chicken = (json["RATING"], json['DISH'], json['RESTURAUNT'], json['LOCATION'], 1)
        sql = ''' INSERT INTO Ratings(RATING,DISH,RESTURAUNT,LOCATION,NUM_RATINGS) VALUES(?,?,?,?,?) '''     
        cur.execute(sql, chicken)
        con.commit()
        con.close()
        
        return "Thanks for your hot chicken rating! Use the endpoint '/hot_chickens' to see how it compares to the competition!\n"
    else:
        return 'Content-Type not supported!'

# PUT endpoint to judge existing ranked chicken meals that have already been rated before.
@app.route('/rate_existing_chicken', methods = ['PUT'])
def rate_existing_chicken():
    new_rating = request.json
    if not ("RATING" in json and "DISH" in json and "RESTURAUNT" in json and "LOCATION" in json):
        return "Please provide a RATING, DISH, RESTURAUNT, and LOCATION to rate an existing chicken.\n"
    con, cur = get_con_cur("Ratings")
    cur.execute("select * from Ratings")
    rows = cur.fetchall()
    con.commit()
    con.close()
    lod = json.dumps( [dict(x) for x in rows] )
    changed = False
    for ii in lod:
        if ii["DISH"] == new_rating["DISH"] and ii["RESTURAUNT"] == new_rating["RESTURAUNT"] and ii["LOCATION"] == new_rating["LOCATION"]:
            new_score = ((ii["RATING"] * ii["NUM_RATINGS"]) + new_rating["RATING"]) / ii["NUM_RATINGS"] + 1
            cur.execute(''' INSERT INTO Ratings(RATING,DISH,RESTURAUNT,LOCATION,NUM_RATINGS) VALUES (?,?,?,?,?) WHERE DISH={} AND RESTURAUNT={} AND LOCATION={}'''.format(ii["DISH"], ii["RESTURAUNT"], ii["LOCATION"]), (new_score, ii["DISH"], ii["RESTURAUNT"], ii["LOCATION"], ii["NUM_RATINGS"] + 1))
    con.commit()
    con.close()
    return "Your rating has been applied to the existing hot chicken you tried!\n"

# POST endpoint to alert the community to the presence of a new hot chicken to consume.
# $ curl -X POST -H "Content-type: application/json" -d "{\"DISH\" : \"Nashville's Hottest Chicken\", \"RESTURAUNT\" : \"Mr. Cluckers\", \"LOCATION\" : \"Nashville, TN\"}" "localhost:5000/chicken_alert"
@app.route('/chicken_alert', methods = ['POST'])
def chicken_alert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        con, cur = get_con_cur("Alerts")
        if not ("DISH" in json and "RESTURAUNT" in json and "LOCATION" in json):
            return "Please provide a DISH, RESTURAUNT, and LOCATION to add a new chicken alert.\n"
        chicken = (0.0, json['DISH'], json['RESTURAUNT'], json['LOCATION'], 0)
        sql = ''' INSERT INTO Alerts(RATING,DISH,RESTURAUNT,LOCATION,NUM_RATINGS) VALUES(?,?,?,?,?) '''
        cur.execute(sql, chicken)
        con.commit()
        con.close()

        return "Thanks for your hot chicken alert! Use the endpoint '/list_chicken_alerts' to see all of the existing alerts!\n"
    else:
        return 'Content-Type not supported!'

# GET endpoint to list all alerts of new chicken dishes to eat and rate.
@app.route('/list_chicken_alerts', methods = ['GET'])
def list_chicken_alerts():
    con, cur = get_con_cur("Alerts")
    cur.execute("select * from Alerts")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps( [dict(x) for x in rows] )

if __name__ == '__main__':
    app.run(debug = True)
