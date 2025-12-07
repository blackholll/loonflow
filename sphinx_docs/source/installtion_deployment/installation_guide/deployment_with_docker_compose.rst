Deployment with Docker Compose
================================

This guide will help you deploy Loonflow in a production environment using Docker Compose.

Prerequisites
-------------

Before starting, ensure you have the following requirements:

- Linux server (refer to :ref:`server_hardware_requirements`)
- Docker 20.10+ installed
- Docker Compose 2.0+ installed


Installing Docker and Docker Compose
------------------------------------

If Docker and Docker Compose are not yet installed on your server, follow these steps:

1. Install Docker:

   .. code-block:: bash

      # Ubuntu/Debian
      curl -fsSL https://get.docker.com -o get-docker.sh
      sudo sh get-docker.sh

      # CentOS/RHEL
      sudo yum install -y docker
      sudo systemctl start docker
      sudo systemctl enable docker

2. Install Docker Compose:

   .. code-block:: bash

      # Download the latest version of Docker Compose
      sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose

3. Verify installation:

   .. code-block:: bash

      docker --version
      docker-compose --version

Downloading Docker Compose Configuration Files
----------------------------------------------

1. Create a deployment directory:

   .. code-block:: bash

      mkdir -p /opt/loonflow
      cd /opt/loonflow

2. Download the necessary configuration files:

   .. code-block:: bash

      wget https://raw.githubusercontent.com/blackholll/loonflow/refs/heads/master/docker_compose_deploy/docker-compose.yml
      wget https://raw.githubusercontent.com/blackholll/loonflow/refs/heads/master/docker_compose_deploy/.env

   Alternatively, if you have already cloned the repository, you can copy the files directly:


Configuring Environment Variables
----------------------------------

Edit the ``.env`` file to configure the following necessary environment variables:

.. code-block:: bash

   # Edit the .env file
   vi .env

**Important Configuration Items:**

- **Database Configuration**:
  
  - ``POSTGRES_USER``: PostgreSQL database username (default: loonflow)
  - ``POSTGRES_PASSWORD``: PostgreSQL database password (**must be changed**)
  - ``POSTGRES_DB``: Database name (default: loonflow)
  - ``POSTGRES_PORT``: PostgreSQL port (default: 5432)

- **Redis Configuration**:
  
  - ``REDIS_PASSWORD``: Redis password (**must be changed**)
  - ``REDIS_PORT``: Redis port (default: 6379)

- **Administrator Account Configuration**:
  
  - ``ADMIN_EMAIL``: Administrator email (for login)
  - ``ADMIN_NAME``: Administrator username
  - ``ADMIN_PASSWORD``: Administrator password (**must be changed**)

- **Tenant Configuration**:
  
  - ``TENANT_NAME``: Tenant name
  - ``TENANT_DOMAIN``: Tenant domain

- **Data Volume Configuration**:
  
  - ``PG_DATA_VOLUME``: PostgreSQL data volume name (for data persistence)

**Security Note:** Please ensure to change all password-related configuration items and use strong passwords to ensure system security.

Starting Services
-----------------

1. Ensure you are in the directory containing the ``docker-compose.yml`` file:

   .. code-block:: bash

      cd /opt/loonflow

2. Start all services:

   .. code-block:: bash

      docker-compose up -d

   This command will start the following services in the background:

   - **loonflow-redis**: Redis service (for generating ticket serial numbers and Celery async tasks)
   - **loonflow-pg**: PostgreSQL database service
   - **loonflow-backend**: Loonflow backend service (Django + Gunicorn)
   - **loonflow-ui**: Loonflow frontend service (Nginx)
   - **loonflow-task**: Celery task processing service

3. Check service status:

   .. code-block:: bash

      docker-compose ps

4. View service logs (optional):

   .. code-block:: bash

      # View logs for all services
      docker-compose logs -f

      # View logs for a specific service
      docker-compose logs -f loonflow-backend

Accessing the Application
-------------------------

After the services are started, you can access Loonflow through your browser:

- **Access URL**: ``http://your_server_ip:80``

- **Login Credentials**:
  
  - Email: The ``ADMIN_EMAIL`` you configured in the ``.env`` file
  - Password: The ``ADMIN_PASSWORD`` you configured in the ``.env`` file

Common Management Commands
--------------------------

- **Stop services**:

  .. code-block:: bash

     docker-compose stop

- **Start services**:

  .. code-block:: bash

     docker-compose start

- **Restart services**:

  .. code-block:: bash

     docker-compose restart

- **Stop and remove containers**:

  .. code-block:: bash

     docker-compose down

- **Stop and remove containers and volumes** (**Warning: This will delete database data**):

  .. code-block:: bash

     docker-compose down -v

- **Update services**:

  .. code-block:: bash

     # Pull the latest images
     docker-compose pull
     
     # Recreate and start containers
     docker-compose up -d

Troubleshooting
---------------

If you encounter issues, try the following steps:

1. **Check service status**:

   .. code-block:: bash

      docker-compose ps

2. **View service logs**:

   .. code-block:: bash

      docker-compose logs [service_name]

3. **Check port usage**:

   .. code-block:: bash

      # Check if port 80 is in use
      netstat -tulpn | grep :80

4. **Check firewall settings**:

   Ensure the firewall allows the following ports:
   
   - 80: HTTP access
   - 8000: Backend API (if direct access is needed)
   - 5432: PostgreSQL (if external access is needed)
   - 6379: Redis (if external access is needed)

5. **Restart service**:

   .. code-block:: bash

      docker-compose restart [service_name]

Important Notes
---------------

- On first startup, the backend service will automatically perform database migrations and create a superuser, which may take a few minutes
- Ensure the server has sufficient resources (CPU, memory, disk space)
- Regularly backup the PostgreSQL data volume (``pg_data``)
- Production environments should configure HTTPS and a reverse proxy
