#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="rabbitmq"
helm upgrade rabbitmq -f values.yaml -n ${namespace} --wait .
