#! /usr/bin/env bash
awslocal secretsmanager create-secret --name local/jwt-key \
    --description "Secret for local testing with Docker" \
    --secret-string "this_is_a_secret_string"
