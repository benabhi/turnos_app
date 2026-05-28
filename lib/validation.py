import re
from datetime import datetime

def validar_formulario_turno(datos, horarios_permitidos):
    """
    Valida rigurosamente los datos recibidos del formulario en el servidor.
    Retorna (True, None) si todo es válido, o (False, "Mensaje de error") si falla.
    """
    nombre = datos.get('nombre', '').strip()
    apellido = datos.get('apellido', '').strip()
    dni = datos.get('dni', '').strip()
    email = datos.get('email', '').strip()
    telefono = datos.get('telefono', '').strip()
    fecha = datos.get('fecha', '').strip()
    hora = datos.get('hora', '').strip()

    # 1. Validación de campos obligatorios vacíos
    if not all([nombre, apellido, dni, email, telefono, fecha, hora]):
        return False, "Todos los campos del formulario son obligatorios."

    # 2. Validación de formato de texto (Nombre y Apellido sin números)
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre) or len(nombre) < 2:
        return False, "El nombre ingresado no es válido (mínimo 2 letras, sin números)."

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido) or len(apellido) < 2:
        return False, "El apellido ingresado no es válido (mínimo 2 letras, sin números)."

    # 3. Validación estricta de DNI (7 u 8 números enteros)
    if not re.match(r"^[0-9]{7,8}$", dni):
        return False, "El DNI debe contener únicamente entre 7 y 8 dígitos numéricos, sin puntos ni espacios."

    # 4. Validación de Teléfono Celular Argentino (10 u 11 dígitos numéricos)
    if not re.match(r"^[0-9]{10,11}$", telefono):
        return False, "El número de teléfono debe tener entre 10 y 11 dígitos, incluyendo la característica."

    # 5. Validación de estructura de Correo Electrónico
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return False, "Por favor, ingrese una dirección de correo electrónico válida."

    # 6. Validaciones de Fecha (Formato, Pasado y Días Hábiles)
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        hoy = datetime.today().date()

        if fecha_obj.date() < hoy:
            return False, "No se admiten solicitudes para fechas que ya pasaron."

        # 0=Lunes, 4=Viernes, 5=Sábado, 6=Domingo
        if fecha_obj.weekday() >= 5:
            return False, "La institución no procesa trámites administrativos durante los fines de semana."
    except ValueError:
        return False, "El formato de la fecha seleccionada es incorrecto."

    # 7. Validación de Hora (Lista blanca institucional)
    if hora not in horarios_permitidos:
        return False, "El horario solicitado no se encuentra dentro del rango de atención permitido."

    # Si supera todos los filtros, los datos son completamente seguros
    return True, None