#!/bin/bash

set -oe pipefail

python -m coverage run --source ${LAMBDA_TASK_ROOT}/lambda_functions/v1/functions/lpa -m pytest ${LAMBDA_TASK_ROOT}/lambda_functions/v1/tests

python -m coverage report
