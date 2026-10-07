resource "aws_s3_bucket" "demo" {
  bucket = var.bucket_name

  # lets terraform destroy delete the bucket even if it has files in it
  force_destroy = true

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    Session     = "18"
  }
}

# keep old versions of files when they are overwritten or deleted
resource "aws_s3_bucket_versioning" "demo" {
  bucket = aws_s3_bucket.demo.id

  versioning_configuration {
    status = "Enabled"
  }
}

# encrypt everything stored in the bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "demo" {
  bucket = aws_s3_bucket.demo.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# nothing in this bucket should ever be public
resource "aws_s3_bucket_public_access_block" "demo" {
  bucket = aws_s3_bucket.demo.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# a small test file so the bucket isn't empty
resource "aws_s3_object" "hello" {
  bucket       = aws_s3_bucket.demo.id
  key          = "hello.txt"
  content      = "Hello from Terraform, Session 18"
  content_type = "text/plain"
}
