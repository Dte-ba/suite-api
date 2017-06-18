import MySQLdb
import os
import flask
from flask import request
from urlparse import urlparse
import re

DATABASE_URL = os.environ.get('DATABASE_URL', None)
DOKKU_APP_TYPE = os.environ.get('DOKKU_APP_TYPE', None)


DB_USER = 'mysql'
DB_PASSWORD = re.search(".*:(.*)@", DATABASE_URL).group(1)
DB_HOST = re.search(".*@(.*)\:.*", DATABASE_URL).group(1)
DB_NAME = re.search(".*/(.*)", DATABASE_URL).group(1)


app = flask.Flask(__name__)


def mysql_select_como_diccionario(query):
    db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()

def convertir_en_respuesta(nombre_del_recurso, query):
    resultado = mysql_select_como_diccionario(query)
    cantidad = len(resultado)
    return flask.jsonify(cantidad=cantidad, nombre_del_recurso=resultado)


@app.route('/api/distritos')
def distritos():
    query = "SELECT * FROM s_distrito"
    return convertir_en_respuesta('distritos', query)

@app.route('/')
def index():
    ROOT_URL = request.host_url
    data = {
        "distritos": os.path.join(ROOT_URL, "api", "distritos")
    }
    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
