# Assumed by the jobs of the environment production of the repository only, with the OIDC provider of GitHub of the
# account, which Pyjoyment-Lambda-Layers manages, as an account has one provider of a URL
data "aws_iam_policy_document" "deploy_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${local.account_id}:oidc-provider/token.actions.githubusercontent.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["${local.subject}:environment:production"]
    }
  }
}

resource "aws_iam_role" "deploy" {
  name               = "${local.name}-deploy"
  assume_role_policy = data.aws_iam_policy_document.deploy_trust.json
}

data "aws_iam_policy_document" "deploy" {
  # The code and the layers of the function, which OpenTofu ignores
  statement {
    actions = [
      "lambda:GetFunctionConfiguration",
      "lambda:UpdateFunctionCode",
      "lambda:UpdateFunctionConfiguration",
    ]
    resources = ["arn:aws:lambda:us-east-1:${local.account_id}:function:${local.name}"]
  }

  # The layers of Pyjoyment of Pyjoyment-Lambda-Layers, of the same account, which a function takes with this
  statement {
    actions   = ["lambda:GetLayerVersion"]
    resources = ["arn:aws:lambda:us-east-1:${local.account_id}:layer:pyjoyment-*"]
  }

  # The distributions of the account, which has this one only, as the ID of the distribution is unknown until it is
  # created
  statement {
    actions   = ["cloudfront:CreateInvalidation", "cloudfront:GetInvalidation"]
    resources = ["arn:aws:cloudfront::${local.account_id}:distribution/*"]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "deploy"
  role   = aws_iam_role.deploy.id
  policy = data.aws_iam_policy_document.deploy.json
}
