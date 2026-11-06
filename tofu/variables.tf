variable "cloudflare_api_token" {
  description = "A token of the API of Cloudflare with Zone:DNS:Edit and Zone:Read of the zone of the domain, in terraform.tfvars, which git ignores"
  type        = string
  sensitive   = true
}

variable "runtime" {
  description = "The runtime of Python of the function, the one of \"generate lambda-zip --runtime\""
  type        = string
  default     = "python3.15"
}
