output "api_gateway_url" {
  value       = aws_api_gateway_domain_name.lpa_data.domain_name
  description = "The Custom Domain of the API Gateway"
}