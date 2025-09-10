#!/bin/bash

set -oe pipefail

coverage run --source ${LAMBDA_TASK_ROOT}/lambda_functions/v1/functions/lpa -m pytest ${LAMBDA_TASK_ROOT}/lambda_functions/v1/tests

coverage report
