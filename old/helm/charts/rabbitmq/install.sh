#!/bin/bash

namespace="rabbit"
helm install ${namespace} -f values.yaml -n ${namespace} .
