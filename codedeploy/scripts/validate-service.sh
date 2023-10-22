#!/bin/bash
set -euo pipefail

curl https://hexxy.media/api/v0/health --write-out "\n" --fail
