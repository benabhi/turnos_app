import sqlite3

DB_NAME = "turnos_policia.db"

def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la tabla incluyendo la columna 'estado'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'activo' -- 'activo' o 'cancelado'
        )
    ''')
    conn.commit()
    conn.close()

def guardar_turno(nombre, apellido, dni, email, telefono, fecha, hora):
    """Inserta un nuevo turno validando primero que no haya otro ACTIVO en ese horario."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Validamos manualmente si ya existe un turno ACTIVO para esa fecha y hora
    cursor.execute('''
        SELECT id FROM turnos
        WHERE fecha = ? AND hora = ? AND estado = 'activo'
    ''', (fecha, hora))

    if cursor.fetchone() is not None:
        conn.close()
        return False # Horario ocupado por un turno activo

    # Si está libre (o si los que hay están cancelados), lo guardamos
    cursor.execute('''
        INSERT INTO turnos (nombre, apellido, dni, email, telefono, fecha, hora, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'activo')
    ''', (nombre, apellido, dni, email, telefono, fecha, hora))

    conn.commit()
    conn.close()
    return True

def obtener_horas_ocupadas(fecha):
    """Retorna las horas que ya tienen un turno ACTIVO (los cancelados liberan el horario)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hora FROM turnos
        WHERE fecha = ? AND estado = 'activo'
    ''', (fecha,))
    filas = cursor.fetchall()
    conn.close()
    return [fila['hora'] for fila in filas]

def obtener_todos_los_turnos():
    """Retorna el historial completo (activos y cancelados) para el panel de administración."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM turnos ORDER BY fecha ASC, hora ASC')
    turnos = cursor.fetchall()
    conn.close()
    return turnos

def cancelar_turno_logico(id_turno):
    """Cambia el estado del turno a 'cancelado' sin borrar el registro."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE turnos
        SET estado = 'cancelado'
        WHERE id = ?
    ''', (id_turno,))
    conn.commit()
    conn.close()