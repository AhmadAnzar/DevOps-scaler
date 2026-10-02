# DynamoDB: NoSQL Database Service

## What Is DynamoDB?

Amazon DynamoDB is a fully managed NoSQL database that provides fast, predictable performance at scale. It stores records as items in tables and does not require the traditional rows, joins, or fixed relational schema used by SQL databases.

## Key Concepts

- **Table:** A collection of items.
- **Item:** A record stored in a table.
- **Attribute:** A field on an item.
- **Partition key:** Determines where an item is stored and must be designed for an even workload.
- **Sort key:** Optionally organizes related items under the same partition key.
- **Query:** Efficiently reads items using a key.
- **Scan:** Reads every item and is generally more expensive and slower.
- **Capacity mode:** On-demand or provisioned capacity for handling requests.

## Common Use Cases

- Session and shopping-cart data
- User profiles and application metadata
- Serverless applications
- High-volume workloads requiring low-latency access

## Important Lessons

DynamoDB design begins with access patterns. Choose keys that distribute traffic evenly and model data around the queries the application needs. Avoid relying on scans for normal application requests. Use conditional writes, backups, encryption, and point-in-time recovery where appropriate.

## Reflection

- When would DynamoDB be a better choice than a relational database?
- What is the difference between a query and a scan?
- How would you choose a partition key for a large table?
