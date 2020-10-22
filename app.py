from flask import Flask, abort, make_response, jsonify, request
import json
import psycopg2
from psycopg2 import sql
import os
from flask_swagger import swagger

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
            elif 'DB_NAME' not in os.environ:
                print("'DB_NAME' environment variable does not exist")
                exit(1)
            elif 'DB_USER' not in os.environ:
                print("'DB_USER' environment variable does not exist")
                exit(1)
            elif 'DB_PORT' not in os.environ:
                print("'DB_PORT' environment variable does not exist")
                exit(1)
            else:
                db_pass = os.getenv('DB_PASS')
                db_host = os.getenv('DB_HOST')
                db_name = os.getenv('DB_NAME')
                db_user = os.getenv('DB_USER')
                db_port = os.getenv('DB_PORT')

            conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user,
                                    password=db_pass)
            conn.autocommit = True
            cur = conn.cursor()

            query = sql.SQL("INSERT INTO public.hashtags (hashtag) VALUES (%s)").format()
            cur.execute(query, (hashtag,))

            cur.close()
            conn.close()
            return "Rows updated with hashtag: " + str(hashtag)

        except psycopg2.OperationalError:
            abort(make_response(jsonify(message="Unable to connect to the database!"), 502))

        except psycopg2.errors.UniqueViolation:
            abort(make_response(jsonify(message="Hashtag already exists in database."), 409))


@app.route('/tweets/<string:hashtag>', methods=['GET'])
def get_hashtag(hashtag):
    try:
        if 'DB_PASS' not in os.environ:
            print("'DB_PASS' environment variable does not exist")
            exit(1)
        elif 'DB_HOST' not in os.environ:
            print("'DB_HOST' environment variable does not exist")
            exit(1)
        elif 'DB_NAME' not in os.environ:
            print("'DB_NAME' environment variable does not exist")
            exit(1)
        elif 'DB_USER' not in os.environ:
            print("'DB_USER' environment variable does not exist")
            exit(1)
        elif 'DB_PORT' not in os.environ:
            print("'DB_PORT' environment variable does not exist")
            exit(1)
        else:
            db_pass = os.getenv('DB_PASS')
            db_host = os.getenv('DB_HOST')
            db_name = os.getenv('DB_NAME')
            db_user = os.getenv('DB_USER')
            db_port = os.getenv('DB_PORT')

        conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user,
                                password=db_pass)
        conn.autocommit = True
        cur = conn.cursor()

        query = sql.SQL("SELECT * FROM public.twitter WHERE hashtag = %s ORDER BY id DESC LIMIT 10").format()
        cur.execute(query, (hashtag,))
        tweets_columns = cur.fetchall()
        cur.close()
        conn.close()

        tweets_data = [{"tweet_id": column[1], "tweet_content": column[2]} for column in tweets_columns]

        if not tweets_data:
            abort(make_response(jsonify(message="Database does not contain tweets with this hashtag."), 400))
        else:
            return jsonify(tweets_data)

    except psycopg2.OperationalError:
        abort(make_response(jsonify(message="Unable to connect to the database!"), 502))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
