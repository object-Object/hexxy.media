#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy_apps/hexxy.media
pm2 stop pm2.config.js
