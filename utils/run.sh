#!/usr/bin/env bash

docker container prune -f
docker-compose up --build -d
docker ps -q | xargs -P 2 -I ID konsole --hide-menubar -e 'docker logs -f ID'
