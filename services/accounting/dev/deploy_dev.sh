#!/usr/local/bin/bash

export DB_NAME=accounting
export DB_USER=user
export DB_PASS=pass

docker-compose -f services/accounting/dev/docker-compose.yml up -d