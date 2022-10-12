from flask import Flask, request, jsonify
import sqlite3 as sql
import json

DB = "./database.db"
app = Flask(__name__)

# Used to set up the connection to the database or create one if it doesn't yet exist.
def get_con_cur(table_name):
    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("create table if not exists {} (RATING real, DISH_NAME text, RESTURAUNT text, LOCATION test, NUM_RATINGS integer)".format(table_name))
    return con, cur

# GET endpoint that just serves as a landing page.
@app.route("/")
def welcome_screen():
    return "<p>Hot chicken rating API!</p>"

# GET endpoint to list all current ratings of chickens.
# $ curl "localhost:5000/hot_chickens"
@app.route('/hot_chickens', methods = ['GET'])
def hot_chickens():
    con, cur = get_con_cur("Ratings")
    cur.execute("select * from Ratings")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return json.dumps( [dict(x) for x in rows] )

# POST endpoint to add a new chicken dish rating to the list of rateable dishes..
# $ curl -X POST -H "Content-type: application/json" -d "{\"RATING\" : 9.2, \"DISH_NAME\" : \"Nashvilles_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers\", \"LOCATION\" : \"Nashville\"}" "localhost:5000/new_chicken_rate"
@app.route('/new_chicken_rate', methods = ['POST'])
def new_chicken_rate():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        con, cur = get_con_cur("Ratings")
        if not ("RATING" in json and "DISH_NAME" in json and "RESTURAUNT" in json and "LOCATION" in json):
            return "Please provide a RATING, DISH_NAME, RESTURAUNT, and LOCATION to add a new chicken rating.\n"
        chicken = (json["RATING"], json['DISH_NAME'], json['RESTURAUNT'], json['LOCATION'], 1)
        sql = ''' INSERT INTO Ratings(RATING,DISH_NAME,RESTURAUNT,LOCATION,NUM_RATINGS) VALUES(?,?,?,?,?) '''     
        cur.execute(sql, chicken)
        con.commit()
        con.close()
        
        return "Thanks for your hot chicken rating! Use the endpoint '/hot_chickens' to see how it compares to the competition!\n"
    else:
        return 'Content-Type not supported!'

# PUT endpoint to judge existing ranked chicken meals that have already been rated before.
# $ curl -X PUT -H "Content-type: application/json" -d "{\"RATING\" : 2.1, \"DISH_NAME\" : \"Nashvilles_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers\", \"LOCATION\" : \"Nashville\"}" "localhost:5000/rate_existing_chicken"
@app.route('/rate_existing_chicken', methods = ['PUT'])
def rate_existing_chicken():
    new_rating = request.json
    if not ("RATING" in new_rating and "DISH_NAME" in new_rating and "RESTURAUNT" in new_rating and "LOCATION" in new_rating):
        return "Please provide a RATING, DISH_NAME, RESTURAUNT, and LOCATION to rate an existing chicken.\n"
    con, cur = get_con_cur("Ratings")
    cur.execute("select * from Ratings")
    rows = cur.fetchall()
    lod = [dict(x) for x in rows]
    changed = False
    for ii in lod:
        if ii["DISH_NAME"] == new_rating["DISH_NAME"] and ii["RESTURAUNT"] == new_rating["RESTURAUNT"] and ii["LOCATION"] == new_rating["LOCATION"]:
            new_score = (((ii["RATING"] * ii["NUM_RATINGS"]) + new_rating["RATING"]) / (ii["NUM_RATINGS"] + 1))
            new_num_ratings = ii["NUM_RATINGS"] + 1
            cur.execute(''' UPDATE Ratings SET RATING = '''+str(new_score)+''', NUM_RATINGS = '''+str(new_num_ratings)+''' WHERE DISH_NAME = "'''+ii["DISH_NAME"]+'''";''')
    con.commit()
    con.close()
    return "Your rating has been applied to the existing hot chicken you tried!\n"

# POST endpoint to alert the community to the presence of a new hot chicken to consume.
# $ curl -X POST -H "Content-type: application/json" -d "{\"DISH_NAME\" : \"Nashvilles_Other_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers2\", \"LOCATION\" : \"Pheonix\"}" "localhost:5000/chicken_alert"
@app.route('/chicken_alert', methods = ['POST'])
def chicken_alert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        con, cur = get_con_cur("Alerts")
        if not ("DISH_NAME" in json and "RESTURAUNT" in json and "LOCATION" in json):
            return "Please provide a DISH_NAME, RESTURAUNT, and LOCATION to add a new chicken alert.\n"
        chicken = (0.0, json['DISH_NAME'], json['RESTURAUNT'], json['LOCATION'], 0)
        sql = ''' INSERT INTO Alerts(RATING,DISH_NAME,RESTURAUNT,LOCATION,NUM_RATINGS) VALUES(?,?,?,?,?) '''
        cur.execute(sql, chicken)
        con.commit()
        con.close()

        return "Thanks for your hot chicken alert! Use the endpoint '/list_chicken_alerts' to see all of the existing alerts!\n"
    else:
        return 'Content-Type not supported!'

# GET endpoint to list all alerts of new chicken dishes to eat and rate.
# $ curl "localhost:5000/list_chicken_alerts"
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
