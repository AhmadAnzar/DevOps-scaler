# EC2 - Compute

EC2 (Elastic Compute Cloud) gives you virtual servers in AWS. It is the service I have used the most so far, mostly to run Docker and small web apps.

## What is EC2?

EC2 lets you rent a virtual machine (called an instance) and pay for the time it runs. You pick the OS, CPU, RAM, disk and network settings, and you can start or stop it whenever you want.

Pricing options I noted:

- **On-Demand** - pay per second, no commitment.
- **Reserved Instances / Savings Plans** - commit for 1 or 3 years, cheaper.
- **Spot** - spare capacity at a big discount, but AWS can take it back with a 2 minute warning.

## AMI

An AMI (Amazon Machine Image) is the template used to launch an instance. It includes the OS and any software already installed.

- AWS provides AMIs like Amazon Linux 2023, Ubuntu, Windows Server.
- You can make your own AMI from a configured instance and launch copies of it.
- AMIs are regional. To use one in another region you copy it.

## Instance types

The instance type decides how much CPU, memory and network you get. The name is like `t3.micro`: family `t`, generation `3`, size `micro`.

| Family | Optimized for | Example |
|---|---|---|
| T | Burstable, general use | `t3.micro`, `t4g.small` |
| M | General purpose, balanced | `m7i.large` |
| C | Compute (CPU heavy) | `c7g.xlarge` |
| R | Memory heavy | `r7i.large` |
| I | Storage / fast local disk | `i4i.large` |
| G / P | GPU workloads | `g5.xlarge` |

A `g` after the generation number (like `t4g`) means it runs on AWS Graviton (ARM) CPUs, which are usually cheaper.

## Key pairs

A key pair is used to SSH into a Linux instance. AWS keeps the public key and you download the private key (`.pem`) once.

```bash
aws ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text > my-key.pem
chmod 400 my-key.pem
ssh -i my-key.pem ec2-user@<public-ip>
```

If you lose the `.pem` file you cannot download it again. Default user is `ec2-user` on Amazon Linux and `ubuntu` on Ubuntu. EC2 Instance Connect and SSM Session Manager are other ways to log in without managing keys.

## Security Groups

A security group is a virtual firewall attached to the instance.

- Only allow rules, no deny rules.
- Stateful: if inbound traffic is allowed, the reply goes out automatically.
- By default all inbound is blocked and all outbound is allowed.

Rules I used for a simple web server:

| Type | Port | Source |
|---|---|---|
| SSH | 22 | My IP only (`x.x.x.x/32`) |
| HTTP | 80 | `0.0.0.0/0` |
| HTTPS | 443 | `0.0.0.0/0` |

Opening port 22 to `0.0.0.0/0` is a common mistake.

## EBS

EBS (Elastic Block Store) is the disk attached to the instance.

- It stays even if you stop the instance.
- It lives in one Availability Zone, same as the instance.
- Types: `gp3` (general SSD, default choice), `io2` (high IOPS), `st1`/`sc1` (HDD).
- Snapshots back up a volume to S3 and can be used to create new volumes.
- By default the root volume is deleted when the instance is terminated.

## Public vs private IP

| | Private IP | Public IP |
|---|---|---|
| Reachable from | Inside the VPC | The internet |
| Changes on stop/start | No | Yes |
| Cost | Free | Charged (AWS bills public IPv4 hourly since Feb 2024) |

If you need a public IP that does not change, use an Elastic IP.

## Instance lifecycle

- **pending** - starting up.
- **running** - on, and you are billed.
- **stopping / stopped** - off. No compute charge, but EBS storage is still billed.
- **rebooting** - restart, keeps the same IPs.
- **shutting-down / terminated** - deleted, cannot be brought back.

Stop and start can move the instance to a different host, and the public IP changes. Termination protection can be turned on to avoid deleting by accident.

```bash
aws ec2 stop-instances --instance-ids i-0abc123def4567890
aws ec2 start-instances --instance-ids i-0abc123def4567890
```

## Common use cases

- Hosting web apps and APIs.
- Running Docker containers or a self-managed Kubernetes cluster.
- Jenkins or other CI build servers.
- Bastion host to reach private servers.
- Batch jobs on Spot instances to save money.
