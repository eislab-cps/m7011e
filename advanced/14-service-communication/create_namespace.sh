#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="rabbitmq"
kubectl --kubeconfig "$HOME/.kube/config" create namespace "$namespace" --dry-run=client -o yaml | kubectl --kubeconfig "$HOME/.kube/config" apply -f -
