#!/usr/local/bin/bash

if [[ "$(docker images -q service_image 2> /dev/null)" == "" ]]; then
  echo "Building base services image"
  docker build -f ./service_image.Dockerfile -t service_image .
fi

export OAUTH_SECRET=secret

./services/oauth/dev/restart_dev.sh
./services/task_tracker/dev/restart_dev.sh
./services/accounting/dev/restart_dev.sh