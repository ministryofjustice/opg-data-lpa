//===============Related to lpa_api_gateway===================

//This gets attached on the lpa_api_gateway directly (api_rest.tf)
data "aws_iam_policy_document" "resource_policy" {
  statement {
    sid    = "ApiAllowLPAUsers"
    effect = "Allow"

    principals {
      identifiers = local.account.allowed_roles
      type        = "AWS"
    }

    actions = ["execute-api:Invoke"]

    // API Gateway will add all of the rest of the ARN details in for us. Prevents a circular dependency.
    resources = ["execute-api:/*/*/*"]
  }
}

//===============Related to Task Execution Role===================

//This is the role that gets assumed from ECS task with assume_role attached
resource "aws_iam_role" "lpa_data" {
  name               = "lpa-api-gateway-access-${local.environment}"
  assume_role_policy = data.aws_iam_policy_document.cross_account_api.json
}

// Access policy, defining who can assume this role
data "aws_iam_policy_document" "cross_account_api" {
  statement {
    sid = "CrossAccountLPAApiGatewayAccessPolicy"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "AWS"
      identifiers = local.account.allowed_roles
    }
  }
}

//Access policy allowing execute on the particular api gateway endpoint
data "aws_iam_policy_document" "gateway_resource_execution_policy" {
  statement {
    sid = "ApiLPAGatewayAccessPolicy"

    actions = [
      "execute-api:Invoke",
    ]

    resources = [
      "${aws_api_gateway_rest_api.lpa.execution_arn}/*/*/*",
    ]
  }
}

//Name of policies and the attachment
resource "aws_iam_policy" "access_policy" {
  depends_on = [aws_api_gateway_rest_api.lpa]

  name   = "access-policy-lpa-${local.environment}"
  policy = data.aws_iam_policy_document.gateway_resource_execution_policy.json
}

resource "aws_iam_role_policy_attachment" "access_policy_attachment" {
  role       = aws_iam_role.lpa_data.id
  policy_arn = aws_iam_policy.access_policy.arn
}
