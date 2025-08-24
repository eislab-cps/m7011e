#!/bin/bash

namespace="rabbit"
helm uninstall rabbit -n ${namespace}
