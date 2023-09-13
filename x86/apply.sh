#!/bin/bash
export KUBECONFIG=kubeconfig
oc apply -f deployment.yaml --insecure-skip-tls-verify=true
oc apply -f svc.yaml --insecure-skip-tls-verify=true

