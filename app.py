import MySQLdb
import os
import flask

DOKKU_APP_TYPE = os.environ['DOKKU_APP_TYPE']

app = flask.Flask(__name__)

@app.route('/')
def temp():
    data = {
        "demo": 123,
        "DOKKU_APP_TYPE": DOKKU_APP_TYPE,
    }

    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
