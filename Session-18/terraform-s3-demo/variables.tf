variable "region" {
  description = "AWS region to create the bucket in"
  type        = string
  default     = "ap-northeast-2"
}

variable "bucket_name" {
  description = "Name of the S3 bucket, has to be unique across all of AWS"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}
