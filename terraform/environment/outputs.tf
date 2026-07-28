output "api_gateway_url" {
  value       = module.region["eu-west-1"].api_gateway_url
  description = "The Custom Domain of the API Gateway"
}
