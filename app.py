import MySQLdb
import os
import flask
from flask import request
import re

DATABASE_URL = os.environ['DATABASE_URL']
DOKKU_APP_TYPE = os.environ['DOKKU_APP_TYPE']


DB_USER = 'mysql'
DB_PASSWORD = re.search(".*:(.*)@", DATABASE_URL).group(1)
DB_HOST = re.search(".*@(.*)\/.*", DATABASE_URL).group(1)
DB_NAME = re.search(".*/(.*)", DATABASE_URL).group(1)

app = flask.Flask(__name__)


def mysql_select_como_diccionario(query):
    db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()

@app.route('/api/distritos')
def distritos():
    query = '''
        SELECT
          *
        FROM
          s_distrito
    '''
    return flask.jsonify(data=mysql_select_como_diccionario(query))

@app.route('/')
def index():
    ROOT_URL = request.host_url
    data = {
        "demo": 123,
        "ROOT_URL": ROOT_URL,
        "DOKKU_APP_TYPE": DOKKU_APP_TYPE,
        "distritos": os.path.join(ROOT_URL, "api", "distritos")
    }
    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
