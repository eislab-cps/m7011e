#!/bin/bash

namespace="monitoring"

echo "Uninstalling monitoring stack from namespace: ${namespace}"

helm uninstall monitoring -n ${namespace}

echo "Monitoring stack uninstalled!"
