moved {
  from = aws_api_gateway_base_path_mapping.mapping
  to   = module.region["eu-west-1"].aws_api_gateway_base_path_mapping.mapping
}

moved {
  from = aws_acm_certificate.environment_cert[0]
  to   = module.region["eu-west-1"].aws_acm_certificate.environment_cert[0]
}

moved {
  from = aws_route53_record.validation[0]
  to   = module.region["eu-west-1"].aws_route53_record.validation[0]
}

moved {
  from = aws_api_gateway_domain_name.lpa_data
  to   = module.region["eu-west-1"].aws_api_gateway_domain_name.lpa_data
}

moved {
  from = aws_api_gateway_method_settings.global_gateway_settings
  to   = module.region["eu-west-1"].aws_api_gateway_method_settings.global_gateway_settings
}

moved {
  from = aws_api_gateway_rest_api.lpa
  to   = module.region["eu-west-1"].aws_api_gateway_rest_api.lpa
}

moved {
  from = aws_route53_record.environment_record
  to   = module.region["eu-west-1"].aws_route53_record.environment_record
}

moved {
  from = module.deploy_v1.aws_api_gateway_deployment.deploy
  to   = module.region["eu-west-1"].aws_api_gateway_deployment.deploy
}

moved {
  from = module.deploy_v1.aws_api_gateway_stage.currentstage
  to   = module.region["eu-west-1"].aws_api_gateway_stage.current
}

moved {
  from = module.deploy_v1.aws_cloudwatch_log_group.lpa_data
  to   = module.region["eu-west-1"].aws_cloudwatch_log_group.lpa_data
}

moved {
  from = module.deploy_v1.aws_wafv2_web_acl_association.api_gateway_stage
  to   = module.region["eu-west-1"].aws_wafv2_web_acl_association.api_gateway_stage
}

moved {
  from = aws_cloudwatch_metric_alarm.rest_api_5xx_errors
  to   = module.region["eu-west-1"].aws_cloudwatch_metric_alarm.rest_api_5xx_errors
}

moved {
  from = aws_cloudwatch_metric_alarm.rest_api_high_count
  to   = module.region["eu-west-1"].aws_cloudwatch_metric_alarm.rest_api_high_count
}

moved {
  from = aws_cloudwatch_metric_alarm.rest_api_slow_response[0]
  to   = module.region["eu-west-1"].aws_cloudwatch_metric_alarm.rest_api_slow_response[0]
}
