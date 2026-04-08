resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = var.rest_api.id
  depends_on  = [var.domain_name]
  triggers = {
    redeployment_open_api_spec = var.content_api_sha
    redeployment_api_policy    = var.content_api_policy_sha
    lambda_version_folder_sha  = var.lpa_lambda_source_code_hash
  }
  lifecycle {
    create_before_destroy = true
  }
}
