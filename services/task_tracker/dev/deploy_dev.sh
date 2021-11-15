#!/usr/local/bin/bash

export DB_NAME=oauth
export DB_USER=user
export DB_PASS=pass

docker-compose -f services/task_tracker/dev/docker-compose.yml up -d