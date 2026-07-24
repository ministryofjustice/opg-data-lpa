resource "aws_elasticache_replication_group" "lpa_redis" {
  count                       = var.region_active ? 1 : 0
  apply_immediately           = var.account.account_mapping != "production" ? true : false
  at_rest_encryption_enabled  = true
  automatic_failover_enabled  = var.account.elasticache_count == 1 ? false : true
  description                 = "ElastiCache Replication Group for Data LPA ${var.environment}"
  engine                      = "redis"
  engine_version              = "7.1"
  kms_key_id                  = aws_kms_key.elasticache_kms.arn
  maintenance_window          = "fri:05:00-fri:06:00"
  multi_az_enabled            = var.account.elasticache_count == 1 ? false : true
  node_type                   = "cache.t2.small"
  num_cache_clusters          = var.account.elasticache_count
  parameter_group_name        = "default.redis7"
  port                        = 6379
  preferred_cache_cluster_azs = var.account.elasticache_count == 1 ? [data.aws_availability_zones.available.names[0]] : data.aws_availability_zones.available.names
  replication_group_id        = "lpa-${substr(var.environment, 0, 26)}-cache-rg"
  security_group_ids          = [aws_security_group.lpa_redis_sg.id]
  snapshot_retention_limit    = 7
  snapshot_window             = "03:00-04:00"
  subnet_group_name           = "private-redis"
  transit_encryption_enabled  = true
  transit_encryption_mode     = "preferred"
  region                      = var.region
}

resource "aws_security_group" "lpa_redis_sg" {
  name_prefix = "${var.environment}-redis-sg"
  vpc_id      = var.account.vpc_id

  lifecycle {
    create_before_destroy = true
  }

  revoke_rules_on_delete = true

  tags = {
    "Name" = "data-lpa-${var.environment}-redis-sg"
  }
  region = var.region
}

resource "aws_security_group_rule" "elasticache_cluster_egress" {
  type              = "egress"
  protocol          = "tcp"
  from_port         = 6379
  to_port           = 6379
  security_group_id = aws_security_group.lpa_redis_sg.id
  description       = "Data LPA ${var.environment} ElastiCache Cluster Communication Egress"
  self              = true
  region            = var.region
}

resource "aws_security_group_rule" "elasticache_cluster_ingress" {
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 6379
  to_port           = 6379
  security_group_id = aws_security_group.lpa_redis_sg.id
  description       = "Data LPA ${var.environment} ElastiCache Cluster Communication Ingress"
  self              = true
  region            = var.region
}

resource "aws_security_group_rule" "elasticache_ingress_from_lambda" {
  description              = "Allow Data LPA ${var.environment} Lambda to call ElastiCache"
  type                     = "ingress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  security_group_id        = aws_security_group.lpa_redis_sg.id
  source_security_group_id = aws_security_group.lambda.id
  region                   = var.region
}

resource "aws_kms_key" "elasticache_kms" {
  description             = "KMS Key for Data LPA ${var.environment} ElastiCache Cluster Encryption"
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.elasticache_kms_key.json
  deletion_window_in_days = 7
  region                  = var.region
}

resource "aws_kms_alias" "elasticache_kms_alias" {
  name          = "alias/elasticache-lpa-${var.environment}"
  target_key_id = aws_kms_key.elasticache_kms.id
  region        = var.region
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
      values   = ["elasticache.${data.aws_region.current.region}.amazonaws.com", "dax.${data.aws_region.current.region}.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}
