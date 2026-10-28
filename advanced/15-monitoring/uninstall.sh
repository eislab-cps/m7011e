#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="monitoring"

echo "Uninstalling monitoring stack from namespace: ${namespace}"

helm uninstall monitoring -n ${namespace}

echo "Monitoring stack uninstalled!"
