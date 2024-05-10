data "aws_availability_zones" "available" {
}

resource "aws_elasticache_replication_group" "lpa_redis" {
  automatic_failover_enabled  = local.account.elasticache_count == 1 ? false : true
  engine                      = "redis"
  engine_version              = "5.0.6"
  replication_group_id        = "lpa-${local.redis_c_rg_name}-cache-rg"
  description                 = "Replication Group for LPA Data"
  node_type                   = "cache.t2.small"
  multi_az_enabled            = local.account.elasticache_count == 1 ? false : true
  preferred_cache_cluster_azs = local.account.elasticache_count == 1 ? ["eu-west-1a"] : data.aws_availability_zones.available.names
  num_cache_clusters          = local.account.elasticache_count
  parameter_group_name        = "default.redis5.0"
  port                        = 6379
  subnet_group_name           = "private-redis"
  security_group_ids          = [aws_security_group.lpa_redis_sg.id]
  tags                        = local.default_tags
  apply_immediately           = true
  at_rest_encryption_enabled  = true
  kms_key_id                  = aws_kms_alias.elasticache_kms_alias.target_key_arn
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

resource "aws_kms_key" "elasticache_kms" {
  description             = "KMS Key for elasticache"
  policy                  = data.aws_iam_policy_document.elasticache_kms_key.json
  deletion_window_in_days = 7
}

data "aws_iam_policy_document" "elasticache_kms_key" {
  statement {
    sid       = "Enable IAM User Permissions"
    effect    = "Allow"
    resources = ["*"]
    actions   = ["kms:*"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
  }

  statement {
    sid       = "Allow access for Key Administrators"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
    ]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ci"]
    }
  }

  statement {
    sid       = "Allow Elasticache to use KMS key"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "kms:DescribeKey",
      "kms:GenerateDataKey*",
      "kms:Encrypt",
      "kms:ReEncrypt*",
      "kms:Decrypt"
    ]

    condition {
      test     = "StringEquals"
      variable = "kms:ViaService"
      values   = ["elasticache.region.amazonaws.com", "dax.region.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }
}

resource "aws_kms_alias" "elasticache_kms_alias" {
  name          = "alias/elasticache-lpa"
  target_key_id = aws_kms_key.elasticache_kms.id
}

data "aws_caller_identity" "current" {}
