# 📚 API REST Biblioteca - Sena

Esta es una API REST robusta para la gestión de una biblioteca, desarrollada con **Django** y **Django REST Framework**. Permite administrar autores, libros y el ciclo de vida de los préstamos (préstamo y devolución) con validaciones de disponibilidad.

## 🚀 Características

* **CRUD Completo**: Gestión de Autores, Libros y Préstamos.
* **Filtrado y Búsqueda**: Búsqueda por título, autor o género y filtrado por disponibilidad.
* **Acciones Personalizadas**:
    * `GET /api/libros/disponibles/`: Lista solo libros listos para préstamo.
    * `POST /api/libros/{id}/prestar/`: Realiza el préstamo de un ejemplar.
    * `POST /api/prestamos/{id}/devolver/`: Gestiona la devolución y actualiza el stock automáticamente.
* **Seguridad**: Los préstamos están protegidos y solo pueden ser gestionados por usuarios autenticados.

## 🛠️ Tecnologías utilizadas

* **Python 3.13**
* **Django 6.0**
* **Django REST Framework**
* **Django Filters** (Para búsquedas avanzadas)
* **SQLite** (Base de datos por defecto)

## 🔧 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto localmente:

1.  **Clonar el repositorio**:
    ```bash
    git clone [https://github.com/ZharithBedoya/Construcci-n-de-API-REST.git](https://github.com/ZharithBedoya/Construcci-n-de-API-REST.git)
    cd Construcci-n-de-API-REST
    ```

2.  **Crear un entorno virtual** (Recomendado):
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install django djangorestframework django-filter
    ```

4.  **Aplicar migraciones**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crear un superusuario** (Para acceder al admin y probar la API):
    ```bash
    python manage.py createsuperuser
    ```

6.  **Iniciar el servidor**:
    ```bash
    python manage.py runserver
    ```

## 📖 Uso de la API

Una vez iniciado el servidor, puedes acceder a la interfaz navegable en:
`http://127.0.0.1:8000/api/`

### Endpoints Principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/autores/` | Listar todos los autores |
| GET | `/api/libros/` | Listar todos los libros |
| GET | `/api/libros/disponibles/` | Ver libros que no están prestados |
| POST | `/api/libros/{id}/prestar/` | Prestar un libro (Requiere Token) |
| POST | `/api/prestamos/{id}/devolver/` | Devolver un libro (Requiere Token) |

## 👤 Autora
* **Zharith Alexandra Bedoya** - *Desarrollo Inicial* - [ZharithBedoya](https://github.com/ZharithBedoya)
