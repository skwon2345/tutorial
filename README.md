# Microservices Tutorial

## Setup
1. In the first terminal, execute the following command in order to create and execute a `db` service container in `docker-compose.yml`.
```bash
$ docker-compose up -d db
```
2. In the second terminal, execute the following command in order to create and execute all service containers in `docker-compose.yml`.
```bash
$ docker-compose up
```
If you want to open `backend` shell, please execute the following command after `docker-compose up db` and `docker-compose up`
```bash
$ docker-compose exec backend sh
```
If you chaned your Dockerfile or any of your changes are not reflected to docker, run the following command to reflect the change to your container.
```bash
$ docker-compose up --build
```
Check all the runnning docker container.
```bash
$ docker-compose ps
or
$ docker ps
```
