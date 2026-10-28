#!/bin/bash

namespace="rabbitmq"
helm upgrade rabbitmq -f values.yaml -n ${namespace} --wait .
