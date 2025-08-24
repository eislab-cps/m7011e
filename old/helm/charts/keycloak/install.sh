#!/bin/bash

namespace="keycloak"
helm install keycloak -f values.yaml -n ${namespace} .
