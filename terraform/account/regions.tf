locals {
  regions = [
    "eu-west-1",
    "eu-west-2"
  ]
}

module "region" {
  source   = "./modules/region"
  for_each = toset(local.regions)

  account = local.account
  region  = each.value
  providers = {
    aws            = aws
    aws.management = aws.management
  }
}
