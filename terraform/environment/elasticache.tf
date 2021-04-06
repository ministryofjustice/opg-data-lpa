data "aws_availability_zones" "available" {
}

resource "aws_elasticache_replication_group" "lpa_redis" {
  automatic_failover_enabled    = local.account.elasticache_count == 1 ? false : true
  engine                        = "redis"
  engine_version                = "5.0.6"
  replication_group_id          = "lpa-data-redis-${local.environment}"
  replication_group_description = "Replication Group for LPA Data"
  node_type                     = "cache.t2.small"
  multi_az_enabled              = local.account.elasticache_count == 1 ? false : true
  availability_zones            = data.aws_availability_zones.available.zone_ids
  number_cache_clusters         = local.account.elasticache_count
  parameter_group_name          = "default.redis5.0"
  port                          = 6379
  subnet_group_name             = "private-redis"
  security_group_ids            = [aws_security_group.lpa_redis_sg.id]
  tags                          = local.default_tags
  apply_immediately             = true

  lifecycle {
    ignore_changes = [number_cache_clusters]
  }
}

resource "aws_security_group" "lpa_redis_sg" {
  name_prefix = "${local.environment}-redis-sg"
  vpc_id      = local.account.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  revoke_rules_on_delete = true

  tags = merge(
    local.default_tags,
    {
      "Name" = "${local.environment}-redis-sg"
    },
  )
}

locals {
  redis_rules = {
    cache_out = {
      port        = 6379
      type        = "egress"
      protocol    = "tcp"
      target_type = "self"
      target      = true
    }
    cache_in = {
      port        = 6379
      type        = "ingress"
      protocol    = "tcp"
      target_type = "self"
      target      = true
    }
  }
}

resource "aws_security_group_rule" "lpa_redis_rules" {
  for_each = local.redis_rules

  type                     = each.value.type
  protocol                 = each.value.protocol
  from_port                = each.value.port
  to_port                  = each.value.port
  security_group_id        = aws_security_group.lpa_redis_sg.id
  source_security_group_id = each.value.target_type == "security_group_id" ? each.value.target : null
  prefix_list_ids          = each.value.target_type == "prefix_list_id" ? [each.value.target] : null
  description              = each.key
  cidr_blocks              = each.value.target_type == "cidr_block" ? [each.value.target] : null
  self                     = each.value.target_type == "self" ? each.value.target : null
}
