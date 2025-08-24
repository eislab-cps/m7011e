#!/bin/bash

namespace="helloworld"
helm install ${namespace} -f values.yaml -n ${namespace} .
