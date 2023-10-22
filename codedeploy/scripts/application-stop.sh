#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy_apps/hexxy.media
sudo su object -c "pm2 stop pm2.config.js --no-color"
