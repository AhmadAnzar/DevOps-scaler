# EC2: Compute Service

## What Is EC2?

Amazon Elastic Compute Cloud (EC2) provides virtual servers, called instances, in the AWS cloud. An EC2 instance can run applications, websites, scripts, and other workloads without maintaining physical hardware.

## Key Concepts

- **AMI:** A template containing the operating system and software used to launch an instance.
- **Instance type:** Defines the available CPU, memory, networking, and pricing profile.
- **Key pair:** Used to authenticate securely when connecting to an instance.
- **Security group:** A stateful virtual firewall that controls inbound and outbound traffic.
- **EBS volume:** Persistent block storage attached to an instance.
- **Elastic IP:** A static public IPv4 address that can be associated with an instance.

## Common Use Cases

- Hosting a web server or API
- Running background workers and scheduled jobs
- Building and testing applications
- Migrating existing server-based workloads to the cloud

## Important Lessons

Choose an instance type based on workload requirements rather than selecting the largest option. Restrict security-group rules to the required ports and trusted sources. Use IAM roles instead of storing AWS access keys on an instance, and stop or terminate unused resources to control cost.

## Reflection

- What type of application would you run on EC2?
- Which ports would it need, and which sources should be allowed to access them?
- What is the difference between stopping and terminating an instance?
