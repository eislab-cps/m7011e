#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

namespace="db"
helm upgrade postgresql -f values.yaml -n ${namespace} --debug --wait .
