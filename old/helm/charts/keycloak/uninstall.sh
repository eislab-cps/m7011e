#!/bin/bash

namespace="keycloak"
helm uninstall keycloak -n ${namespace}
