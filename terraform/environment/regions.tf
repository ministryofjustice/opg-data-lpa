module "region" {
  source   = "./modules/region"
  for_each = tomap(local.account.active_regions)

  account            = local.account
  environment        = local.environment
  is_ephemeral       = local.is_ephemeral
  lambda_iam_role    = aws_iam_role.lambda
  lambda_image_tag   = var.lambda_image_tag
  region             = each.key
  region_active      = each.value
  target_environment = local.target_environment
  providers = {
    aws            = aws
    aws.management = aws.management
  }
}
