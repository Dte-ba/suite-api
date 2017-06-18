import MySQLdb
import os
import flask
from flask import request

DOKKU_APP_TYPE = os.environ['DOKKU_APP_TYPE']


app = flask.Flask(__name__)


def mysql_select_como_diccionario(query):
    """
    db = MySQLdb.connect("localhost", "root", "","test")
    cur = db.cursor()
    cur.execute(query, param)
    data = cur.fetchall()

    return data.json_encoder()
    """
    return None

@app.route('/')
def temp():
    ROOT_URL = request.host_url
    data = {
        "demo": 123,
        "ROOT_URL": ROOT_URL,
        "DOKKU_APP_TYPE": DOKKU_APP_TYPE,
    }

    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
