# VPC - Networking

A VPC (Virtual Private Cloud) is your own private network inside AWS. Every EC2 instance and RDS database I launched ended up inside one, so I wanted to understand how the parts connect.

## What is VPC?

A VPC is an isolated network in one AWS region. You choose its IP range, split it into subnets, and control how traffic goes in and out.

- Each region has a default VPC so you can launch things right away.
- For real projects it is better to create your own VPC with a clear layout.
- A VPC spans all Availability Zones in the region, but each subnet lives in one AZ.

## CIDR

CIDR is how the IP range is written, like `10.0.0.0/16`. The number after `/` is how many bits are fixed for the network. The rest are for hosts.

- `/16` = 65,536 addresses
- `/24` = 256 addresses
- VPC size can be from `/16` (largest) to `/28` (smallest).
- AWS reserves 5 IPs in every subnet (first 4 and the last one), so a `/24` gives 251 usable IPs.

Example split of `10.0.0.0/16` into `/24` subnets:

| Subnet | CIDR | AZ | Type |
|---|---|---|---|
| public-a | 10.0.1.0/24 | ap-south-1a | Public |
| public-b | 10.0.2.0/24 | ap-south-1b | Public |
| private-a | 10.0.11.0/24 | ap-south-1a | Private |
| private-b | 10.0.12.0/24 | ap-south-1b | Private |

I left gaps (1-2 for public, 11-12 for private) so more subnets can be added later without things getting mixed up.

## Subnets

A subnet is a smaller range inside the VPC, placed in one AZ. Resources like EC2 are launched into a subnet.

```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-0abc123 --cidr-block 10.0.1.0/24 --availability-zone ap-south-1a
```

Using at least two AZs is normal, so if one AZ goes down the app still runs.

## Route tables

A route table decides where traffic from a subnet goes.

- Every route table has a `local` route for the VPC CIDR, so all subnets can talk to each other.
- Each subnet is linked to one route table.

Public route table:

| Destination | Target |
|---|---|
| 10.0.0.0/16 | local |
| 0.0.0.0/0 | igw-xxxx |

Private route table:

| Destination | Target |
|---|---|
| 10.0.0.0/16 | local |
| 0.0.0.0/0 | nat-xxxx |

## Internet Gateway

An Internet Gateway (IGW) connects the VPC to the internet.

- One IGW per VPC.
- It is free.
- A subnet is only "public" if its route table sends `0.0.0.0/0` to the IGW and instances have a public IP.

## NAT Gateway

A NAT Gateway lets instances in a private subnet go out to the internet (for example `apt update` or pulling Docker images), but nothing from the internet can start a connection to them.

- It is placed in a public subnet and needs an Elastic IP.
- It costs money every hour it exists, plus per GB of data processed. I deleted mine after the lab because of this.
- It works in one AZ. For high availability you put one in each AZ.

## Security Groups

Security groups work at the instance (network interface) level. They are stateful and only have allow rules. A security group can use another security group as the source, for example "allow port 3306 only from the web-server SG".

## Network ACLs

Network ACLs work at the subnet level. They are stateless, so return traffic must be allowed separately (usually ephemeral ports 1024-65535).

| | Security Group | Network ACL |
|---|---|---|
| Level | Instance / ENI | Subnet |
| State | Stateful | Stateless |
| Rules | Allow only | Allow and Deny |
| Rule order | All rules checked | Lowest number first, stops at first match |
| Default | Inbound blocked, outbound allowed | Default NACL allows all |

I mostly use security groups. NACLs are useful for blocking a specific IP range for a whole subnet.

## Public vs private subnet

| | Public subnet | Private subnet |
|---|---|---|
| Route to 0.0.0.0/0 | Internet Gateway | NAT Gateway (or none) |
| Reachable from internet | Yes, if instance has public IP | No |
| Typical resources | Load balancer, bastion host, NAT Gateway | App servers, databases |

The usual setup I saw: load balancer in public subnets, app servers and databases in private subnets. Users only reach the load balancer, and the database is never exposed directly.
