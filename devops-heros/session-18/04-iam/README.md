# IAM: Identity and Access Management

## What Is IAM?

AWS Identity and Access Management (IAM) controls who can access AWS resources and what actions they can perform. IAM supports authentication, authorization, and least-privilege access.

## Key Concepts

- **User:** An identity for a person or application that needs AWS access.
- **Group:** A collection of users that can share permissions.
- **Role:** An identity with permissions that can be assumed by trusted users or AWS services.
- **Policy:** A JSON document that allows or denies actions on resources.
- **Principal:** The user, role, account, or service making a request.
- **MFA:** An additional authentication factor that protects accounts from stolen passwords.

## Important Lessons

Use the root account only for tasks that require it and protect it with MFA. Give users and workloads only the permissions they need. Prefer temporary credentials and IAM roles over long-lived access keys. Review unused users, keys, roles, and permissions regularly.

## Example Permission Idea

A deployment role might be allowed to upload objects to one S3 bucket but not delete objects from other buckets. Permissions should identify the specific actions and resources required by the job.

## Reflection

- Why are IAM roles preferred for EC2 applications?
- What is the principle of least privilege?
- What steps would you take after discovering an exposed access key?
