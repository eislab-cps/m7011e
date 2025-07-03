#!/bin/bash

namespace="rabbitmq"

kubectl create namespace ${namespace}
helm install ${namespace} -f values.yaml -n ${namespace} .
