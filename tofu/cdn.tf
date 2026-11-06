resource "aws_cloudfront_origin_access_control" "site" {
  name                              = local.name
  origin_access_control_origin_type = "lambda"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# The application says what is cached with Cache-Control, as the files of public/ do, and a response without it is
# not cached; the query is in the key, the cookies and the headers are not
resource "aws_cloudfront_cache_policy" "site" {
  name        = local.name
  default_ttl = 0
  min_ttl     = 0
  max_ttl     = 31536000

  parameters_in_cache_key_and_forwarded_to_origin {
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true

    cookies_config {
      cookie_behavior = "none"
    }

    headers_config {
      header_behavior = "none"
    }

    query_strings_config {
      query_string_behavior = "all"
    }
  }
}

# Everything of the request but the Host header, as the Function URL takes the requests of its own host only
data "aws_cloudfront_origin_request_policy" "all_viewer_except_host" {
  name = "Managed-AllViewerExceptHostHeader"
}

resource "aws_cloudfront_distribution" "site" {
  enabled         = true
  comment         = local.domain
  aliases         = [local.domain]
  is_ipv6_enabled = true
  http_version    = "http2and3"
  price_class     = "PriceClass_100"

  origin {
    origin_id                = "function"
    domain_name              = split("/", aws_lambda_function_url.site.function_url)[2]
    origin_access_control_id = aws_cloudfront_origin_access_control.site.id

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # Without the methods with a body: the origin access control of a Function URL takes them only with the SHA-256 of
  # the body in x-amz-content-sha256, which the client computes, and the distribution rejects them before the function
  default_cache_behavior {
    target_origin_id         = "function"
    viewer_protocol_policy   = "redirect-to-https"
    allowed_methods          = ["GET", "HEAD", "OPTIONS"]
    cached_methods           = ["GET", "HEAD"]
    compress                 = true
    cache_policy_id          = aws_cloudfront_cache_policy.site.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_viewer_except_host.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.site.certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
