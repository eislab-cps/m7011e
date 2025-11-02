#!/bin/bash

namespace="db"

helm uninstall postgresql -n ${namespace}
