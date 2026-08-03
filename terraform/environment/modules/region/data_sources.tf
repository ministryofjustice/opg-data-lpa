data "aws_availability_zones" "available" {
  region = var.region
}

data "aws_caller_identity" "current" {}

data "aws_ecr_image" "data_lpa_lambda_image" {
  repository_name = data.aws_ecr_repository.data_lpa_lambda_image.name
  image_tag       = var.lambda_image_tag
  provider        = aws.management
  region          = var.region
}

data "aws_ecr_repository" "data_lpa_lambda_image" {
  name     = "integrations/lpa-data-lambda"
  provider = aws.management
  region   = var.region
}

data "aws_kms_key" "secrets_manager" {
  key_id = "alias/secrets-manager-regional-kms-key"
  region = var.region
}

data "aws_region" "current" {
  region = var.region
}

data "aws_secretsmanager_secret" "jwt_secret_key" {
  name   = "${var.environment.account_name}/jwt-key"
  region = var.region
}

data "aws_security_group" "lambda_sirius_api_ingress" {
  filter {
    name   = "tag:Name"
    values = ["integration-lambda-api-access-${var.sirius_environment}"]
  }
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
    values = ["Sirius-${var.environment.account_name}-vpc"]
  }
  region = var.region
}
