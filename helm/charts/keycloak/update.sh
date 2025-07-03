#!/bin/bash

namespace="keycloak"
helm upgrade keycloak -f values.yaml -n ${namespace} --wait .
