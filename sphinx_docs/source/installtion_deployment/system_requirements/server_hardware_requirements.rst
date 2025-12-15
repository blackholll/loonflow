Server Hardware Requirements
=============================

This section describes the baseline and recommended hardware requirements for running **LoonFlow**, including CPU, memory, disk, and network resources. Actual requirements will vary depending on the number of concurrent users, ticket volume, and the number of integrated systems. The values below are general guidelines for typical deployments.


Docker Compose Deployment
------------------------------

Suitable for personal evaluation, local development, feature verification, or small pilot environments, where all components (web application, database, Redis, etc.) are deployed on a single server.

**Minimum configuration**

- **CPU**: 4 vCPU
- **Memory**: 8 GB
- **Disk**: 40 GB of available space



.. important::

   When multiple components run on the same machine, memory is usually the first resource to become a bottleneck. If you frequently observe memory pressure or unstable services in test environments, first consider adding more memory or moving the database to a separate instance.


High Availability and Scalability Recommendations
--------------------------------------------------

For production environments that require higher stability and availability, consider the following enhancements based on your actual needs:

- **multiple backend or task instances**

  - use "replicas" attribute to start multiple backend or task instances in docker-compose.yml.

- **Database high availability**

  - use a separate database server, rather than starting on a single server through docker compose.

- **Monitoring and capacity planning**

  - Use monitoring systems (such as Prometheus + Grafana or cloud monitoring services) to track CPU, memory, I/O, database connections, and other key metrics.
  - Based on historical load and growth trends, plan CPU, memory, and disk expansions in advance to avoid emergency scaling during business peaks.

Summary
-------

Hardware planning should be based on your organization's actual business scale and future growth expectations. Ensure that LoonFlow has enough resources to run reliably while keeping some buffer for headroom. It is strongly recommended to perform stress testing before going live and adjust CPU, memory, and database configurations according to the test results to achieve a more robust production environment.


