#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
helm upgrade mongodb -f values.yaml -n db .
