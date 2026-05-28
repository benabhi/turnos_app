# Sistema de Gestión de Turnos - Policía de Río Negro

Este proyecto es una aplicación web minimalista, responsiva y autocontenida desarrollada para la gestión de turnos administrativos del **Certificado de Antecedentes Penales** de la Policía de la Provincia de Río Negro. El desarrollo fue concebido bajo los lineamientos y estándares solicitados para la cátedra de **Sistemas de Información II**.

---

## 🚀 Funcionalidades Principales

El sistema resuelve la problemática de asignación de turnos mediante una arquitectura de software limpia y validaciones en dos capas (Cliente-Servidor):

1. **Formulario Público Dinámico (`/`)**:
   - Registro de datos del ciudadano: Nombre, Apellido, DNI, Teléfono y Email.
   - Calendario inteligente que bloquea de forma interactiva fechas pasadas y fines de semana.
   - **Validación del lado del Cliente (JS)**: Comprobación de formatos de texto, DNI de 7 u 8 dígitos, celulares argentinos de 10-11 dígitos y correos electrónicos válidos antes de enviar la solicitud.
   - **Consulta de Disponibilidad en Tiempo Real**: API dinámica que consulta la base de datos y deshabilita los horarios que ya están ocupados por otros usuarios para la fecha elegida.

2. **Validación de Servidor Robusta (`lib/validation.py`)**:
   - Capa de seguridad backend mediante Expresiones Regulares (regex) para evitar inyecciones de datos corruptos o bypass de validaciones del navegador.

3. **Persistencia Local (`lib/database.py`)**:
   - Base de datos relacional ultraligera basada en **SQLite3**.
   - Restricción lógica para garantizar la unicidad de las citas (no pueden existir dos turnos activos para el mismo día y la misma hora).

4. **Panel de Control Administrativo (`/admin`)**:
   - Listado completo de todas las solicitudes registradas, ordenadas de forma cronológica (fecha y hora).
   - **Baja Lógica (Borrado Lógico)**: Al cancelar un turno, el registro no se elimina físicamente de la base de datos (preservando el historial de auditoría del sistema). El estado cambia a `cancelado`, liberando automáticamente el horario para que otro ciudadano pueda reservarlo.

5. **Alineación Estética Nv-1**:
   - Estilo minimalista y profesional adaptado a la paleta institucional (azules policiales, gris de fondo y tipografía moderna), implementado mediante CSS nativo (`static/style.css`) sin dependencias externas (CDNs) ni frameworks que ralenticen la carga del sitio.

---

## 📂 Estructura del Proyecto

A continuación se detalla la estructura lógica de los directorios del proyecto (omitiendo archivos temporales de compilación y librerías internas del entorno virtual para mayor legibilidad):

```text
turnos_app/
│   main.py               # Servidor de rutas de Flask (Controlador Principal)
│   README.md             # Documentación técnica del sistema (Este archivo)
│   requirements.txt      # Listado de dependencias del proyecto (Flask, etc.)
│   turnos_policia.db     # Base de datos SQLite (Generada automáticamente)
│   .gitignore            # Archivos y carpetas excluidos del control de versiones
│
├───lib/                  # Módulos de lógica interna de la aplicación
│       database.py       # Consultas SQL, inicialización de tablas y conexión de DB
│       validation.py     # Lógica de negocio y validación estricta de datos en el servidor
│
├───static/               # Archivos de recursos estáticos del cliente
│       style.css         # Archivo único de estilos CSS nativos para todo el sitio
│
├───templates/            # Plantillas HTML procesadas por Jinja2
│       admin.html        # Vista del Panel de Control Interno del Administrador
│       exito.html        # Comprobante/Ticket digital emitido tras agendar con éxito
│       formulario.html   # Formulario público de solicitud de citas
│
└───venv/                 # Entorno virtual de Python (Librerías del sistema)