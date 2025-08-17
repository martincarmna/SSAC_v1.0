from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'prueba_flask'
}

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
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM apoyos")
                datos = cursor.fetchall()
        return render_template('apoyos.html', apoyos=datos, request=request)
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

@app.route('/ver_apoyos/<int:id>')
def ver_apoyos(id):
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as c:
                c.execute("SELECT * FROM apoyos WHERE id=%s", (id,))
                apoyo = c.fetchone()
        return render_template('ver_apoyos.html', apoyo=apoyo, request=request)
    except Exception as e:
        return f"Error al mostrar detalles: {e}"

#@app.route('/solicitudes_apoyo')
#def solicitarApoyo():
    #return render_template('solicitudes_apoyo.html')


@app.route('/solicitudes_apoyo')
def solicitudesApoyo():
    # Aquí puedes traer los datos desde la DB o poner lista vacía
    solicitudes = [
        {"id": 1, "nombre_apoyo": "Beca Educativa", "solicitante": "Juan Pérez", "fecha": "2025-08-14", "estado": "Pendiente"},
        {"id": 2, "nombre_apoyo": "Apoyo Alimentario", "solicitante": "Ana López", "fecha": "2025-08-13", "estado": "Aprobado"},
    ]
    return render_template('solicitudesApoyo.html', solicitudes=solicitudes)





# --- TRÁMITES ---
@app.route('/tramites')
def tramites():
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM tramites")
                tramites = cursor.fetchall()
        return render_template('tramites.html', tramites=tramites, request=request)
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
    
@app.route('/solicitudesTramite')
def solicitudesTramite():
    # Aquí puedes traer los datos desde la DB o poner lista vacía
    solicitudes = [
        {"id": 1, "nombre_apoyo": "Beca Educativa", "solicitante": "Juan Pérez", "fecha": "2025-08-14", "estado": "Pendiente"},
        {"id": 2, "nombre_apoyo": "Apoyo Alimentario", "solicitante": "Ana López", "fecha": "2025-08-13", "estado": "Aprobado"},
    ]
    return render_template('solicitudesTramite.html', solicitudes=solicitudes)


  
    

# --- SERVICIOS ---
@app.route('/servicios')
def servicios():
    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM servicios")
                servicios = cursor.fetchall()
        return render_template('servicios.html', servicios=servicios, request=request)
    except Exception as e:
        return f"Error al obtener servicios: {e}"

@app.route('/nuevo_servicio')
def nuevo_registro():
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




if __name__ == '__main__':
    app.run(debug=True)