#!/usr/local/bin/bash

export OAUTH_SECRET=secret

./services/oauth/dev/down_dev.sh
./services/task_tracker/dev/down_dev.sh
./services/accounting/dev/down_dev.sh
./services/analytics/dev/down_dev.sh