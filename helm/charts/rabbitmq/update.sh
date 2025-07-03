#!/bin/bash

namespace="rabbit"
helm upgrade rabbitmq -f values.yaml -n ${namespace} --wait .
