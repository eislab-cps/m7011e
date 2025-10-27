#!/bin/bash

namespace="db"
helm upgrade postgresql -f values.yaml -n ${namespace} --debug --wait .
