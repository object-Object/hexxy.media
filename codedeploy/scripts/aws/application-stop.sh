#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy-apps/hexxy.media

sudo su object -c "pm2 --no-color --mini-list delete pm2.config.js || true"
