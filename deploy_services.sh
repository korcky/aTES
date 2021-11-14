#!/usr/local/bin/bash

if [[ "$(docker images -q service_image 2> /dev/null)" == "" ]]; then
  echo "Building base services image"
  docker build -f ./services/service_image.Dockerfile -t service_image ./services
fi

export OAUTH_SECRET=secret


./services/oauth/dev/deploy_dev.sh
./services/task_tracker/dev/deploy_dev.sh