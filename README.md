# eVariant

The repository contains the main code of eVariant web app.

A fully functional example can be found:

<a href="http://167.235.206.155/" target="_blank">eVariant</a>

The application is a dockerized fullstack web app powered by NGINX as reverse proxy that connects frontend (HTML+CSS+JS) and backend (FastAPI python) on a single entry. Also a MySQL database is used.

The deployment is done via Ubuntu Virtual Machine and it is continously integrated via github. Every push triggers a new docker set up.

# Server (VM)

The server can be accessed via SSH:
The app is located on /home/evariant

Server has the following features

    PRETTY_NAME="Ubuntu 22.04.2 LTS"
    NAME="Ubuntu"
    VERSION_ID="22.04"
    VERSION="22.04.2 LTS (Jammy Jellyfish)"


# Fullstack application

As mentioned before, the app consists on HTML+CSS+JS for the frontend, fastAPI (Python) for the backend and MySQL for data persistence.

__Client folder__ holds the frontend, __Server folder__ the backend and __mysql folder__ the initial script to setup the database.

# Run the app: development and Production

In this case, it is consider development environment the local machine and production environment the external server.

You can change and test locally the application via docker compose command or push changes to git in order to test them in production (public IP of server).

To run the project locally you must be placed on root directory (where the docker-compose.yml file is located) and run the following command:

docker compose up -d --build

The files are live-upload to docker container, but if you notice no change are displayed,
rerun the command again.

## Deployment

The app is automatically deployed when a change is pushed on the main branch via github actions.

## Developmpent

For development, a 'development' branch has been created. This branch does not trigger any new deployment.
