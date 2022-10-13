# Hot Chicken REST API!

### Purpose:
Last year I was asked in a technical interview to build and document an REST API with a couple different endpoints and a backend database. At the time, doing this all in 24 hours seemed out of my reach. In one of my first grad courses, however, I was given the opportunity to choose this as one of my midterm projects, so I jumped at it. I have long wanted to get some experience with building API's and databases. This project allowed me to do that and get some closure on that failed technical interview.

This is a REST API to rate the hot chicken dishes I have eaten in various locations, and to track the ones that I saw but haven't gotten to eat just yet. I most likely won't be filling in the database here with my food because I'm mainly posting this just for my own reference in the future and for other people to have a good example of a very simple REST API with a SQLite backend and a couple diverse endpoints. 

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
