# Terraform and AWS Services

Name: Anzar
Enrollment Number: 24BCS10289

```text
Session-18/
├── terraform-s3-demo/      Task 1: S3 bucket with Terraform
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── terraform.tfvars
│   └── README.md
├── aws-services/           Task 2: notes on each AWS service
│   ├── 01-iam/README.md
│   ├── 02-ec2/README.md
│   ├── 03-s3/README.md
│   ├── 04-vpc/README.md
│   └── 05-dynamodb-rds/README.md
└── images/
```

## Task 1: Terraform S3 demo

Full walkthrough with screenshots is in
[terraform-s3-demo/README.md](terraform-s3-demo/README.md). In short:

```text
terraform init -> fmt -> validate -> plan -> apply -> show -> output -> destroy
```

It creates one S3 bucket with versioning, encryption and public access
blocked, puts a test file in it, prints the outputs, and then destroys
everything.

## Task 2: AWS services

| Service | Category | Notes |
|---|---|---|
| IAM | Governance | [01-iam](aws-services/01-iam/README.md) |
| EC2 | Compute | [02-ec2](aws-services/02-ec2/README.md) |
| S3 | Storage | [03-s3](aws-services/03-s3/README.md) |
| VPC | Networking | [04-vpc](aws-services/04-vpc/README.md) |
| DynamoDB and RDS | Databases | [05-dynamodb-rds](aws-services/05-dynamodb-rds/README.md) |

## What is Terraform

Terraform is Infrastructure as Code. Instead of clicking around the AWS
console, I write what I want in `.tf` files and Terraform creates it.
It keeps a state file so it knows what already exists, which is why `plan`
can show the exact difference before anything changes. The same files can
be run again to get the same setup, and they can be reviewed in git like
normal code.
