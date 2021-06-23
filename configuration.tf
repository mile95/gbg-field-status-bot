variable "AWS_ACCESS_KEY" {
  description = "AWS_ACCESS_KEY"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_KEY" {
  description = "AWS_SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "TWITTER_ACCESS_TOKEN_SECRET" {
  description = "TWITTER_ACCESS_TOKEN_SECRET"
  type        = string
  sensitive   = true
}

variable "TWITTER_ACCESS_TOKEN" {
  description = "TWITTER_ACCESS_TOKEN"
  type        = string
  sensitive   = true
}

variable "TWITTER_CONSUMER_API_KEY" {
  description = "TWITTER_CONSUMER_API_KEY"
  type        = string
  sensitive   = true
}

variable "TWITTER_CONSUMER_API_SECRET" {
  description = "TWITTER_CONSUMER_API_SECRET"
  type        = string
  sensitive   = true
}

provider "aws" {
  region     = "eu-north-1"
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}

resource "aws_lambda_function" "TwitterBot" {
  filename         = "lambda.zip"
  function_name    = "TwitterBot"
  role             = "arn:aws:iam::753907798323:role/terra"
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda.zip")
  runtime          = "python3.8"
  environment {
    variables = {
      ACCESS_TOKEN_SECRET = var.TWITTER_ACCESS_TOKEN_SECRET
      ACCESS_TOKEN        = var.TWITTER_ACCESS_TOKEN
      CONSUMER_API_KEY    = var.TWITTER_CONSUMER_API_KEY
      CONSUMER_API_SECRET = var.TWITTER_CONSUMER_API_SECRET
    }
  }
}

module "lambda-cloudwatch-trigger" {
  source                     = "infrablocks/lambda-cloudwatch-events-trigger/aws"
  region                     = "eu-north-1"
  component                  = "TwitterBot"
  deployment_identifier      = "production"
  lambda_arn                 = aws_lambda_function.TwitterBot.arn
  lambda_function_name       = "TwitterBot"
  lambda_schedule_expression = "cron(0 8,10,13 ? * * *)"
}
