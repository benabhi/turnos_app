from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from lib.database import init_db, guardar_turno, obtener_horas_ocupadas, obtener_todos_los_turnos, cancelar_turno_logico
from lib.validation import validar_formulario_turno  # Importamos nuestro nuevo validador
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_sistemas_informacion_2'

# Inicializamos el motor de base de datos
init_db()

# Horarios permitidos de atención cada 30 minutos
HORARIOS_PERMITIDOS = [
    "08:00", "08:30", "09:00", "09:30",
    "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "13:00"
]

@app.route('/')
def index():
    """Muestra la vista pública con el formulario de solicitud."""
    return render_template('formulario.html')

@app.route('/api/horas-disponibles')
def horas_disponibles():
    """API en tiempo real consultada por el JavaScript del Frontend."""
    fecha_str = request.args.get('fecha')
    if not fecha_str:
        return jsonify([])

    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return jsonify([])

    if fecha_obj.weekday() >= 5:
        return jsonify({"error": "No laborable"}), 400

    horas_ocupadas = obtener_horas_ocupadas(fecha_str)
    horas_libres = [hora for hora in HORARIOS_PERMITIDOS if hora not in horas_ocupadas]

    return jsonify(horas_libres)

@app.route('/solicitar', methods=['POST'])
def solicitar_turno():
    """Procesa el formulario delegando los controles al módulo de validación."""

    # Invocamos la validación del servidor pasando todo el diccionario del formulario
    es_valido, mensaje_error = validar_formulario_turno(request.form, HORARIOS_PERMITIDOS)

    if not es_valido:
        # Si el validador encuentra anomalías, enviamos la alerta y abortamos el flujo
        flash(mensaje_error, "error")
        return redirect(url_for('index'))

    # Si los datos son válidos, los extraemos de forma segura
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    dni = request.form.get('dni')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')

    # Intentamos impactar el registro en la Base de Datos SQLite
    exito = guardar_turno(nombre, apellido, dni, email, telefono, fecha, hora)

    if not exito:
        flash("El horario seleccionado acaba de ser reservado por otro usuario. Por favor, elegí uno diferente.", "error")
        return redirect(url_for('index'))

    # Transición limpia hacia la pantalla de éxito
    return render_template(
        'exito.html',
        nombre=nombre,
        apellido=apellido,
        fecha=fecha,
        hora=hora
    )

# ==========================================
#        RUTAS DEL PANEL DE CONTROL
# ==========================================

@app.route('/admin')
def admin():
    """Sección administrativa interna para auditar las solicitudes."""
    turnos = obtener_todos_los_turnos()
    return render_template('admin.html', turnos=turnos)

@app.route('/admin/cancelar/<int:id_turno>', methods=['POST'])
def cancelar_turno(id_turno):
    """Cancela de forma lógica un turno liberando el horario de atención."""
    cancelar_turno_logico(id_turno)
    flash("El turno seleccionado ha sido cancelado con éxito.", "success")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)