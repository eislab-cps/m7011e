#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
kubectl --kubeconfig "$HOME/.kube/config" create namespace db --dry-run=client -o yaml | kubectl --kubeconfig "$HOME/.kube/config" apply -f -
