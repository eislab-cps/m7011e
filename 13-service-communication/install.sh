#!/bin/bash

namespace="rabbitmq"
helm install rabbitmq -f values.yaml -n ${namespace} .
