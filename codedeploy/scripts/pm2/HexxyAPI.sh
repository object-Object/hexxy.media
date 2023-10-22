#!/bin/bash
set -euo pipefail

source venv/bin/activate
python -m hexxy_media.api.app
