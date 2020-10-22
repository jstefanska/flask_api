from flask import Flask, abort, make_response, jsonify, request
import json
from flask_swagger import swagger
import redis
import os

app = Flask(__name__)


@app.route("/")
def spec():
    return jsonify(swagger(app))


@app.route('/hashtag', methods=['POST'])
def add_hashtag():
    data = json.loads(request.data)
    hashtag = data.get("value", None)

    if "#" in str(hashtag):
        abort(make_response(jsonify(message="Use a word without '#'. Application will take care of that."), 400))
    else:
        try:
            if 'DB_PASS' not in os.environ:
                print("'DB_PASS' environment variable does not exist")
                exit(1)
            elif 'DB_HOST' not in os.environ:
                print("'DB_HOST' environment variable does not exist")
                exit(1)
            elif 'DB_PORT' not in os.environ:
                print("'DB_PORT' environment variable does not exist")
                exit(1)
            else:
                db_pass = os.getenv('DB_PASS')
                db_host = os.getenv('DB_HOST')
                db_port = os.getenv('DB_PORT')

            r = redis.StrictRedis(
                host=db_host,
                port=db_port,
                password=db_pass,
                charset="utf-8",
                decode_responses=True)

            r.sadd('hashtags', hashtag)

            return "Database updated with hashtag: " + str(hashtag)

        except ConnectionError:
            abort(make_response(jsonify(message="Unable to connect to the database!"), 502))

        except redis.exceptions.ResponseError as ex:
            error_message = "Error: " + str(ex)
            abort(make_response(jsonify(message=error_message), 500))


@app.route('/tweets/<string:hashtag>', methods=['GET'])
def get_tweets_with_hashtag(hashtag):
    try:
        if 'DB_PASS' not in os.environ:
            print("'DB_PASS' environment variable does not exist")
            exit(1)
        elif 'DB_HOST' not in os.environ:
            print("'DB_HOST' environment variable does not exist")
            exit(1)
        elif 'DB_PORT' not in os.environ:
            print("'DB_PORT' environment variable does not exist")
            exit(1)
        else:
            db_pass = os.getenv('DB_PASS')
            db_host = os.getenv('DB_HOST')
            db_port = os.getenv('DB_PORT')

        r = redis.StrictRedis(
            host=db_host,
            port=db_port,
            password=db_pass,
            charset="utf-8",
            decode_responses=True)

        tweets_data = (r.lrange(hashtag, 0, 9))

        if not tweets_data:
            abort(make_response(jsonify(message="Database does not contain tweets with this hashtag."), 400))
        else:
            return jsonify(tweets_data)

    except ConnectionError:
        abort(make_response(jsonify(message="Unable to connect to the database!"), 502))

    except redis.exceptions.ResponseError as ex:
        error_message = "Error: " + str(ex)
        abort(make_response(jsonify(message=error_message), 500))


@app.route('/vote', methods=['POST'])
def vote_tweet_id():
    data = json.loads(request.data)
    tweet_id = data.get("value", None)

    try:
        if 'DB_PASS' not in os.environ:
            print("'DB_PASS' environment variable does not exist")
            exit(1)
        elif 'DB_HOST' not in os.environ:
            print("'DB_HOST' environment variable does not exist")
            exit(1)
        elif 'DB_PORT' not in os.environ:
            print("'DB_PORT' environment variable does not exist")
            exit(1)
        else:
            db_pass = os.getenv('DB_PASS')
            db_host = os.getenv('DB_HOST')
            db_port = os.getenv('DB_PORT')

        r = redis.StrictRedis(
            host=db_host,
            port=db_port,
            password=db_pass,
            charset="utf-8",
            decode_responses=True)

        r.incr(tweet_id, 1)
        votes = r.get(tweet_id)

        if int(votes) > 2:
            return "Tweet with id: " + tweet_id + " has " + votes + " votes."
        else:
            return "Tweet with id: " + tweet_id + " has " + votes + " vote."

    except ConnectionError:
        abort(make_response(jsonify(message="Unable to connect to the database!"), 502))

    except redis.exceptions.ResponseError as ex:
        error_message = "Error: " + str(ex)
        abort(make_response(jsonify(message=error_message), 500))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
