# S3: Storage Service

## What Is S3?

Amazon Simple Storage Service (S3) is an object storage service. It stores data as objects inside buckets. Each object contains the data, metadata, and a key that identifies its location in the bucket.

## Key Concepts

- **Bucket:** A container for objects with a globally unique name.
- **Object:** A file and its metadata stored in a bucket.
- **Key:** The object name, including any prefix that looks like a folder path.
- **Storage class:** A pricing and availability option such as Standard, Intelligent-Tiering, or Glacier.
- **Versioning:** Keeps previous versions of objects so accidental changes or deletions can be recovered.
- **Bucket policy:** A resource-based policy controlling access to bucket resources.

## Common Use Cases

- Storing images, videos, documents, and backups
- Hosting static websites
- Collecting application logs and data-lake files
- Sharing build artifacts between CI/CD stages

## Important Lessons

S3 buckets are private by default, but access can be granted through IAM policies, bucket policies, or presigned URLs. Enable versioning for important data and lifecycle rules for automatic archival or deletion. Never make a bucket public unless the use case and security review explicitly require it.

## Reflection

- What is the difference between an object key and a local file path?
- Which storage class would suit rarely accessed backups?
- How would you share one private object temporarily with another person?
