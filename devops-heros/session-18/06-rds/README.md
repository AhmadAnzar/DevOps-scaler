# RDS: Relational Database Service

## What Is RDS?

Amazon Relational Database Service (RDS) is a managed service for relational database engines such as PostgreSQL, MySQL, MariaDB, Oracle, and SQL Server. AWS manages common operational tasks while the team manages the database schema, queries, and application data.

## Key Concepts

- **DB instance:** The managed database server and its compute capacity.
- **Engine:** The relational database software selected for the instance.
- **Subnet group:** The set of VPC subnets where the database can be placed.
- **Security group:** Controls which clients can connect to the database port.
- **Multi-AZ deployment:** Maintains a standby database in another Availability Zone for failover.
- **Read replica:** Provides a read-only copy to scale read traffic.
- **Automated backups:** Support point-in-time recovery within the configured retention period.

## Common Use Cases

- Applications that need SQL queries and transactions
- Existing applications using PostgreSQL or MySQL
- Systems that require relational constraints and joins
- Production databases that benefit from managed backups and failover

## Important Lessons

Keep RDS in private subnets and allow connections only from approved application security groups. Select Multi-AZ for higher availability and read replicas when read scaling is required. Backups, encryption, monitoring, patching, and storage sizing should be part of the database operating plan.

## DynamoDB and RDS

DynamoDB is a managed NoSQL database designed around access patterns and large-scale low-latency workloads. RDS is a managed relational database designed around SQL, relationships, and transactions. The better choice depends on the application's data model and access requirements.

## Reflection

- When would you choose RDS over DynamoDB?
- Why should an RDS database not be exposed directly to the public internet?
- What problem does a Multi-AZ deployment solve?
