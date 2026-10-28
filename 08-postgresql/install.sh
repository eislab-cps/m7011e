#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="db"
helm install postgresql -f values.yaml -n ${namespace} .
