#!/bin/bash
set -euo pipefail

cd /var/lib/codedeploy-apps/hexxy.media

rm -rf venv
uv venv venv --python 3.11 --seed
source venv/bin/activate
uv pip install --find-links dist "hexxy.media[runtime]" --constraints dist/requirements.txt
