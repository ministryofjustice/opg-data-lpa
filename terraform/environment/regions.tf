module "region" {
  source   = "./modules/region"
  for_each = tomap(local.account.active_regions)

  account            = local.account
  environment        = local.environment
  lambda_iam_role    = aws_iam_role.lambda
  lambda_image_tag   = var.lambda_image_tag
  region             = each.key
  region_active      = each.value
  target_environment = local.target_environment
  tmp_execution_arn  = aws_api_gateway_rest_api.lpa.execution_arn
}
