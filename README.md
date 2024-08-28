# TalaTask

TalaTask es una aplicación de gestión de tareas para empleados, construida con Django y Django REST Framework. Permite asignar tareas a empleados basándose en sus habilidades y disponibilidad de horas y de dias en la semana.

## Requisitos Previos

- Python 3.9+
- Docker (opcional, para ejecución en contenedores)

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/talatask.git
cd talatask
```
Te encontraras con el directorio `env` y `TalaTask`.
El directorio `env` almacena las configuraciones y dependencias del entorno virtual utilizado para crear esta aplicacion en entorno de desarrollo, por lo que podemos eliminarlo para crear un nuevo entorno virtual en el siguiente paso.
El directorio `TalaTask` es la raiz de la aplicacion

## Configuración del Entorno Local

### 1. Crear y activar un entorno virtual

```bash
python -m venv env
source env/bin/activate  #en Windows usar `env\Scripts\activate`
```

Una vez activado el entorno virtual, entraremos al directorio de la aplicacion

```bash
cd TalaTask
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones

```bash
python manage.py migrate
```

### 4. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

### 5. Acceso a la consola de administración

El superusuario ya ha sido creado con las siguientes credenciales:
- Usuario: admin
- Contraseña: admin

Puedes acceder a la consola de administración en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Configuración con Docker

### 1. Construir y ejecutar los contenedores

```bash
docker-compose up --build
```
Una vez que el contenedor esta corriendo correctamente, aplicaremos las migraciones.

### 2. Aplicar migraciones

Debemos ingresare por consola lo siguiente:

```bash
docker-compose exec web python manage.py migrate
```

### 3. Acceso a la aplicacion

La aplicación estará disponible en [http://localhost:8000](http://localhost:8000) tal como se configuro en nuestro `docker-compose.yml`.

### 4. Acceso a la consola de administración

Puedes acceder a la consola de administración en [http://localhost:8000/admin/](http://localhost:8000/admin/) con las credenciales del superusuario ya creado:
- Usuario: admin
- Contraseña: admin

## Crear Employees, Skills y Tasks

### Crear Skills

En la consola de administración, navega a `Skills` y crea las habilidades necesarias. Las habilidades esta organizadas en cuatro dimensiones:
- Tecnología (`tech`)
- Comunicación (`com`)
- Liderazgo (`lead`)
- Procesos (`proc`)

Cada dimensión tiene 3 niveles (por ejemplo, tech_lvl_1, tech_lvl_2, tech_lvl_3).
*Nota: Si un empleado tiene un nivel 2 en una dimensión, también debería tener el nivel 1, aunque esta validación no está implementada en el código.*

### Crear Employees

En la consola de administración, navega a `Employees` y crea empleados asignándoles habilidades previamente creadas, especificando sus horas disponibles por día y los días de la semana en los que están disponibles.
**Las horas disponibles por dia, indican el promedio de horas semanales que tiene un `Employee`. Es decir, que si el `Employee` tiene 2 dias disponibles, y 4 horas disponibles, entonces, el `Employee` tiene 8 (2 x 4) horas totales disponibles en la semana.**

### Crear Tasks

En la consola de administración, navega a `Tasks` y crea tareas especificando las habilidades requeridas, la duración y la fecha de la tarea.
**La duracion de las tareas, indica el total de horas que toma realizar una tarea**

## Endpoint de Asignación de Tareas

Puedes consultar las asignaciones de tareas utilizando el siguiente endpoint `GET /api/assign/`.
Esto se puede realizar directamente sobre el navegador, dirijiendose a la ruta `/api/assign/`.

Este endpoint devuelve un reporte sobre cómo las tareas han sido asignadas a los empleados `Employee`, considerando sus habilidades `Skill` y disponibilidad.

## Consideraciones de respuestas HTML

No se han configurado mas endpoints aparte del entregado por defecto por django (`/admin`) y el endpoint para la respuesta de la asignacion de tareas (`/api/assign/`).

## Deudas de experiencia

### Calculo de horas desde la hora actual al final del dia de la fecha de entrega de la tarea
- Actualmente se estan calculando las horas disponibles del `Employee` suponiendo que este aun tiene disponibles las horas del dia en el cual se esta haciendo la consulta. Faltaria agregar un rango horario de trabajo del `Employee` de manera de saber de mayor precision para las fechas borde.

### Encolamiento de peticiones

- Para mejorar la experiencia del usuario, es importante que podamos encolar las peticiones http al endpoint `/api/assign/` de manera evitar problemas al intentar actualizar algun registro de `Employee` y `Task`. Esto asegurara que no podamos asignar tareas 2 o mas veces al existir dos o mas peticiones simultaneas.

### Mejora de performance en `TalaTask\tasks\services.py`

- Actualmente se estan iterando por todos los `Employee` por cada `Task` sin asignar. Esto genera un orden de complejidad O(m*n), donde m es numero de tareas, y n el numero de empleados, por lo cual se debe mejorar la forma en que se estan asignando las tareas.

## Opcion para mejora de performance
- Dividir la operacion en batches asincronos y responder a la peticion una vez que la operacion de todos los batches haya acabado.

### Tests de la aplicacion
Actualmente, en `TalaTask\tasks\tests.py` se estan probando los servicios de `TalaTask\tasks\services.py`. Para ejecutar los tests, por consola, se debe ingresar lo siguiente:

```bash
python manage.py test
```

### Uso de factory boy para crear empleados y tasks masivamente

Para probar el performance de la aplicacion, se recomienda que se utilice gran cantidad de datos. Para eso, podemos utilizar Factory Boy a traves de la shell de django.
Para eso, ingresemos a la shell.

```bash
python manage.py shell
```

Una vez dentro, ingresaremos el siguiente codigo:

```bash
from tasks.factories import EmployeeFactory, TaskFactory

for _ in range(100):
    EmployeeFactory.create()

# Crear tareas
for _ in range(200):
    TaskFactory.create()
```

Esto creara 100 `Employee` y 200 `Task`. Considere generar 1000 empleados y 2000 tasks para realizar pruebas del endpoint.