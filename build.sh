cd $(dirname $BASH_SOURCE)
$(aws-vault exec identity -- go run ./docs/support_scripts/aws/getcreds.go)
docker-compose -f docker-compose.yml build \
--build-arg AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
--build-arg AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
--build-arg AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN
