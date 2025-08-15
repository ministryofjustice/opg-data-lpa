locals {
  openapi_sha = substr(replace(base64sha256(data.local_file.openapispec.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
  //Modify here for new version - uncomment below and modify accordingly
  //  openapi_sha               = var.openapi_version == "v1" ? "fixed_variable" : substr(replace(base64sha256(data.local_file.openapispec.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
}

data "local_file" "openapispec" {
  filename = "../../lambda_functions/${var.openapi_version}/openapi/${var.api_name}-openapi.yml"
}

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
