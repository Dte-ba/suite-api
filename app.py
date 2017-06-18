import MySQLdb

import flask

app = flask.Flask(__name__)

@app.route('/')
def temp():
    return flask.jsonify(data={'demo': 123})

if __name__ == '__main__':
    app.debug = True
    app.run()
