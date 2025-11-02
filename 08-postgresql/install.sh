#!/bin/bash

namespace="db"
helm install postgresql -f values.yaml -n ${namespace} .
