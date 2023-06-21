#!/bin/bash

set -o pipefail

coverage run --source /lpa_data/lambda_functions/v1/functions/lpa/app/api -m pytest /lpa_data/lambda_functions/v1/tests/

coverage report
