#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy-apps/hexxy.media

python3.11 -m venv venv --clear
source venv/bin/activate
pip install --find-links dist "hexxy.media[runtime]"
