# Flask API for Twitter Client (https://github.com/jstefanska/twitter_client)

API created in Flask to use Python batch application for getting Tweets - https://github.com/jstefanska/twitter_client. API has Swagger UI, it's using Redis library to connect to Redis database.

## Redis database and environment variables

First you need to create Redis database using e.g. Docker. Here you can find Dockerfile and Redis config with authorization password I used: https://github.com/jstefanska/flask_api/tree/master/Redis
Then you need to create environment variables on your system, otherwise API won't work.


You need **DB_PORT**, **DB_HOST** and **DB_PASS**.

## API 
With this API, you can POST a hashtag with which you want to find Tweets, GET Tweets with the chosen hashtag and POST Tweet ID to vote for the Tweet you liked the most.
E.g.:
- POST curl to add hashtag "doggo" for Windows

curl -i -X POST -H "Content-Type: application/json" -d "{\"value\":\"doggo\"}" http://127.0.0.1:5000/hashtag

- GET curl with header to get tweets with hashtag "doggo" for Windows

curl -i -H "Accept: application/json" http://127.0.0.1:5000/tweets/doggo

- POST curl to vote for Tweet with chosen ID

curl -i -X POST -H "Content-Type: application/json" -d "{\"value\":\"1234784584443\"}" http://127.0.0.1:5000/vote

You can run it easily with Swagger UI - templates and static files for Swagger UI can be found in the project.


After POST request make sure https://github.com/jstefanska/twitter_client/tree/master runs. twitter_client and this Flask API are designed to run on Openshift, so you can run twitter_client as cron_job in Openshift: https://github.com/jstefanska/twitter_client/blob/master/Openshift/twitter-client-job-cron.yaml

Twitter client will always return 10 most recent Tweets with the hashtag of your choice.
