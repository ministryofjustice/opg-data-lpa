resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = aws_api_gateway_rest_api.lpa.id
  depends_on  = [aws_api_gateway_domain_name.lpa_data]
  triggers = {
    redeployment_open_api_spec = local.open_api_spec_sha
    redeployment_api_policy    = local.api_gateway_policy_sha
    lambda_function            = aws_lambda_function.data_lpa.function_name
  }
  lifecycle {
    create_before_destroy = true
  }
}
