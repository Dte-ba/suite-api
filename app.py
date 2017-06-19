# coding: utf-8
import MySQLdb, MySQLdb.cursors
import os
import flask
from flask import request
from urlparse import urlparse
import re
from flask import json, Response

DATABASE_URL = os.environ['DATABASE_URL']


DB_USER = 'mysql'
DB_PASSWORD = re.search(".*:(.*)@", DATABASE_URL).group(1)
DB_HOST = re.search(".*@(.*)\:.*", DATABASE_URL).group(1)
DB_NAME = re.search(".*/(.*)", DATABASE_URL).group(1)


app = flask.Flask(__name__)


def mysql_select_como_diccionario(query):
    db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, cursorclass=MySQLdb.cursors.DictCursor, use_unicode=True, charset="utf8")
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()

def convertir_en_respuesta(nombre_del_recurso, query):
    resultado = mysql_select_como_diccionario(query)
    cantidad = len(resultado)

    data = {
     "cantidad": cantidad,
     nombre_del_recurso: resultado
    }

    json_string = json.dumps(data, ensure_ascii=False)
    content_type = "application/json; charset=utf-8"
    response = Response(json_string, content_type=content_type)
    return response

@app.route('/api/usuarios')
def usuarios():
    query = """
        SELECT
          s_usuario_nivel.ids_region,
          s_contratador.nombre,
          s_cargo_proyectos.nombre,
          s_usuarios.nombre,
          s_usuarios.estado,
          s_usuarios.fecha_nac,
          s_usuarios.dni,
          s_usuarios.celular,
          s_usuarios.telefono,
          s_usuarios.direccion,
          s_usuarios.email,
          s_usuarios.zona,
          s_usuarios.ids_usuarios,
          s_usuarios.cbu,
          s_usuarios.cuil
      FROM
          s_usuarios
      INNER JOIN
          s_usuario_nivel
      ON
          s_usuarios.ids_usuarios = s_usuario_nivel.ids_usuarios
      INNER JOIN
          s_niveles_acceso
      ON
          s_usuario_nivel.ids_niveles_acceso = s_niveles_acceso.ids_niveles_acceso
      INNER JOIN
          s_contratador
      ON
          s_niveles_acceso.ids_contratador = s_contratador.ids_contratador
      INNER JOIN
          s_cargo_proyectos
      ON
          s_niveles_acceso.ids_cargo_proyectos = s_cargo_proyectos.ids_cargo_proyectos
      WHERE
          s_usuarios.estado = 1
    """
    return convertir_en_respuesta('usuarios', query)

@app.route('/api/escuelas')
def escuelas():
    query = """
        SELECT
        	escuela.nombre AS `nombre`,
            escuela.cue AS `cue`,
            escuela.telefono AS `telefono`,
            escuela.direccion AS `direccion`,
            localidad.nombre AS `localidad`,
            escuela.lat AS `latitud`,
            escuela.lng AS `longitud`,
            tipo_financiamiento.nombre AS `tipo_financiamiento`,
            tipo_gestion.nombre AS `tipo_gestion`,
            nivel.nombre AS `nivel`,
            area.nombre AS `area`,
            escuela.estado AS `estado`
        FROM
            `s_escuela` AS `escuela`
        INNER JOIN
        	`s_distrito_localidad` AS `localidad`
        ON
        	`escuela`.`ids_distrito_localidad` = `localidad`.`ids_distrito_localidad`
        INNER JOIN
        	`s_tipo_financiamiento` AS `tipo_financiamiento`
        ON
        	`escuela`.`ids_tipo_financiamiento` = `tipo_financiamiento`.`ids_tipo_financiamiento`
        INNER JOIN
        	`s_gestion` AS `tipo_gestion`
        ON
        	`escuela`.`ids_gestion` = `tipo_gestion`.`ids_gestion`
        INNER JOIN
        	`s_tipo` AS `nivel`
        ON
        	`escuela`.`ids_tipo` = `nivel`.`ids_tipo`
        INNER JOIN
        	`s_area` AS `area`
        ON
        	`escuela`.`ids_area` = `area`.`ids_area`
    """
    return convertir_en_respuesta('escuelas', query)

@app.route('/api/localidades')
def localidades():
    query = """
    SELECT
      localidad.nombre AS `localidad`,
      distrito.nombre AS `distrito`,
      distrito.ids_region AS `region`
    FROM
      `s_distrito_localidad` AS `localidad`
    INNER JOIN
      `s_distrito` AS `distrito`
    ON
      `distrito`.`ids_distrito` = `localidad`.`ids_distrito`
    """
    return convertir_en_respuesta('localidades', query)

@app.route('/api/distritos')
def distritos():
    query = "SELECT * FROM s_distrito"
    return convertir_en_respuesta('distritos', query)

@app.route('/')
def index():
    ROOT_URL = request.host_url
    data = {
        "usuarios": os.path.join(ROOT_URL, "api", "usuarios"),
        "escuelas": os.path.join(ROOT_URL, "api", "escuelas"),
        "localidades": os.path.join(ROOT_URL, "api", "localidades"),
        "distritos": os.path.join(ROOT_URL, "api", "distritos"),
    }
    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
