#!/bin/bash -x

# update is a no-op for now

exec 3>&1 # "save" stdout to fd 3
exec &>> /tmp/create-statefulset.log

function error_exit() {
    echo "{\"Reason\": \"$1\"}" >&3 3>&- # echo reason to stdout (instead of log) and then close fd 3
    exit $2
}


echo "{}" >&3 3>&-  # echo success to stdout (instead of log) and then close fd 3
exit 0
