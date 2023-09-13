#!/bin/bash
export KUBECONFIG=kubeconfig
oc delete -f deployment.yaml --insecure-skip-tls-verify=true
oc delete -f svc.yaml --insecure-skip-tls-verify=true

