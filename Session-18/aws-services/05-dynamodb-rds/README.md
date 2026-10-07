# DynamoDB & RDS - Database Services

AWS has two main managed database options that I looked at: DynamoDB for NoSQL and RDS for normal relational databases. Both are managed, so AWS handles the servers and patching.

## DynamoDB

### NoSQL

DynamoDB is a fully managed NoSQL key-value and document database. There is no server to manage and no fixed schema except the key.

- Very fast, single-digit millisecond reads and writes at almost any scale.
- No joins. You design the table around how you will query it.
- Two capacity modes: **on-demand** (pay per request) and **provisioned** (set read/write capacity, can auto scale).

### Tables

A table is a collection of items. You only define the primary key when creating it. Other fields can be different for each item.

### Items

An item is one record in the table, like a row. Max item size is 400 KB.

### Attributes

Attributes are the fields inside an item, like `status` or `total`. Types include string, number, boolean, list, map and set. Two items in the same table can have different attributes.

### Partition key

The partition key decides which partition stores the item. If a table only has a partition key, it must be unique for each item. A good partition key has many different values so load spreads out evenly.

### Sort key

The sort key is optional. With partition key + sort key, the combination must be unique, and items with the same partition key are stored sorted by the sort key. This lets you do range queries.

Example: `Orders` table with `customer_id` as partition key and `order_date` as sort key.

| customer_id (PK) | order_date (SK) | total | status |
|---|---|---|---|
| C101 | 2026-09-02 | 45.00 | shipped |
| C101 | 2026-10-01 | 120.50 | pending |
| C205 | 2026-09-15 | 18.99 | delivered |

```bash
aws dynamodb create-table --table-name Orders \
  --attribute-definitions AttributeName=customer_id,AttributeType=S AttributeName=order_date,AttributeType=S \
  --key-schema AttributeName=customer_id,KeyType=HASH AttributeName=order_date,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

aws dynamodb query --table-name Orders \
  --key-condition-expression "customer_id = :c AND order_date >= :d" \
  --expression-attribute-values '{":c":{"S":"C101"},":d":{"S":"2026-09-01"}}'
```

The query returns all orders for customer C101 from September 2026 onwards. If I want to search by something else, like `status`, I need a Global Secondary Index.

### Use cases (DynamoDB)

- Shopping carts and user sessions.
- Gaming leaderboards and player data.
- IoT and event data with lots of writes.
- Serverless apps with Lambda.
- Terraform state locking (older setups; newer Terraform can lock with S3 directly).

## RDS

### Relational database

RDS (Relational Database Service) runs SQL databases for you. You get tables, schemas, joins and transactions like a normal database, but AWS handles setup, patching, backups and failover.

### Supported engines

- MySQL
- PostgreSQL
- MariaDB
- Oracle
- Microsoft SQL Server
- IBM Db2
- Amazon Aurora (MySQL and PostgreSQL compatible, AWS's own engine)

### DB instances

A DB instance is the database server. You pick an instance class (like `db.t4g.micro`), storage type (`gp3` or `io2`) and size. You cannot SSH into it. You connect using the endpoint and port, e.g. 3306 for MySQL, 5432 for PostgreSQL.

```bash
aws rds create-db-instance --db-instance-identifier app-db \
  --engine postgres --db-instance-class db.t4g.micro \
  --allocated-storage 20 --master-username dbadmin \
  --manage-master-user-password --no-publicly-accessible
```

`--manage-master-user-password` stores the password in Secrets Manager so it is not typed in the command.

### Security

- Put the DB in private subnets and keep "publicly accessible" off.
- Use a security group that only allows the DB port from the app servers' security group.
- Encryption at rest with KMS (must be chosen at creation time).
- Use SSL/TLS for connections.
- IAM database authentication is supported for MySQL, MariaDB and PostgreSQL.

### Backups

- **Automated backups** - daily snapshot plus transaction logs, kept 1-35 days. Lets you do point-in-time restore.
- **Manual snapshots** - kept until you delete them.
- Restoring always creates a new DB instance.

### Multi-AZ

Multi-AZ keeps a standby copy in another AZ with synchronous replication. If the primary fails, RDS fails over to the standby automatically and the endpoint stays the same. The standby is for availability, not for reading. (The newer Multi-AZ DB cluster option has two readable standbys.)

### Read replicas

Read replicas are copies that use asynchronous replication. They are used to spread out read traffic.

- Each replica has its own endpoint, and the app must send reads there.
- Can be in the same region or another region.
- A replica can be promoted to a standalone DB.

| | Multi-AZ | Read replica |
|---|---|---|
| Purpose | High availability | Read scaling |
| Replication | Synchronous | Asynchronous |
| Can serve reads | No (classic Multi-AZ) | Yes |

### Use cases (RDS)

- Web apps with users, orders, payments.
- ERP and CRM systems.
- Any app that needs joins, transactions and a fixed schema.
- Moving an existing on-prem MySQL/PostgreSQL/Oracle database to AWS.

## DynamoDB vs RDS, when I'd pick which

| | DynamoDB | RDS |
|---|---|---|
| Type | NoSQL key-value | Relational SQL |
| Schema | Flexible | Fixed |
| Joins | No | Yes |
| Scaling | Automatic, horizontal | Bigger instance or read replicas |
| Server to manage | None | Pick instance size |

I would pick DynamoDB when I know my access patterns, need very high scale, or am building a serverless app with Lambda. I would pick RDS when the data has relations (customers, orders, products), I need complex queries or reports, or the app already uses SQL.
