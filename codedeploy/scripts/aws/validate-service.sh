#!/bin/bash
set -euo pipefail

sleep 10s  # give it time to start up
curl https://hexxy.media/api/v0/health --write-out "\n" --fail
