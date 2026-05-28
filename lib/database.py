import sqlite3

DB_NAME = "turnos_policia.db"

def get_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    # Esto permite acceder a las filas como diccionarios: fila['nombre'] en vez de fila[1]
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la tabla de turnos si no existe."""
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
            hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_turno(nombre, apellido, dni, email, telefono, fecha, hora):
    """Inserta un nuevo turno en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO turnos (nombre, apellido, dni, email, telefono, fecha, hora)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido, dni, email, telefono, fecha, hora))
    conn.commit()
    conn.close()