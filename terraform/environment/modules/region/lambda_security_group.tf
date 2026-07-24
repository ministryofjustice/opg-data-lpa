resource "aws_security_group" "lambda" {
  name        = "data-lpa-${var.environment}"
  vpc_id      = data.aws_vpc.sirius.id
  description = "Data LPA Lambda ${var.environment} Security Group"
  region      = var.region
}


resource "aws_security_group_rule" "lambda_egress_elasticache" {
  description              = "Allow Lambda to reach connect to ElastiCache"
  type                     = "egress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  security_group_id        = aws_security_group.lambda.id
  source_security_group_id = aws_security_group.lpa_redis_sg.id
  region                   = var.region
}
