#!/bin/bash
set -euo pipefail

for _ in {1..3}; do
    sleep 15s  # give it time to start up
    if curl https://hexxy.media/api/v0/health --write-out "\n" --fail; then
        exit 0
    fi
done

exit 1
