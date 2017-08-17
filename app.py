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

@app.route('/api/paquetes')
def paquetes():
    query = """
        SELECT
            paquete.id_paquete AS legacy_id,
            paquete.region AS region,
            paquete.cue AS cue,
            paquete.ne AS ne,
            paquete.serie AS servidor_serie,
            paquete.idhardware AS idhardware,
            paquete.marca AS marca_de_arranque,
            paquete.archivo AS llave_servidor,
            DATE_FORMAT(paquete.fecha, "%Y-%m-%d") AS `fecha_pedido`,
            paquete.comentario AS comentario,
            paquete.carpeta AS carpeta_paquete,
            DATE_FORMAT(paquete.envio_anses, "%Y-%m-%d") AS `fecha_envio_anses`,
            paquete.zipanses AS zipanses,
            paquete.estado AS estado,
            DATE_FORMAT(paquete.fecha_devolucion, "%Y-%m-%d") AS `fecha_devolucion`,
            paquete.leido AS leido
        FROM
            `paquetes` AS paquete
    """
    return convertir_en_respuesta('paquetes', query)

@app.route('/api/devoluciones')
def devoluciones():
    query = """
        SELECT
            devolucion.id_devolucion AS legacy_id,
            paquete.id_paquete AS paquete_legacy_id,
            devolucion.archivo AS archivo_devolucion,
            DATE_FORMAT(
                devolucion.fecha_proceso,
                "%Y-%m-%d"
            ) AS `fecha_proceso`,
            devolucion.procesado AS procesado,
            devolucion.comentarios AS comentarios
        FROM
            `devoluciones` AS devolucion
        INNER JOIN
            paquetes AS paquete
        ON
            paquete.id_devolucion = devolucion.id_devolucion
    """
    return convertir_en_respuesta('devoluciones', query)

@app.route('/api/escuelas')
def escuelas():
    query = """
        SELECT
        	escuela.ids_escuela AS `id`,
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
        LEFT JOIN
        	`s_distrito_localidad` AS `localidad`
        ON
        	`escuela`.`ids_distrito_localidad` = `localidad`.`ids_distrito_localidad`
        LEFT JOIN
        	`s_tipo_financiamiento` AS `tipo_financiamiento`
        ON
        	`escuela`.`ids_tipo_financiamiento` = `tipo_financiamiento`.`ids_tipo_financiamiento`
        LEFT JOIN
        	`s_gestion` AS `tipo_gestion`
        ON
        	`escuela`.`ids_gestion` = `tipo_gestion`.`ids_gestion`
        LEFT JOIN
        	`s_tipo` AS `nivel`
        ON
        	`escuela`.`ids_tipo` = `nivel`.`ids_tipo`
        LEFT JOIN
        	`s_area` AS `area`
        ON
        	`escuela`.`ids_area` = `area`.`ids_area`
    """
    return convertir_en_respuesta('escuelas', query)

@app.route('/api/pisos')
def pisos():
    query = """
        SELECT
            escuela.cue AS `cue`,
            servidor.marca AS `marca`,
            servidor.serie AS `serie`,
            ups_rack.rack AS `rack`,
            ups_rack.ups AS `ups`,
            ups_rack.estado AS `piso_estado`
        FROM
            `s_escuela` AS `escuela`
        INNER JOIN
            `s_piso` AS `piso`
        ON
            `piso`.`ids_escuela` = `escuela`.`ids_escuela`
        INNER JOIN
            `s_servidor` AS `servidor`
        ON
            `servidor`.`ids_piso` = `piso`.`ids_piso`
        INNER JOIN
            `s_ups_rack` AS `ups_rack`
        ON
            `ups_rack`.`ids_piso` = `piso`.`ids_piso`
    """
    return convertir_en_respuesta('pisos', query)

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

@app.route('/api/contactos')
def contactos():
    query = """
        SELECT
            contactos.nombre AS nombre,
            contactos.telefono_part AS telefono,
            contactos.celular AS celular,
            contactos.email AS email,
            contactos.horario AS horario,
            cargo.nombre AS cargo,
            escuela.cue AS escuela
        FROM
            s_contactos AS contactos
        INNER JOIN
            s_cargo AS cargo
        ON
            cargo.ids_cargo = contactos.ids_cargo
        INNER JOIN
            s_escuela AS escuela
        ON
            escuela.ids_escuela = contactos.ids_escuela
    """
    return convertir_en_respuesta('contactos', query)

@app.route('/api/programas')
def programas():
    query = """
        SELECT
            escuela.cue AS `cue`,
            programa.nombre AS `programa`
        FROM
            `s_escuela` AS `escuela`
        INNER JOIN
            `s_programa_escuela` AS `programa_escuela`
        ON
            `programa_escuela`.`ids_escuela` = `escuela`.`ids_escuela`
		INNER JOIN
        	`s_programa` AS `programa`
        ON
        	`programa`.ids_programa = `programa_escuela`.`ids_programa`
    """
    return convertir_en_respuesta('programas', query)

@app.route('/api/acompaniantes_eventos')
def acompaniantes_eventos():
    query = """
        SELECT
            usuarios.nombre AS `nombre`,
            usuarios.dni AS `dni_usuario`,
            evento_usuarios.agenda_idagenda AS `legacy_id`
        FROM
            `agenda_usuarios` AS `evento_usuarios`
        INNER JOIN
            `s_usuarios` AS `usuarios`
        ON
            `evento_usuarios`.`s_usuarios_ids_usuarios` = `usuarios`.`ids_usuarios`
        INNER JOIN
        	`agenda` AS `evento`
        ON
        	`evento_usuarios`.`agenda_idagenda` = `evento`.`idagenda`
        WHERE
            (
                `evento`.`fecha_inicio` LIKE '%2016%' OR `evento`.`fecha_inicio` LIKE '%2017'
            ) AND `evento`.`estado` = 1
    """
    return convertir_en_respuesta('acompaniantes_eventos', query)

@app.route('/api/eventos')
def eventos():
    query = """
        SELECT
            evento.idagenda AS `legacy_id`,
            DATE_FORMAT(evento.fecha_inicio, "%Y-%m-%d") AS `fecha_inicio`,
            DATE_FORMAT(evento.fecha_inicio, "%H:%i:%s") AS `hora_inicio`,
            DATE_FORMAT(evento.fecha_final, "%Y-%m-%d") AS `fecha_final`,
            DATE_FORMAT(evento.fecha_final, "%H:%i:%s") AS `hora_final`,
            evento.fecha_inicio AS `datetime_inicio`,
            evento.fecha_final AS `datetime_final`,
            evento.fecha_carga AS `fecha_de_carga`,
            evento.cue AS `cue`,
            escuela.nombre AS `nombre_escuela`,
            usuarios.nombre AS `usuario`,
            usuarios.dni AS `dni_usuario`,
            evento.lugar AS `lugar`,
            evento.objetivo AS `objetivo`,
            evento.cant_participantes AS `cantidad_de_participantes`,
            categoria.nombre AS `categoria`,
            subcategoria.nombre AS `subcategoria`,
            evento.minuta AS `minuta`,
            evento.acta AS `acta`
        FROM
            `agenda` AS `evento`
        INNER JOIN
            `s_usuarios` AS `usuarios`
        ON
            `evento`.`s_usuarios_ids_usuarios` = `usuarios`.`ids_usuarios`
        INNER JOIN
            `agenda_detalle` AS `detalle`
        ON
            `evento`.`idagenda` = `detalle`.`agenda_idagenda`
        INNER JOIN
            `agenda_subcategoria` AS `subcategoria`
        ON
            `detalle`.`agenda_subcategoria_idagenda_subcategoria` = `subcategoria`.`idagenda_subcategoria`
        INNER JOIN
            `agenda_categoria` AS `categoria`
        ON
            `subcategoria`.`agenda_categoria_idagenda_categoria` = `categoria`.`idagenda_categoria`
        INNER JOIN
            `s_escuela` AS `escuela`
        ON
            `evento`.`ids_escuela` = `escuela`.`ids_escuela`
        WHERE
            (
                `evento`.`fecha_inicio` LIKE '%2016%' OR `evento`.`fecha_inicio` LIKE '%2017'
            ) AND `evento`.`estado` = 1
    """
    return convertir_en_respuesta('eventos', query)

@app.route('/api/categorias_agenda')
def categorias_agenda():
    query = """
    SELECT
        categoria.nombre AS `categoria`,
        subcategoria.nombre AS `subcategoria`
    FROM
        `agenda_subcategoria` AS `subcategoria`
    INNER JOIN
        `agenda_categoria` AS `categoria`
    ON
        `subcategoria`.`agenda_categoria_idagenda_categoria` = `categoria`.`idagenda_categoria`
    """
    return convertir_en_respuesta('categorias_agenda', query)

@app.route('/api/tickets')
def tickets():
    query = """
    SELECT
        tarea.ids_ticket AS `id_ticket_original`,
        DATE_FORMAT(tarea.fecha_alta, "%Y-%m-%d") AS `fecha_alta`,
        tipo.nombre AS `motivo`,
        estado.nombre AS `estado`,
        tarea.prioridad AS `prioridad`,
        usuario.nombre AS `usuario`,
        usuario.dni AS `dni_usuario`,
        escuela.cue AS `cue`,
        tarea.observaciones AS `descripcion`,
        tarea.ticket_ConIg AS `ticket_conig`
    FROM
        `s_ticket` AS `tarea`
    INNER JOIN
        `s_ticket_tipo` AS `tipo`
    ON
        `tarea`.`ids_ticket_tipo` = `tipo`.`ids_ticket_tipo`
    INNER JOIN
        `s_ticket_estado` AS `estado`
    ON
        `tarea`.`ids_ticket_estado` = `estado`.`ids_ticket_estado`
    INNER JOIN
        `s_usuarios` AS `usuario`
    ON
        `tarea`.`ids_usuarios` = `usuario`.`ids_usuarios`
    INNER JOIN
        `s_escuela` AS `escuela`
    ON
        `tarea`.`ids_escuela` = `escuela`.`ids_escuela`
    WHERE
    	`usuario`.`estado` = 1
    """
    return convertir_en_respuesta('tickets', query)

@app.route('/api/comentarios_tickets')
def comentarios_tickets():
    query = """
    SELECT
    	tarea.ids_ticket AS `id_ticket_original`,
        comentarios.observaciones AS `comentario`,
        usuario.nombre AS `autor_del_comentario`,
        usuario.dni AS `dni_usuario`,
        DATE_FORMAT(comentarios.fecha_alta, "%Y-%m-%d") AS `fecha`
    FROM
        `s_ticket_novedades` AS `comentarios`
    INNER JOIN
        `s_ticket` AS `tarea`
    ON
        `comentarios`.`ids_ticket` = `tarea`.`ids_ticket`
    INNER JOIN
            `s_usuarios` AS `usuario`
        ON
            `tarea`.`ids_usuarios` = `usuario`.`ids_usuarios`
    """
    return convertir_en_respuesta('comentarios_tickets', query)

@app.route('/api/validaciones')
def validaciones():
    query = """
        SELECT
            validaciones.ids_validaciones AS `legacy_id`,
            DATE_FORMAT(validaciones.fecha, "%Y-%m-%d") AS `fecha_de_alta`,
            escuela.nombre AS `escuela`,
            validaciones.cue AS `cue`,
            validaciones.estado AS `estado`,
            validaciones.cantidad AS `cantidad`,
            usuarios.nombre AS `usuario`,
            usuarios.dni AS `dni_usuario`
        FROM
            `s_validaciones` AS `validaciones`
            INNER JOIN
            `s_escuela` AS `escuela`
            ON
            validaciones.ids_escuela = escuela.ids_escuela
            inner JOIN
            s_usuarios AS `usuarios`
            ON
           	validaciones.ids_usuarios = usuarios.ids_usuarios
        WHERE
        	`validaciones`.`fecha` LIKE '%2016%' OR `validaciones`.`fecha` LIKE '%2017%'
    """
    return convertir_en_respuesta('validaciones', query)

@app.route('/api/historial_validaciones')
def historial_validaciones():
    query = """
        SELECT
            DATE_FORMAT(historial.fecha, "%Y-%m-%d") AS `fecha`,
            usuario.nombre AS `usuario`,
            usuario.dni AS `dni_usuario`,
            historial.cantidad AS `cantidad`,
            historial.observaciones AS `observaciones`,
            historial.ids_validaciones AS `validacion_legacy_id`,
            historial.ids_validacion_historial AS `legacy_id`

        FROM
            s_validacion_historial AS `historial`
            inner JOIN
            s_validaciones AS `validacion`
            ON
            historial.ids_validaciones = validacion.ids_validaciones
            inner JOIN
            s_usuarios AS `usuario`
            ON
            historial.ids_usuarios = usuario.ids_usuarios
            WHERE
                	historial.fecha LIKE '%2016%' OR historial.fecha LIKE '%2017%'
    """
    return convertir_en_respuesta('historial_validaciones', query)

@app.route('/api/conformaciones')
def conformaciones():
    query = """
        SELECT
            principal.cue AS cue_principal,
            principal.nombre AS nombre_escuela_principal,
        	s_escuela.cue AS cue_conformado,
            s_escuela.nombre AS nombre_escuela_conformada,
            s_anexa_motivo.nombre AS motivo,
            DATE_FORMAT(s_escuela_anexa.fecha, "%Y-%m-%d") AS fecha
        FROM
            s_escuela
        INNER JOIN
            s_escuela_anexa
        ON
            s_escuela.ids_escuela = s_escuela_anexa.ids_escuela
        INNER JOIN
            s_escuela AS principal
        ON
            s_escuela_anexa.ids_escuela_principal = principal.ids_escuela
        INNER JOIN
            s_anexa_motivo
        ON
            s_anexa_motivo.ids_anexa_motivo = s_escuela_anexa.ids_anexa_motivo
    """
    return convertir_en_respuesta('conformaciones', query)

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
        "contactos": os.path.join(ROOT_URL, "api", "contactos"),
        "pisos": os.path.join(ROOT_URL, "api", "pisos"),
        "programas": os.path.join(ROOT_URL, "api", "programas"),
        "eventos": os.path.join(ROOT_URL, "api", "eventos"),
        "acompaniantes_eventos": os.path.join(ROOT_URL, "api", "acompaniantes_eventos"),
        "categorias_agenda": os.path.join(ROOT_URL, "api", "categorias_agenda"),
        "tickets": os.path.join(ROOT_URL, "api", "tickets"),
        "comentarios_tickets": os.path.join(ROOT_URL, "api", "comentarios_tickets"),
        "validaciones": os.path.join(ROOT_URL, "api", "validaciones"),
        "historial_validaciones": os.path.join(ROOT_URL, "api", "historial_validaciones"),
        "conformaciones": os.path.join(ROOT_URL, "api", "conformaciones"),
        "paquetes": os.path.join(ROOT_URL, "api", "paquetes"),
        "devoluciones": os.path.join(ROOT_URL, "api", "devoluciones"),
    }
    return flask.jsonify(data=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
