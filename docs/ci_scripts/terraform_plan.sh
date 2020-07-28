#!/bin/bash

while getopts w: option
do
  case "${option}"
  in
    w) TF_WS=${OPTARG};;
    *) echo "usage: $0 [-d] [-r]" >&2
           exit 1 ;;
  esac
done

cd ~/project/terraform/environment
TF_DIR=".terraform"
if [ -d "${TF_DIR}" ]; then rm -Rf ${TF_DIR}; fi
export TF_WORKSPACE=${TF_WS}
echo ""
echo "=== Running Initialisation ==="
echo ""
terraform init
echo ""
echo "=== Running Plan on ${TF_WS} ==="
echo ""
terraform plan -input=false
