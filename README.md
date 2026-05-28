# Sistema de Gestión de Turnos - Policía de Río Negro

Este proyecto es una aplicación web minimalista, responsiva y autocontenida desarrollada para la gestión de turnos administrativos del **Certificado de Antecedentes Penales** de la Policía de la Provincia de Río Negro. El desarrollo fue concebido bajo los lineamientos y estándares solicitados para la cátedra de **Sistemas de Información II**.

## 🚀 Funcionalidades Principales

El sistema resuelve la problemática de asignación de turnos mediante una arquitectura de software limpia y validaciones en dos capas (Cliente-Servidor):

1. **Formulario Público Dinámico (`/`)**:
* Registro de datos del ciudadano: Nombre, Apellido, DNI, Teléfono y Email.
* Calendario inteligente que bloquea de forma interactiva fechas pasadas y fines de semana.
* **Validación del lado del Cliente (JS)**: Comprobación de formatos de texto, DNI de 7 u 8 dígitos, celulares argentinos de 10-11 dígitos y correos electrónicos válidos antes de enviar la solicitud.
* **Consulta de Disponibilidad en Tiempo Real**: API dinámica que consulta la base de datos y deshabilita los horarios que ya están ocupados por otros usuarios para la fecha elegida.


2. **Validación de Servidor Robusta (`lib/validation.py`)**:
* Capa de seguridad backend mediante Expresiones Regulares (regex) para evitar inyecciones de datos corruptos o bypass de validaciones del navegador.


3. **Persistencia Local (`lib/database.py`)**:
* Base de datos relacional ultraligera basada en **SQLite3**.
* Restricción lógica para garantizar la unicidad de las citas (no pueden existir dos turnos activos para el mismo día y la misma hora).


4. **Panel de Control Administrativo (`/admin`)**:
* Listado completo de todas las solicitudes registradas, ordenadas de forma cronológica (fecha y hora).
* **Baja Lógica (Borrado Lógico)**: Al cancelar un turno, el registro no se elimina físicamente de la base de datos (preservando el historial de auditoría del sistema). El estado cambia a `cancelado`, liberando automáticamente el horario para que otro ciudadano pueda reservarlo.


5. **Alineación Estética Nv-1**:
* Estilo minimalista y profesional adaptado a la paleta institucional (azules policiales, gris de fondo y tipografía moderna), implementado mediante CSS nativo (`static/style.css`) sin dependencias externas (CDNs) ni frameworks que ralenticen la carga del sitio.



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
│       admin.html        # Vista del Panel de Control Interno del Administrator
│       exito.html        # Comprobante/Ticket digital emitido tras agendar con éxito
│       formulario.html   # Formulario público de solicitud de citas
│
└───venv/                 # Entorno virtual de Python (Librerías del sistema)

```

## 🛠️ Detalle de los Archivos Clave

* **`main.py`**: Es el núcleo de la aplicación. Configura la aplicación Flask, expone los endpoints públicos, las APIs dinámicas y la sección de administración, gestionando el flujo de datos entre el frontend, las validaciones y la persistencia.
* **`lib/database.py`**: Contiene las instrucciones SQL que crean la tabla de la base de datos y controlan los estados (`activo` / `cancelado`) de los registros. No permite borrados físicos para asegurar la trazabilidad del sistema.
* **`lib/validation.py`**: Módulo que aplica expresiones regulares y lógica matemática en el servidor para verificar que ningún campo esté vacío, que la fecha no haya expirado y que las citas se programen únicamente dentro de la lista blanca de horarios (`08:00 a 13:00`).
* **`static/style.css`**: Almacena de forma centralizada la estética visual de la app, implementando layouts modernos mediante Flexbox y CSS Grid para garantizar que el sistema sea responsivo (adaptable a celulares, tablets y computadoras).
* **`templates/`**: Almacena las páginas del sistema. La comunicación de datos dinámicos entre el backend en Python y estas pantallas se procesa mediante las etiquetas de renderizado de Jinja2 (como `{% if %}` y `{{ variable }}`).

## 🎨 Criterios de Diseño Adoptados (UI / UX)

El desarrollo del sistema se estructuró siguiendo estrictamente los principios de diseño de interfaz de usuario y experiencia de usuario analizados en la materia:

### 1. Enfoque Basado en el Modelo del Diseñador (Look-and-Feel Iceberg)

Siguiendo las pautas de diseño arquitectónico, no se priorizó una "cara bonita" superficial al inicio del desarrollo. El diseño comenzó desde la base del iceberg: las **Relaciones entre Objetos** (esquema de base de datos relacional y restricciones lógicas), continuó con las **Técnicas de Interacción** (APIs dinámicas de consulta y eventos JS), y decantó naturalmente en la **Presentación Visual**. Esto garantiza que el software se adapte sólidamente al modelo mental y a las expectativas reales del usuario final.

### 2. Establecimiento de Punto Focal y Jerarquía Visual

Respetando las pautas de lectura occidentales, donde los usuarios inician la exploración en la parte superior izquierda de la pantalla, se ubicó allí la identidad institucional y el logotipo de la Policía de Río Negro. A partir de este eje, se construyó el **Punto Focal** principal mediante una tarjeta centralizada (`.card`) aislada visualmente del fondo con sombras suaves (`box-shadow`), guiando el orden en la ejecución de las tareas de manera comprensible y fluida.

### 3. Consistencia, Legibilidad y Aplicación de la Ley de Fitt

* **Consistencia**: Se estandarizó la interfaz mediante un diseño constante en las tres ventanas del sistema (`formulario`, `exito` y `admin`), manteniendo cabeceras, pies de página y estructuras homogéneas.
* **Legibilidad**: El layout cuenta con alineaciones basadas en CSS Grid y un espaciado equilibrado que maximiza la legibilidad. El uso del color se consideró una herramienta informativa secundaria: se aplicó una paleta homogénea, sobria y de alta resolución (texto oscuro `#1e293b` sobre fondo blanco o amarillo sutil de precaución) apropiada para aplicaciones de corte institucional.
* **Ley de Fitt**: El botón principal de confirmación se diseñó a lo ancho de todo el contenedor (`width: 100%`) y con un área de clic grande, reduciendo significativamente el tiempo que le toma al usuario alcanzar el objetivo de control.

### 4. Supresión de Valores por "Defecto" y Anticipación Cognitiva

En cumplimiento estricto con las directrices de UX que prohíben el uso de textos genéricos por "defecto", el elemento `<select>` de horarios utiliza mensajes dinámicos inteligentes para anticiparse a las necesidades del ciudadano. Al ingresar al sitio, se muestra la frase informativa *"Primero seleccione fecha"*; al cambio del calendario, se actualiza a *"Cargando horarios disponibles..."*; y finalmente se muta a *"Seleccione horario"*.

### 5. Arquitectura de Retroalimentación (Feedback) Efectiva

El sistema implementa mecanismos explícitos para mantener al usuario informado en tiempo real:

* **Notificación de Entrada Incorrecta (Feedback Tipo 3)**: Al perder el foco un campo inválido (DNI, Email, Celular), el campo se tiñe sutilmente de rojo (`:user-invalid`) y expone inmediatamente una etiqueta explicativa (`.error-feedback`) detallando cómo corregir el problema.
* **Aceptación de la Solicitud Completa (Feedback Tipo 5)**: Al procesar la reserva con éxito en el backend, la aplicación rompe con respuestas secas u "extrañas" (como el texto plano "Entrada Aceptada"). En su lugar, emite una interfaz dedicada de comprobante impreso en pantalla (`exito.html`) que confirma de manera positiva que la acción se completó correctamente.

### 6. Descentralización de Datos y Reducción de Latencia (Auditoría del Sistema)

La aplicación implementa técnicas eficientes que colocan las computaciones pesadas en segundo plano (consultas asíncronas vía `fetch` / AJAX), permitiendo una interacción fluida y minimizando la latencia percibida por el usuario. Adicionalmente, el sistema captura características clave de auditoría (asentando marcas de tiempo de fecha y hora exacta en SQLite), y facilita la descentralización de datos a nivel provincial al procesar de forma local y segura la base de datos de los ciudadanos.

## 🛠️ Tecnologías Utilizadas

Para garantizar que la aplicación sea liviana, eficiente y modular, se seleccionó un stack tecnológico robusto y sin dependencias externas innecesarias:

* **Backend**: **Python** con el microframework **Flask** para la gestión de enrutamiento, controladores de API y renderizado de plantillas.
* **Persistencia**: **SQLite3**, un motor de bases de datos relacional autocontenido y serverless, ideal para el almacenamiento local estructurado y trazabilidad de auditorías mediante SQL nativo.
* **Frontend**: **HTML5** estructurado semánticamente y **Jinja2** como motor de plantillas dinámicas del lado del servidor.
* **Estilos**: **CSS3 nativo** avanzado (utilizando layouts basados en **Flexbox** y **CSS Grid** para asegurar la adaptabilidad responsiva) junto con pseudo-clases de validación modernas como `:user-invalid`.
* **Lógica del Cliente**: **JavaScript asíncrono (Vanilla JS)** para el manejo de eventos del DOM, manipulación dinámica del calendario y peticiones HTTP en segundo plano mediante la API **Fetch**.

## ⚙️ Puesta en Marcha (Instalación y Uso)

Seguí los pasos correspondientes a tu sistema operativo en la terminal para ejecutar el sistema de forma local:

### 🪟 En Windows (PowerShell / CMD)

1. **Ubicarse en la carpeta del proyecto**:
Abrí la terminal dentro del directorio raíz de la aplicación:
```powershell
cd C:\Users\benabhi\Documents\Code\python\turnos_app

```


2. **Activar el Entorno Virtual (`venv`)**:
* Si usás **PowerShell**:
```powershell
.\venv\Scripts\Activate.ps1

```


* Si usás **CMD (Símbolo del sistema)** clásico:
```cmd
.\venv\Scripts\activate.bat

```




*Sabrás que está activo porque aparecerá el prefijo `(venv)` al inicio de la línea de comandos.*
3. **Instalar dependencias**:
```powershell
pip install -r requirements.txt

```


4. **Ejecutar el Servidor**:
```powershell
python main.py

```



### 🐧 En Linux (Ubuntu / Debian / Mint)

1. **Ubicarse en la carpeta del proyecto**:
Abrí la terminal y navegá hasta el directorio donde clonaste o descomprimiste la app:
```bash
cd /ruta/hacia/tu/carpeta/turnos_app

```


2. **Activar el Entorno Virtual (`venv`)**:
```bash
source venv/bin/activate

```


*Sabrás que está activo porque tu indicador de la terminal cambiará para mostrar `(venv)` al principio.*
3. **Instalar dependencias**:
Asegurate de tener el gestor de paquetes actualizado e instalá los requerimientos:
```bash
pip install -r requirements.txt

```


4. **Ejecutar el Servidor**:
```bash
python3 main.py

```



### 🌐 Acceder a la aplicación (Cualquier Sistema Operativo)

Una vez que el servidor esté corriendo, abrí tu navegador web de preferencia e ingresa a las siguientes direcciones locales:

* **Sección Pública (Formulario de reserva)**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Sección Privada (Panel de Administración)**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)