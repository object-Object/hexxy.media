#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy-apps/hexxy.media

sudo su object -c "pm2 start pm2.config.js --no-color"
sudo su object -c "pm2 save --no-color"
