#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="rabbitmq"
helm install rabbitmq -f values.yaml -n ${namespace} .
