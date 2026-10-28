#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
kubectl create namespace db --dry-run=client -o yaml | kubectl apply -f -
