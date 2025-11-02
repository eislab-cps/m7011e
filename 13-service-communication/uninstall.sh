#!/bin/bash

namespace="rabbitmq"
helm uninstall rabbitmq -n ${namespace}
