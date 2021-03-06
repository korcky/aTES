#!/usr/local/bin/bash

if [[ "$(docker images -q service_image 2> /dev/null)" == "" ]]; then
  echo "Building base services image"
  docker build -f ./service_image.Dockerfile -t service_image .
fi

export OAUTH_SECRET=secret

./services/oauth/dev/build_dev.sh
./services/task_tracker/dev/build_dev.sh
./services/accounting/dev/build_dev.sh
./services/analytics/dev/build_dev.sh
