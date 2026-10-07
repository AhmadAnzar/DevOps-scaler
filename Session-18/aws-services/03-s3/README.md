# S3 - Storage

S3 (Simple Storage Service) is AWS object storage. You upload files and get them back through the console, CLI or an HTTP URL.

## What is S3?

S3 stores data as objects inside buckets. It is not a disk you mount like EBS. You read and write whole files through an API.

Things I noted:

- Practically no storage limit. A single object can be up to 5 TB.
- Designed for 99.999999999% (11 nines) durability.
- You pay for storage used, requests and data transfer out.

## Buckets

A bucket is a container for objects.

- Bucket names are globally unique across all AWS accounts.
- Names must be lowercase, 3-63 characters, no underscores.
- A bucket is created in one region.
- New buckets have Block Public Access turned on by default.

```bash
aws s3 mb s3://anzar-devops-notes-2026 --region ap-south-1
aws s3 ls
```

## Objects

An object is the file plus its metadata. Each object has a key, which is the full path name.

- Example key: `logs/2026/10/app.log`.
- There are no real folders. The `/` in the key just makes it look like folders in the console.

```bash
aws s3 cp notes.txt s3://anzar-devops-notes-2026/docs/notes.txt
aws s3 sync ./site s3://anzar-devops-notes-2026/site/
```

## Storage classes

| Class | Use it for | Notes |
|---|---|---|
| S3 Standard | Frequently accessed data | Default |
| S3 Intelligent-Tiering | Unknown access pattern | Moves data between tiers automatically |
| S3 Standard-IA | Infrequent access | Cheaper storage, retrieval fee |
| S3 One Zone-IA | Infrequent, can be recreated | Only one AZ |
| S3 Glacier Instant Retrieval | Archive, needs millisecond access | |
| S3 Glacier Flexible Retrieval | Archive | Minutes to hours to restore |
| S3 Glacier Deep Archive | Long-term archive | Cheapest, up to ~12 hours to restore |

## Versioning

Versioning keeps every version of an object instead of overwriting it.

- If you overwrite a file, the old version is kept.
- If you delete a file, S3 adds a delete marker and the old versions are still there.
- Once enabled, versioning can only be suspended, not turned off fully.
- Old versions are billed, so it is good to pair this with a lifecycle rule.

```bash
aws s3api put-bucket-versioning --bucket anzar-devops-notes-2026 \
  --versioning-configuration Status=Enabled
```

## Lifecycle policies

Lifecycle rules move or delete objects automatically after some time. This rule moves logs to Standard-IA after 30 days, to Glacier Flexible Retrieval after 90 days, and deletes them after 365 days. It also cleans up old versions after 30 days.

```json
{
  "Rules": [
    {
      "ID": "logs-cleanup",
      "Filter": { "Prefix": "logs/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" }
      ],
      "Expiration": { "Days": 365 },
      "NoncurrentVersionExpiration": { "NoncurrentDays": 30 }
    }
  ]
}
```

```bash
aws s3api put-bucket-lifecycle-configuration --bucket anzar-devops-notes-2026 \
  --lifecycle-configuration file://lifecycle.json
```

## Encryption

- Since January 2023, all new objects are encrypted at rest by default with SSE-S3 (keys managed by S3).
- **SSE-KMS** - uses AWS KMS keys, gives more control and audit logs in CloudTrail.
- **DSSE-KMS** - two layers of KMS encryption, for strict compliance.
- **SSE-C** - you provide the key with every request.
- **Client-side** - you encrypt before uploading.
- In transit, use HTTPS. A bucket policy can deny requests where `aws:SecureTransport` is false.

## Bucket policies

A bucket policy is a resource-based JSON policy attached to the bucket. It controls who can access the bucket, including other accounts or the public.

Example: allow public read of a static website folder (Block Public Access must be turned off for this to work):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::anzar-devops-notes-2026/site/*"
    }
  ]
}
```

ACLs are the older way of controlling access. New buckets have ACLs disabled by default and AWS recommends using policies instead.

## Common use cases

- Backups and database dumps.
- Static website hosting (often with CloudFront in front).
- Storing application logs.
- Storing Terraform state files.
- Data lake for analytics with Athena.
- Storing user uploads like images and videos.
