# The index of the public layers of the latest release of Pyjoyment-Lambda-Layers, {layer: {region: arn}}, behind a
# redirection of GitHub, which the provider follows
data "http" "layers" {
  url = "https://github.com/pyjoyment/Pyjoyment-Lambda-Layers/releases/latest/download/layers.json"
}

# The alias of the layer of the latest Pyjoyment of the version of Python of the runtime, as pyjoyment-python3_15
locals {
  pyjoyment_layer = jsondecode(data.http.layers.response_body)["pyjoyment-${replace(var.runtime, ".", "_")}"]["us-east-1"]
}

resource "aws_iam_role" "function" {
  name = local.name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "function" {
  role       = aws_iam_role.function.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "function" {
  name              = "/aws/lambda/${local.name}"
  retention_in_days = 14
}

# The function of site/dist/function.zip of "generate lambda-zip --function-only", on the runtime of Python with the
# public layer of Pyjoyment. The configuration creates it with the first build, and a deployment of the application
# changes its code and its layer without OpenTofu, which ignores them, so that a plan needs no build and does not
# take a deployment back
resource "aws_lambda_function" "site" {
  function_name = local.name
  role          = aws_iam_role.function.arn
  runtime       = var.runtime
  architectures = ["arm64"]
  handler       = "app.handler"
  filename      = "${path.module}/../site/dist/function.zip"
  layers        = [local.pyjoyment_layer]
  memory_size   = 128
  timeout       = 10

  environment {
    variables = {
      PYJO_MODE = "production"
    }
  }

  logging_config {
    log_format = "Text"
    log_group  = aws_cloudwatch_log_group.function.name
  }

  lifecycle {
    ignore_changes = [filename, layers]
  }

  depends_on = [aws_iam_role_policy_attachment.function]
}

# The Function URL takes only the requests that CloudFront signs, with its origin access control, so nobody passes by
# the distribution
resource "aws_lambda_function_url" "site" {
  function_name      = aws_lambda_function.site.function_name
  authorization_type = "AWS_IAM"
}

# Both actions, as a Function URL needs them, for the distribution only
resource "aws_lambda_permission" "cloudfront_url" {
  statement_id           = "AllowCloudFrontFunctionURL"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.site.function_name
  principal              = "cloudfront.amazonaws.com"
  source_arn             = aws_cloudfront_distribution.site.arn
  function_url_auth_type = "AWS_IAM"
}

resource "aws_lambda_permission" "cloudfront_invoke" {
  statement_id             = "AllowCloudFrontInvokeFromFunctionURL"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.site.function_name
  principal                = "cloudfront.amazonaws.com"
  source_arn               = aws_cloudfront_distribution.site.arn
  invoked_via_function_url = true
}
