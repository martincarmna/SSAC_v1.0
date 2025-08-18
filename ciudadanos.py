from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "1234"

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'prueba_flask'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def inicio():
    return render_template('SSAC.html', request=request)

@app.route('/registro')
def registro():
    return render_template('registro.html', request=request)

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.form
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ciudadanos 
                    (nombre, apellido_paterno, apellido_materno, fecha_nacimiento, curp, rfc, correo, domicilio, celular, cp, genero)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    datos.get('campo2'), datos.get('campo3'), datos.get('campo4'),
                    datos.get('campo5'), datos.get('campo6'), datos.get('campo7'),
                    datos.get('campo10'), datos.get('campo11'), datos.get('campo12'),
                    datos.get('campo13'), datos.get('campo14')
                ))
            conn.commit()
        return redirect('/ver')
    except Exception as e:
        return f"Error al guardar ciudadano: {e}"

@app.route('/ver')
def ver():
    busqueda = request.args.get('busqueda', '').strip()
    estado_civil = request.args.get('estado_civil', '').strip()
    genero = request.args.get('genero', '').strip()
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM ciudadanos WHERE 1=1 "
                params = []
                if busqueda:
                    query += "AND (nombre LIKE %s OR curp LIKE %s) "
                    params.extend([f"%{busqueda}%", f"%{busqueda}%"])
                if estado_civil:
                    query += "AND estado_civil = %s "
                    params.append(estado_civil)
                if genero:
                    query += "AND genero = %s "
                    params.append(genero)
                cursor.execute(query, params)
                ciudadanos = cursor.fetchall()
        return render_template('ver.html',
                               ciudadanos=ciudadanos,
                               busqueda=busqueda,
                               estado_civil=estado_civil,
                               genero=genero,
                               request=request)
    except Exception as e:
        return f"Error al obtener ciudadanos: {e}"

@app.route('/editar_registro/<int:id>', methods=['GET', 'POST'])
def editar_registro(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            if request.method == 'POST':
                datos = request.form
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE ciudadanos SET 
                        nombre=%s, apellido_paterno=%s, apellido_materno=%s, fecha_nacimiento=%s,
                        curp=%s, rfc=%s, correo=%s, domicilio=%s, celular=%s, cp=%s, genero=%s
                        WHERE id=%s
                    """, (
                        datos.get('campo2'), datos.get('campo3'), datos.get('campo4'),
                        datos.get('campo5'), datos.get('campo6'), datos.get('campo7'),
                        datos.get('campo10'), datos.get('campo11'), datos.get('campo12'),
                        datos.get('campo13'), datos.get('campo14'), id
                    ))
                conn.commit()
                return redirect('/ver')
            else:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM ciudadanos WHERE id=%s", (id,))
                    ciudadano = cursor.fetchone()
                return render_template('editar_registro.html', ciudadano=ciudadano, request=request)
    except Exception as e:
        return f"Error al editar ciudadano: {e}"

@app.route('/eliminar_ciudadano/<int:id>', methods=['POST'])
def eliminar_ciudadano(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ciudadanos WHERE id = %s", (id,))
            conn.commit()
        return redirect('/ver')
    except Exception as e:
        return f"Error al eliminar ciudadano: {e}"

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s",
                               (usuario, contrasena))
                resultado = cursor.fetchone()
        if resultado:
            return redirect('/ver')
        else:
            return "<h3>Credenciales inválidas. Intenta nuevamente.</h3>"
    except Exception as e:
        return f"Error al iniciar sesión: {e}"
from flask import Flask, render_template, request, redirect, url_for

# ... (código de tu aplicación)

@app.route('/solicitar_ciudadano/<int:id>')
def solicitar_ciudadano(id):
    tipo_solicitud = request.args.get('tipo_solicitud')
    if tipo_solicitud:
        # Aquí es donde pondrías la lógica para redirigir al usuario
        # en función del tipo de solicitud que eligió.
        if tipo_solicitud == 'servicios':
            return redirect(url_for('servicios'))
        elif tipo_solicitud == 'apoyos':
            return redirect(url_for('apoyos'))
        elif tipo_solicitud == 'tramites':
            return redirect(url_for('tramites'))
    # Si no se seleccionó nada o algo falla, puedes redirigir a ver ciudadanos
    return redirect(url_for('ver_ciudadanos'))

# ... (el resto de tus rutas)
# --- APOYOS ---
@app.route('/apoyos')
def apoyos():
    busqueda = request.args.get('busqueda', '')  # Captura el texto del buscador

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM apoyos WHERE 1=1"
                params = []

                if busqueda:
                    query += " AND nombre LIKE %s"  # Filtra por nombre del apoyo
                    params.append(f"%{busqueda}%")

                cursor.execute(query, params)
                datos = cursor.fetchall()

        return render_template('apoyos.html', apoyos=datos, busqueda=busqueda, request=request)
    except Exception as e:
        return f"Error al obtener apoyos: {e}"


@app.route('/registroApoyo')
def registroApoyo():
    return render_template('registroApoyo.html', request=request)

@app.route('/guardar_apoyo', methods=['POST'])
def guardar_apoyo():
    d = request.form
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO apoyos (nombre, descripcion, categoria, fecha_inicio, fecha_vencimiento, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (d.get('nombre'), d.get('descripcion'), d.get('categoria'),
                      d.get('fecha_inicio'), d.get('fecha_vencimiento'), d.get('estado')))
            conn.commit()
        return redirect('/apoyos')
    except Exception as e:
        return f"Error al guardar apoyo: {e}"

@app.route('/editar_apoyo/<int:id>', methods=['GET', 'POST'])
def editar_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            if request.method == 'POST':
                d = request.form
                with conn.cursor() as c:
                    c.execute("""
                        UPDATE apoyos SET nombre=%s, descripcion=%s, categoria=%s,
                          fecha_inicio=%s, fecha_vencimiento=%s, estado=%s
                        WHERE id=%s
                    """, (d.get('nombre'), d.get('descripcion'), d.get('categoria'),
                          d.get('fecha_inicio'), d.get('fecha_vencimiento'),
                          d.get('estado'), id))
                conn.commit()
                return redirect('/apoyos')
            else:
                with conn.cursor(dictionary=True) as c:
                    c.execute("SELECT * FROM apoyos WHERE id=%s", (id,))
                    apoyo = c.fetchone()
                return render_template('registroApoyo.html', apoyo=apoyo, request=request)
    except Exception as e:
        return f"Error al editar apoyo: {e}"

@app.route('/ver_apoyo/<int:id>')
def ver_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as c:
                c.execute("SELECT * FROM apoyos WHERE id=%s", (id,))
                apoyo = c.fetchone()
        return render_template('ver_apoyos.html', apoyo=apoyo, request=request)
    except Exception as e:
        return f"Error al mostrar detalles: {e}"

@app.route('/eliminar_apoyo/<int:id>', methods=['POST'])
def eliminar_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM apoyos WHERE id = %s", (id,))
            conn.commit()
        return redirect('/apoyos')  # Redirige de nuevo a la lista de apoyos
    except Exception as e:
        return f"Error al eliminar apoyo: {e}"

#@app.route('/solicitudes_apoyo')
#def solicitarApoyo():
    #return render_template('solicitudes_apoyo.html')


@app.route('/solicitudes_apoyo')
def solicitudes_apoyo():
    busqueda = request.args.get('busqueda', '')  # Captura la búsqueda

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT sa.id_sol_apoyo AS id,
                           a.nombre AS nombre_apoyo,
                           c.nombre AS solicitante,
                           sa.fecha_solicitud AS fecha,
                           sa.estado
                    FROM solicitud_apoyo sa
                    JOIN apoyos a ON sa.apoyos_id = a.id
                    JOIN ciudadanos c ON sa.ciudadanos_id = c.id
                    WHERE 1=1
                """
                params = []

                if busqueda:
                    query += " AND (a.nombre LIKE %s OR c.nombre LIKE %s OR sa.estado LIKE %s)"
                    params.extend([f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"])

                cursor.execute(query, params)
                solicitudes = cursor.fetchall()

        return render_template('solicitudesApoyo.html', solicitudes=solicitudes, busqueda=busqueda, request=request)
    except Exception as e:
        return f"Error al obtener solicitudes de apoyo: {e}"

# Ruta para mostrar el formulario de solicitud de apoyo
@app.route('/registro_solicitud_apoyo', methods=['GET', 'POST'])
def registro_solicitud_apoyo():
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:

                # Traemos los apoyos disponibles
                cursor.execute("SELECT id, nombre FROM apoyos WHERE estado='Activo'")
                apoyos = cursor.fetchall()

                # Traemos los ciudadanos
                cursor.execute("SELECT id, nombre, apellido_paterno FROM ciudadanos")
                ciudadanos = cursor.fetchall()

        return render_template(
            'solicitud_apoyo_form.html',
            apoyos=apoyos,
            ciudadanos=ciudadanos,
            request=request
        )
    except Exception as e:
        return f"Error al cargar el formulario: {e}"


# Ruta para guardar la solicitud en la base de datos
@app.route('/guardar_solicitud_apoyo', methods=['POST'])
def guardar_solicitud_apoyo():
    d = request.form
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO solicitud_apoyo 
                    (apoyos_id, ciudadanos_id, nombre, descripcion, fecha_solicitud, costo, estado, tipo_tramite, formato_pago)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    d.get('apoyos_id'),
                    d.get('ciudadanos_id'),
                    d.get('nombre'),
                    d.get('descripcion'),
                    d.get('fecha_solicitud'),
                    d.get('costo'),
                    d.get('estado'),
                    d.get('tipo_tramite'),
                    d.get('formato_pago')
                ))
            conn.commit()  # Confirmamos la inserción
        return redirect(url_for('solicitudes_apoyo'))
 # Redirige a la lista de solicitudes
    except Exception as e:
        return f"Error al guardar la solicitud: {e}"

# Ruta para eliminar solicitud de apoyo
@app.route('/eliminar_solicitud_apoyo/<int:id>', methods=['POST'])
def eliminar_solicitud_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM solicitud_apoyo WHERE id_sol_apoyo = %s", (id,))
                conn.commit()
        return redirect(url_for('solicitudes_apoyo'))  # Redirige a la lista de solicitudes
    except Exception as e:
        return f"Error al eliminar la solicitud: {e}"

@app.route('/editar_solicitud_apoyo/<int:id>', methods=['GET', 'POST'])
def editar_solicitud_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            if request.method == 'POST':
                d = request.form
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE solicitud_apoyo 
                        SET apoyos_id=%s, ciudadanos_id=%s, nombre=%s, descripcion=%s,
                            fecha_solicitud=%s, costo=%s, estado=%s, tipo_tramite=%s, formato_pago=%s
                        WHERE id_sol_apoyo=%s
                    """, (
                        d.get('apoyos_id'), d.get('ciudadanos_id'), d.get('nombre'),
                        d.get('descripcion'), d.get('fecha_solicitud'), d.get('costo'),
                        d.get('estado'), d.get('tipo_tramite'), d.get('formato_pago'), id
                    ))
                conn.commit()
                return redirect(url_for('solicitudes_apoyo'))
            else:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM solicitud_apoyo WHERE id_sol_apoyo=%s", (id,))
                    solicitud = cursor.fetchone()
                return render_template('editar_solicitud_apoyo.html', solicitud=solicitud, request=request)
    except Exception as e:
        return f"Error al editar la solicitud: {e}"
    
@app.route('/ver_solicitud_apoyo/<int:id>')
def ver_solicitud_apoyo(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT sa.id_sol_apoyo AS id,
                           a.nombre AS nombre_apoyo,
                           c.nombre AS solicitante,
                           sa.fecha_solicitud AS fecha,
                           sa.estado,
                           sa.descripcion,
                           sa.costo,
                           sa.tipo_tramite,
                           sa.formato_pago
                    FROM solicitud_apoyo sa
                    JOIN apoyos a ON sa.apoyos_id = a.id
                    JOIN ciudadanos c ON sa.ciudadanos_id = c.id
                    WHERE sa.id_sol_apoyo = %s
                """, (id,))
                solicitud = cursor.fetchone()

        if solicitud:
            return render_template('ver_solicitud_apoyo.html', solicitud=solicitud)
        else:
            return "Solicitud de apoyo no encontrada", 404
    except Exception as e:
        return f"Error al obtener la solicitud: {e}"




# --- TRÁMITES ---
# --- TRÁMITES CON BÚSQUEDA ---
@app.route('/tramites')
def tramites():
    busqueda = request.args.get('busqueda', '')  # Captura el texto del buscador
    estado = request.args.get('estado', '')      # Si quieres filtrar por estado también

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Consulta básica
                query = "SELECT * FROM tramites WHERE 1=1"
                params = []

                # Filtrado por búsqueda
                if busqueda:
                    query += " AND nombre LIKE %s"
                    params.append(f"%{busqueda}%")

                # Filtrado por estado
                if estado:
                    query += " AND estado = %s"
                    params.append(estado)

                cursor.execute(query, params)
                tramites = cursor.fetchall()

        return render_template('tramites.html', tramites=tramites, busqueda=busqueda, estado=estado, request=request)
    except Exception as e:
        return f"Error al obtener trámites: {e}"


@app.route('/registroTramite')
def registroTramite():
    return render_template('registroTramite.html', request=request)

@app.route('/guardar_tramite', methods=['POST'])
def guardar_tramite():
    d = request.form
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tramites 
                    (nombre, dependencia, modalidad, tipo_tramite, costo, formato_pago, estado, documento_expide, vigencia)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    d.get('nombre'), d.get('dependencia'), d.get('modalidad'),
                    d.get('tipo_tramite'), d.get('costo'), d.get('formato_pago'),
                    d.get('estado'), d.get('documento_expide'), d.get('vigencia')
                ))
            conn.commit()
        return redirect('/tramites')
    except Exception as e:
        return f"Error al guardar trámite: {e}"

@app.route('/editar_tramite/<int:id>', methods=['GET', 'POST'])
def editar_tramite(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            if request.method == 'POST':
                d = request.form
                with conn.cursor() as c:
                    c.execute("""
                        UPDATE tramites SET nombre=%s, dependencia=%s, modalidad=%s, tipo_tramite=%s,
                            costo=%s, formato_pago=%s, estado=%s, documento_expide=%s, vigencia=%s
                        WHERE id=%s
                    """, (
                        d.get('nombre'), d.get('dependencia'), d.get('modalidad'), d.get('tipo_tramite'),
                        d.get('costo'), d.get('formato_pago'), d.get('estado'),
                        d.get('documento_expide'), d.get('vigencia'), id
                    ))
                conn.commit()
                return redirect('/tramites')
            else:
                with conn.cursor(dictionary=True) as c:
                    c.execute("SELECT * FROM tramites WHERE id=%s", (id,))
                    tramite = c.fetchone()
                return render_template('registroTramite.html', tramite=tramite, request=request)
    except Exception as e:
        return f"Error al editar trámite: {e}"

@app.route('/eliminar_tramite/<int:id>', methods=['POST'])
def eliminar_tramite(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as c:
                c.execute("DELETE FROM tramites WHERE id = %s", (id,))
            conn.commit()
        return redirect('/tramites')
    except Exception as e:
        return f"Error al eliminar trámite: {e}"
    
@app.route('/ver_tramite/<int:id>')
def ver_tramite(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM tramites WHERE id=%s", (id,))
                tramite = cursor.fetchone()  # Un solo trámite
        return render_template('ver_tramite.html', tramite=tramite)  # Aquí la variable debe llamarse 'tramite'
    except Exception as e:
        return f"Error al mostrar detalles: {e}"



    
# --- SERVICIOS ---
@app.route('/servicios')
def servicios():
    busqueda = request.args.get('busqueda', '')  # Captura lo que escriba el usuario

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM servicios WHERE 1=1"
                params = []

                # Filtrado por búsqueda en nombre o tipo de servicio
                if busqueda:
                    query += " AND (nombre LIKE %s OR tipo_servicio LIKE %s)"
                    params.extend([f"%{busqueda}%", f"%{busqueda}%"])

                cursor.execute(query, params)
                servicios = cursor.fetchall()

        return render_template('servicios.html', servicios=servicios, busqueda=busqueda, request=request)
    except Exception as e:
        return f"Error al obtener servicios: {e}"


@app.route('/registro_servicio')
def registro_servicio():
    return render_template('nuevo_servicio.html', request=request)

@app.route('/guardar_servicio', methods=['POST'])
def guardar_servicio():
    d = request.form
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO servicios (nombre, tipo_servicio, costo, estado)
                    VALUES (%s, %s, %s, %s)
                """, (
                    d.get('nombre'),
                    d.get('tipo_servicio'),
                    d.get('costo'),
                    d.get('estado')
                ))
            conn.commit()
        return redirect('/servicios')
    except Exception as e:
        return f"Error al guardar servicio: {e}"


@app.route('/editar_servicio/<int:id>', methods=['GET', 'POST'])
def editar_servicio(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            if request.method == 'POST':
                d = request.form
                with conn.cursor() as c:
                    c.execute("""
                        UPDATE servicios
                        SET nombre=%s, tipo_servicio=%s, costo=%s, estado=%s
                        WHERE id=%s
                    """, (
                        d.get('nombre'), d.get('tipo_servicio'), d.get('costo'),
                        d.get('estado'), id
                    ))
                conn.commit()
                return redirect('/servicios')
            else:
                with conn.cursor(dictionary=True) as c:
                    c.execute("SELECT * FROM servicios WHERE id=%s", (id,))
                    servicio = c.fetchone()
                return render_template('nuevo_registro.html', servicio=servicio, request=request)
    except Exception as e:
        return f"Error al editar servicio: {e}"


@app.route('/eliminar_servicio/<int:id>', methods=['POST'])
def eliminar_servicio(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as c:
                c.execute("DELETE FROM servicios WHERE id = %s", (id,))
            conn.commit()
        return redirect('/servicios')
    except Exception as e:
        return f"Error al eliminar servicio: {e}"
    
@app.route('/ver_servicio/<int:id>')
def ver_servicio(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM servicios WHERE id=%s", (id,))
                servicio = cursor.fetchone()  # Un solo servicio
        return render_template('ver_servicios.html', serv=servicio)  # Enviamos la variable correcta
    except Exception as e:
        return f"Error al mostrar detalles: {e}"



@app.route('/solicitudes-servicio')
def solicitudes_servicio():
    return render_template("solicitudServicio.html")





if __name__ == '__main__':
    app.run(debug=True)