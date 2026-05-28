from flask import Flask, render_template, request, redirect, url_for
from lib.database import init_db, guardar_turno

app = Flask(__name__)

# Aseguramos que la base de datos y su tabla estén creadas al arrancar
init_db()

@app.route('/')
def index():
    """Renderiza el formulario para solicitar turnos."""
    return render_template('formulario.html')

@app.route('/solicitar', methods=['POST'])
def solicitar_turno():
    """Procesa el envío del formulario de turnos."""
    # Extraemos la información ingresada por el ciudadano
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    dni = request.form.get('dni')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')

    # Guardamos los datos en la base de datos a través de nuestro módulo lib/database
    guardar_turno(nombre, apellido, dni, email, telefono, fecha, hora)

    # Redireccionamos a la pantalla de éxito pasando los datos a renderizar
    return render_template(
        'exito.html',
        nombre=nombre,
        apellido=apellido,
        fecha=fecha,
        hora=hora
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)