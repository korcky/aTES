#!/usr/local/bin/bash

export DB_NAME=analytics
export DB_USER=user
export DB_PASS=pass

docker-compose -f services/analytics/dev/docker-compose.yml build