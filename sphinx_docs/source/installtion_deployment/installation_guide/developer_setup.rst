Developer Setup
================

This guide will help you set up the Loonflow development environment on your local machine.

Prerequisites
-------------

Before starting, ensure you have the following installed:

- Python 3.12.x (latest stable version of Python 3.12)
- Node.js 22.x (latest stable version of Node.js 22)
- Redis (for generating unique ticket serial numbers and Celery async tasks)
- PostgreSQL(database)

Backend Setup
-------------

1. Navigate to the backend directory:

   .. code-block:: bash

      cd backend

2. Create configuration file:

   Copy ``settings/dev.py.sample`` to ``settings/config.py`` in the settings directory.

   .. code-block:: bash

      cp settings/dev.py.sample settings/config.py

3. Configure settings:

   Edit ``settings/config.py`` and update the following configurations:
   
   - Database configuration (connection settings)
   - Redis address configuration
   - Log path configuration
   - Other environment-specific settings

4. Create and activate a Python virtual environment:

   .. code-block:: bash

      python3.12 -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

5. Install dependencies:

   .. code-block:: bash

      pip install -r requirements/dev.txt

6. Start Redis:

   Redis is required for:
   
   - Celery async tasks (script execution, status hooks, notification hooks)
   
   Make sure Redis is running before proceeding.

7. Initialize the database:

   .. code-block:: bash

      python manage.py makemigrations
      python manage.py migrate

8. Create a superuser:

   .. code-block:: bash

      python manage.py createsuperuser

9. Start the backend server:

   .. code-block:: bash

      python manage.py runserver

   The backend will be available at ``http://{your_ip}:8000``.

Frontend Setup
--------------

1. Navigate to the frontend directory:

   .. code-block:: bash

      cd frontend

2. Install dependencies:

   .. code-block:: bash

      yarn install --immutable

3. Start the frontend development server:

   .. code-block:: bash

      yarn start

   The frontend will be available at ``http://{your_ip}:3000``.

Celery Worker (Optional)
------------------------

For local development, the Celery worker is optional unless you need the following features:

- Script execution
- Status hooks
- Notification hooks

If you need these features, start the Celery worker:

1. Navigate to the backend directory:

   .. code-block:: bash

      cd backend

2. Start the Celery worker:

   .. code-block:: bash

      celery -A tasks worker -l info -Q loonflow

Access the Application
----------------------

Once both the backend and frontend are running, access the application at:

   http://{your_ip}:3000

The frontend is configured to proxy API requests to the backend at ``http://{your_ip}:8000``.