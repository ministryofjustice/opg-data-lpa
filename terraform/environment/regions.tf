module "region" {
  source   = "./modules/region"
  for_each = tomap(local.environment.active_regions)

  environment        = local.environment
  environment_name   = local.environment_name
  is_ephemeral       = local.is_ephemeral
  lambda_iam_role    = aws_iam_role.lambda
  lambda_image_tag   = var.lambda_image_tag
  region             = each.key
  region_active      = each.value
  sirius_environment = local.sirius_environment
  providers = {
    aws            = aws
    aws.management = aws.management
  }
}
