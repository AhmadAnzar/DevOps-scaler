# ---------- Networking ----------

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = "session19-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = { Name = "session19-public-subnet" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "session19-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # send all internet traffic through the internet gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = { Name = "session19-public-rt" }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ---------- Security Group ----------

resource "aws_security_group" "web" {
  name        = "session19-web-sg"
  description = "Allow HTTP in, everything out"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "session19-web-sg" }
}

# ---------- EC2 ----------

# latest Amazon Linux 2023 image, so I don't hardcode an AMI id per region
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-x86_64"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]

  # installs nginx on first boot and writes a simple page
  user_data = <<-EOF
    #!/bin/bash
    dnf install -y nginx
    echo "<h1>Session 19 - deployed with Terraform</h1><p>Instance: $(hostname)</p>" > /usr/share/nginx/html/index.html
    systemctl enable --now nginx
  EOF

  # explicit dependency: the instance needs the internet route to exist
  # before boot, otherwise dnf install in user_data has no internet
  depends_on = [aws_route_table_association.public]

  tags = { Name = "session19-web" }
}

# ---------- S3 ----------

resource "aws_s3_bucket" "assets" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = { Name = var.bucket_name }
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket = aws_s3_bucket.assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
