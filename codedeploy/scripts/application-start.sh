#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy_apps/hexxy.media
pm2 start pm2.config.js
pm2 save
