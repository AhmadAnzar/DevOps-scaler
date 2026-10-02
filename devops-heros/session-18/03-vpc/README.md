# VPC: Networking Service

## What Is a VPC?

Amazon Virtual Private Cloud (VPC) is a logically isolated network in AWS. It lets you define IP address ranges, subnets, routing, and network access controls for cloud resources.

## Key Concepts

- **CIDR block:** The IP address range assigned to the VPC, such as `10.0.0.0/16`.
- **Subnet:** A smaller IP range inside a VPC, associated with one Availability Zone.
- **Public subnet:** Has a route to an internet gateway.
- **Private subnet:** Does not accept direct inbound internet traffic; it may use a NAT gateway for outbound access.
- **Route table:** Determines where network traffic is sent.
- **Internet gateway:** Connects a VPC to the public internet.
- **Security group and network ACL:** Control traffic at the instance and subnet boundaries.

## Common Design

A typical application places public load balancers in public subnets and application servers and databases in private subnets. Multiple Availability Zones improve availability. The network should expose only the components that must be reachable from the internet.

## Important Lessons

Plan CIDR ranges before creating resources so networks can be expanded or connected later. A resource in a public subnet is not automatically reachable unless its route table, security group, and service configuration permit the traffic. Keep databases in private subnets and allow access only from the application layer.

## Reflection

- What makes a subnet public?
- Why should a database usually be placed in a private subnet?
- What is the difference between a security group and a network ACL?
