#!/bin/bash

namespace="minio"
helm upgrade minio -f values.yaml -n ${namespace} --wait .
