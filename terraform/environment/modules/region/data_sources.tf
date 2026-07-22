data "aws_kms_key" "secrets_manager" {
  key_id = "alias/secrets-manager-regional-kms-key"
  region = var.region
}

data "aws_region" "current" {
  region = var.region
}

data "aws_secretsmanager_secret" "jwt_secret_key" {
  name   = "${var.account.account_mapping}/jwt-key"
  region = var.region
}

data "aws_subnets" "application" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.sirius.id]
  }

  filter {
    name = "tag:Name"
    values = [
      "application-*",
    ]
  }
  region = var.region
}

data "aws_vpc" "sirius" {
  filter {
    name   = "tag:Name"
    values = ["Sirius-${var.account.account_mapping}-vpc"]
  }
  region = var.region
}

data "aws_security_group" "lambda_sirius_api_ingress" {
  filter {
    name   = "tag:Name"
    values = ["integration-lambda-api-access-${var.target_environment}"]
  }
  region = var.region
}

data "aws_caller_identity" "current" {}
