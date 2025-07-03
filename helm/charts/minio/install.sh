#!/bin/bash

namespace="minio"
helm install ${namespace} -f values.yaml -n ${namespace} .
