resource "aws_iam_role_policy_attachment" "regional_lambda_permissions" {
  role       = var.lambda_iam_role.name
  policy_arn = aws_iam_policy.regional_lambda_permissions.arn
}


resource "aws_iam_policy" "regional_lambda_permissions" {
  name        = "data-lpa-lambda-permissions-${var.environment}-${data.aws_region.current.region}"
  description = "Regional Permissions for Data LPA Lambda"
  policy      = data.aws_iam_policy_document.regional_lambda_permissions.json
}

data "aws_iam_policy_document" "regional_lambda_permissions" {
  statement {
    sid = "AllowJWTSecretRead"

    actions = [
      "secretsmanager:GetSecretValue"
    ]

    resources = [
      data.aws_secretsmanager_secret.jwt_secret_key.arn
    ]
  }
  statement {
    sid = "AllowSecretsManagerKMSDecrypt"

    actions = [
      "kms:Decrypt"
    ]

    resources = [
      data.aws_kms_key.secrets_manager.arn
    ]
  }
}

