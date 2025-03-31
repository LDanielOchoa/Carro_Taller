# Sistema de Control del Carro Taller

Este sistema permite gestionar las salidas y entradas del carro taller de la empresa, eliminando la dependencia de registros físicos y mejorando la trazabilidad de la información.

## Características principales
- **Registro de salidas**: Se ingresan los datos del operador, acompañante, motivo de salida, fecha, etc.
- **Control de ingreso**: Se ingresa el estado de las partes del vehículo al regresar.
- **Evidencias fotográficas**: Se guardan las evidencias fotográficas registradas con daños.
- **Historial de movimientos**: Permite auditar y consultar registros anteriores para un mejor control del uso del vehículo.

## Arquitectura del Sistema
El sistema está desarrollado con el framework **Django** siguiendo el patrón **Model-Template-View (MTV)**:
- **Modelos**: Representan la estructura de la base de datos mediante el ORM de Django.
- **Vistas**: Gestionan la lógica del negocio y la interacción con los modelos.
- **Plantillas**: Manejan la presentación con HTML, CSS y Bootstrap.

## Tecnologías utilizadas
- **Backend**: Django 5.1.5, Django Templates, Django ORM, Asgiref 3.8.1, sqlparse 0.5.3
- **Frontend**: Bootstrap, HTML5, CSS3, JavaScript, AJAX
- **Base de Datos**: MySQL con mysqlclient y pyodbc
- **Seguridad**: Middleware de Django, autenticación y protección CSRF
- **Manejo de archivos**: Configuración de archivos estáticos y multimedia con Pillow y tzdata

## Estructura del Proyecto
El proyecto se organiza en carpetas siguiendo la estructura de Django:
```
CarroTaller/
│── Public/
│── Templates/
    │── home/
    │── inc/
    │── registration/
    │── registros/
    │── Usuarios/
│── __init__.py
│── asgi.py
│── decoradores.py
│── forms.py
│── models.py
│── settings.py
│── urls.py
│── views.py
│── wsgi.py
│── media/
│── staticfiles/
│── gitignore
│── README.md
│── manage.py
│── requirements.txt
```

## Base de Datos
El sistema gestiona los registros mediante las siguientes tablas principales:
- `registros`: Almacena información sobre las salidas y entradas del carro taller.
- `detallecarro`: Guarda el estado de las partes del vehículo al ingresar.
- `fotosdetalle`: Contiene las imágenes de evidencia del estado del vehículo.

### Creación de la Base de Datos
```sql
CREATE DATABASE controlcarrotaller;

USE controlcarrotaller;

CREATE TABLE registros(
    id int PRIMARY KEY AUTO_INCREMENT,
    cedula_operador varchar (25) not null, 
    codigo_operador varchar (50) not null,
    nombre_operador varchar (50) not null,
    cedula_acompanante varchar (25) not null,
    nombre_acompanante varchar (50) not null,
    cargo_acompanante varchar (50) not null,
    fecha date not null,
    hora_salida time not null,
    hora_entrada time,
    kilometraje_salida varchar (50) not null,
    kilometraje_entrada varchar (50) not null,
    motivo_salida varchar (30) not null,
    autorizacion varchar (50) not null,
    observaciones varchar (100), 
    estado_registro int not null,
    vigilante_asignado_id int,
    ultimo_vigilante_id int,
    FOREIGN KEY (ultimo_vigilante_id) REFERENCES  auth_user(id),
    FOREIGN KEY (vigilante_asignado_id) REFERENCES auth_user(id));

CREATE TABLE detallecarro(
    id int PRIMARY KEY AUTO_INCREMENT,
    puerta_faldon_delantero_conductor varchar(20) not null, 
    puerta_trasera_conductor varchar(20) not null,
    puerta_faldon_delantero_copiloto varchar(20) not null,
    puerta_trasera_copiloto varchar(20) not null,
    techo_capot varchar(20) not null,
    boomper_delantero varchar(20) not null,
    boomper_trasero_tapamaleta varchar(20) not null,
    llanta_delantera_izquierda varchar(20) not null,
    llanta_trasera_izquierda varchar(20) not null,
    llanta_delantera_derecha varchar(20) not null,
    llanta_trasera_derecha varchar(20) not null,
    faldon_trasero_izquierdo varchar(20), 
    faldon_trasero_derecho varchar(20) not null,
    registro_carro_id int,
    FOREIGN KEY (registro_carro_id) REFERENCES registros(id));

CREATE TABLE fotosdetalle(
    id int PRIMARY KEY AUTO_INCREMENT,
    parte varchar (100) not null,
    imagen varchar (200) not null,
    detalle_carro_id int,
    FOREIGN KEY (detalle_carro_id) REFERENCES detallecarro(id));


```

## Respaldo de la Información
Se recomienda realizar backups cada 15 días (o semanalmente si hay un alto volumen de registros) para garantizar la seguridad de la información.

## Instalación y Configuración
1. Clona el repositorio:
   ```bash
   git clone https://github.com/JhonatanUsugaSao6/ControlCarroTaller-Compras-Reman-.git
   ```
2. Instala las dependencias:
   ```bash
   SECRET_KEY = tu-clave-seguridad

    DEBUG = True o False

    ALLOWED_HOSTS = localhost, 127.0.0.1

    # Base de datos SQL Server (Siesa)
    ENGINE_SQL=tu-engine-siesa
    NAME_SQL=tu-tabla
    USER_SQL=tu-usuario
    PASSWORD_SQL=tu-contraseña
    HOST_SQL=tu-host
    PORT_SQL=tu-puerto
    DRIVER=tu-drive-odbc

    # Base de datos MySQL (Default)
    ENGINE_MYSQL=tu-engine
    NAME_MYSQL=tu-tabla
    USER_MYSQL=tu-usuario
    PASSWORD_MYSQL=tu-contraseña
    HOST_MYSQL=tu-host
    PORT_MYSQL=tu-puerto
    INIT=SET sql_mode='STRICT_TRANS_TABLES'
   ```

3. Crear archivo .env:
   ```bash
   pip install -r requirements.txt
   ```

4. Realiza las migraciones de la base de datos:
   ```bash
   python manage.py migrate
   ```
5. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

## Posibles Problemas
1. No se puede ver la información de un registro desde el icono del listado de registros (el ojo) si no tiene la hora de entrada ingresada, se debe completar primero el registro. 

