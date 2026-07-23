module "region" {
  source   = "./modules/region"
  for_each = tomap(local.account.active_regions)

  account            = local.account
  environment        = local.environment
  lambda_iam_role    = aws_iam_role.lambda
  lambda_image_tag   = var.lambda_image_tag
  region             = each.key
  target_environment = local.target_environment
  tmp_execution_arn  = aws_api_gateway_rest_api.lpa.execution_arn
  tmp_redis_endpoint = aws_elasticache_replication_group.lpa_redis.primary_endpoint_address
  tmp_redis_sg_id    = aws_security_group.lpa_redis_sg.id
}
