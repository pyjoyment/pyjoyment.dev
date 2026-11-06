# The zone of the domain in Cloudflare, whose records point at CloudFront without the proxy of Cloudflare, as the
# distribution is the CDN
data "cloudflare_zone" "site" {
  filter = {
    name = local.domain
  }
}

resource "aws_acm_certificate" "site" {
  domain_name       = local.domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "cloudflare_dns_record" "validation" {
  for_each = {
    for option in aws_acm_certificate.site.domain_validation_options : option.domain_name => option
  }

  zone_id = data.cloudflare_zone.site.zone_id
  name    = trimsuffix(each.value.resource_record_name, ".")
  type    = each.value.resource_record_type
  content = trimsuffix(each.value.resource_record_value, ".")
  ttl     = 1
  proxied = false
  comment = "Validation of the certificate of ACM, ${local.repository}"
}

resource "aws_acm_certificate_validation" "site" {
  certificate_arn         = aws_acm_certificate.site.arn
  validation_record_fqdns = [for record in cloudflare_dns_record.validation : record.name]
}

# A CNAME at the apex, which Cloudflare flattens
resource "cloudflare_dns_record" "site" {
  zone_id = data.cloudflare_zone.site.zone_id
  name    = local.domain
  type    = "CNAME"
  content = aws_cloudfront_distribution.site.domain_name
  ttl     = 1
  proxied = false
  comment = "CloudFront, ${local.repository}"
}
