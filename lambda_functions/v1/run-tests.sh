#!/bin/bash

set -oe pipefail

coverage run --source ${LAMBDA_TASK_ROOT}/lambda_functions/v1/functions/lpa/app/api -m pytest ${LAMBDA_TASK_ROOT}/lambda_functions

coverage report
