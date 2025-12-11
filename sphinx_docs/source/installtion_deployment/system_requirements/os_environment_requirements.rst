OS Environment Requirements
====================================

This section describes the operating system requirements for running **LoonFlow**.

Linux (Recommended)
--------------------

**LoonFlow is recommended to run on Linux operating systems, which is the preferred choice for production environments.**

Supported All major Linux distributions:

.. note::
   Linux operating system is strongly recommended for production environments to ensure system stability and performance.

Windows (Development Only)
--------------------------

**Windows operating system is not recommended for running LoonFlow in production environments.**

Since LoonFlow's asynchronous tasks are implemented using Celery, there may be compatibility issues on Windows systems, causing asynchronous tasks to fail to work properly. Here is some compatibility resoves https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows:

.. warning::
   you can use Windows as a development environment, but may encounter issues such as asynchronous task execution exceptions.

macOS (Development Only)
------------------------

**macOS can be used as a development environment, but is not recommended for production environments.**

Supported common macOS versions.

.. note::
   macOS is suitable for local development and testing, but is not recommended for production environment deployment. Linux operating system should be used for production environments.