provider "aws" {}

variable "lambda_layer_arn" {
  type = string
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "movie_scheduler_lambda_execution_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy" "lambda_basic_execution_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = data.aws_iam_policy.lambda_basic_execution_policy.arn
  role = aws_iam_role.lambda_execution_role.name
}

resource "aws_lambda_function" "movie_scheduler_example_function" {
  function_name = "MovieSchedulerExample"
  handler = "lambda_example.lambda_handler"
  filename = "lambda_example.zip"
  role = aws_iam_role.lambda_execution_role.arn
  runtime = "python3.7"
  layers = [var.lambda_layer_arn]
  memory_size = 3008
  timeout = 180
}