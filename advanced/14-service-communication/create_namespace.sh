#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="rabbitmq"
kubectl create namespace "$namespace" --dry-run=client -o yaml | kubectl apply -f -
