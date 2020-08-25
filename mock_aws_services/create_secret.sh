#!/bin/bash


printf "creating secret\n"
until $(curl --output /dev/null --silent --head --fail 'http://0.0.0.0:4584/?Action=ListSecrets'); do
    printf '.'
    sleep 1
done
curl --location --request POST 'http://0.0.0.0:4584/?Action=CreateSecret' --header 'Content-Type: application/json' --header 'Content-Type: text/plain' --data-raw '{"Name": "local/jwt-key_docker", "Description": "Secret for local testing with Docker","SecretString":"this_is_a_secret_string","ClientRequestToken": "EXAMPLE1-90ab-cdef-fedc-ba987SECRET1"}'
printf "\nsecret created\n"
