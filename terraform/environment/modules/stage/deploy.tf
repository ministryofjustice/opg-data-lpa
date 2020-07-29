locals {
  openapi_sha               = substr(replace(base64sha256(data.local_file.openapispec.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
  lambda_version_folder_sha = substr(replace(base64sha256(data.local_file.lambda_version_folder_sha.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
  //Modify here for new version - uncomment below and modify accordingly
  //  openapi_sha               = var.openapi_version == "v1" ? "fixed_variable" : substr(replace(base64sha256(data.local_file.openapispec.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
  //  lambda_version_folder_sha = var.openapi_version == "v1" ? "fixed_variable" : substr(replace(base64sha256(data.local_file.lambda_version_folder_sha.content_base64), "/[^0-9A-Za-z_]/", ""), 0, 5)
}

data "local_file" "openapispec" {
  filename = "../../lambda_functions/${var.openapi_version}/openapi/${var.api_name}-openapi.yml"
}

data "local_file" "lambda_version_folder_sha" {
  filename = "../../lambda_functions/${var.openapi_version}/directory_sha"
}

resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = var.rest_api.id
  depends_on  = [var.domain_name]
  variables = {
    // Force a deploy only when content has changed
    stage_version      = var.openapi_version
    content_api_sha    = local.openapi_sha
    lambda_version_sha = var.template_lambda.source_code_hash
  }
  lifecycle {
    create_before_destroy = true
  }
}
