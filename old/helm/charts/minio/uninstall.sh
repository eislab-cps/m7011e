#!/bin/bash

namespace="minio"
helm uninstall minio -n ${namespace}
