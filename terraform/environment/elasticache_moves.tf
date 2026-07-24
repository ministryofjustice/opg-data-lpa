moved {
  from = aws_elasticache_replication_group.lpa_redis
  to   = module.region["eu-west-1"].aws_elasticache_replication_group.lpa_redis[0]
}

moved {
  from = aws_kms_alias.elasticache_kms_alias
  to   = module.region["eu-west-1"].aws_kms_alias.elasticache_kms_alias
}

moved {
  from = aws_kms_key.elasticache_kms
  to   = module.region["eu-west-1"].aws_kms_key.elasticache_kms
}

moved {
  from = aws_security_group.lpa_redis_sg
  to   = module.region["eu-west-1"].aws_security_group.lpa_redis_sg
}

moved {
  from = aws_security_group_rule.elasticache_ingress_from_lambda
  to   = module.region["eu-west-1"].aws_security_group_rule.elasticache_ingress_from_lambda
}

moved {
  from = aws_security_group_rule.lpa_redis_rules["cache_in"]
  to   = module.region["eu-west-1"].aws_security_group_rule.elasticache_cluster_ingress
}

moved {
  from = aws_security_group_rule.lpa_redis_rules["cache_out"]
  to   = module.region["eu-west-1"].aws_security_group_rule.elasticache_cluster_egress
}
