# Hot Chicken REST API!

### Purpose:
I am a huge hot chicken fan and I built this app to track all of the chicken I eat and hear about. Feel free to contribute to the repository of hot chickens.

### Setup:
When launching this API locally, please do the following:
```
$ cd hot_chicken
$ . venv/bin/actviate
$ export FLASK_APP=hot_chicken
$ flask run
 * Running on http://127.0.0.1:5000/
```

If you run into any issues with those commands, please consult the flask documentation @ https://flask.palletsprojects.com/en/2.0.x/quickstart/

### Endpoints:
The following endpoints make up the api:
- '/': GET endpoint that just serves as a landing page.
- '/hot_chickens': GET endpoint to list all current ratings of chickens.
- '/new_chicken_rate': POST endpoint to add a new chicken dish rating to the list of rateable dishes.
- '/rate_existing_chicken': PUT endpoint to judge existing ranked chicken meals that have already been rated before.
- '/chicken_alert': POST endpoint to alert the community to the presence of a new hot chicken to consume.
- '/list_chicken_alerts': GET endpoint to list all alerts of new chicken dishes to eat and rate.

### Example Usage:
- $ curl "localhost:5000/"
- $ curl "localhost:5000/hot_chickens"
- $ curl -X POST -H "Content-type: application/json" -d "{\"RATING\" : 9.2, \"DISH_NAME\" : \"Nashvilles_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers\", \"LOCATION\" : \"Nashville\"}" "localhost:5000/new_chicken_rate"
- $ curl -X PUT -H "Content-type: application/json" -d "{\"RATING\" : 2.1, \"DISH_NAME\" : \"Nashvilles_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers\", \"LOCATION\" : \"Nashville\"}" "localhost:5000/rate_existing_chicken"
- $ curl -X POST -H "Content-type: application/json" -d "{\"DISH_NAME\" : \"Nashvilles_Other_Hottest_Chicken\", \"RESTURAUNT\" : \"Cluckers2\", \"LOCATION\" : \"Pheonix\"}" "localhost:5000/chicken_alert"
- $ curl "localhost:5000/list_chicken_alerts"
