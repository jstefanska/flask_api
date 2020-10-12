from flask import Flask, abort, make_response, jsonify, request
import json
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)


@app.route('/hashtag', methods=['POST'])
def add_hashtag():
    data = json.loads(request.data)
    hashtag = data.get("value", None)

    if "#" in str(hashtag):
        abort(make_response(jsonify(message="Use a word without '#'. Application will take care of that."), 400))
    else:
        try:
            if 'DB_PASS' not in os.environ:
                abort(make_response(jsonify(message="'DB_PASS' environment variable does not exist"), 400))
            else:
                pass

            db_pass = os.getenv('DB_PASS')

            conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres',
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
            abort(make_response(jsonify(message="'DB_PASS' environment variable does not exist"), 400))
        else:
            pass

        db_pass = os.getenv('DB_PASS')

        conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres',
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
    app.run(
        debug=True
    )
