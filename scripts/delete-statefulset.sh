#!/bin/bash -x

exec 3>&1 # "save" stdout to fd 3
exec &>> /tmp/delete-statefulset.log

function error_exit() {
    echo "{\"Reason\": \"$1\"}" >&3 3>&- # echo reason to stdout (instead of log) and then close fd 3
    exit $2
}

export KUBECONFIG=/home/ubuntu/.kube/config

kubectl delete statefulset -l app=cockroachdb
kubectl delete pvc -l app=cockroachdb
delete_ret=$?

if [ $delete_ret -ne 0 ]
then
    error_exit "Couldn't delete persistent volumes." $delete_ret
else
    echo "{}" >&3 3>&- # echo reason to stdout (instead of log) and then close fd 3
    exit 0
fi
