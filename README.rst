Trixie is a CMDB which focuses on reporting on services. It aims to be flexible in what is reported on and
tries not to make assumptions on what the definition of a service is.

Installation
============

Configuration
-------------

You can adjust settings in the .env file.::

Local installation using docker
-------------------------------

Install docker and docker-compose.

.. code-block:: console

        git clone git://github.com/tijmenvandenbrink/trixie.git
        docker-compose -f docker-compose-dev.yml build
        docker-compose -f docker-compose-dev.yml up -d
        docker-compose -f docker-compose-dev.yml run django python manage.py migrate