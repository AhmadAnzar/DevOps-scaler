# IAM - Governance

IAM (Identity and Access Management) is the AWS service that decides who can log in and what they are allowed to do. I covered it first because every other service depends on it.

## What is IAM?

IAM is how you control access to your AWS account. It answers two things: who is making the request (authentication) and whether they are allowed to do it (authorization).

A few things I noted:

- IAM is global. It is not tied to a region.
- It is free. You only pay for the resources people create.
- When you create an AWS account you get a root user. The root user can do everything, so it should not be used for daily work.

## Users

An IAM user is one identity, usually one person or one application.

- A user can have a password (for the console) and access keys (for the CLI/SDK).
- A new user has no permissions at all until you give them some.
- For people, AWS now recommends IAM Identity Center (SSO) instead of long-lived IAM users. I still used plain IAM users for practice.

```bash
aws iam create-user --user-name anzar-dev
aws iam list-users
```

## Groups

A group is a collection of users. You attach policies to the group and every user in it gets those permissions.

- Example groups: `Developers`, `Admins`, `ReadOnly`.
- A user can be in more than one group.
- Groups cannot contain other groups.

```bash
aws iam create-group --group-name Developers
aws iam add-user-to-group --user-name anzar-dev --group-name Developers
```

## Roles

A role is an identity that has permissions but no password or permanent keys. Someone or something "assumes" the role and gets temporary credentials.

What I noticed is that roles are used a lot more than users in real setups:

- An EC2 instance uses a role to read from S3, so no keys are stored on the server.
- A Lambda function uses a role to write to DynamoDB.
- A user from another AWS account can assume a role to get access.
- GitHub Actions can assume a role through OIDC, so no AWS keys go into the repo.

Each role has a trust policy (who can assume it) and permission policies (what it can do).

## Policies

A policy is a JSON document that lists permissions. Main parts:

| Field | Meaning |
|---|---|
| `Effect` | `Allow` or `Deny` |
| `Action` | API actions, e.g. `s3:GetObject` |
| `Resource` | ARN of what the action applies to |
| `Condition` | Optional extra rules (IP, MFA, tags, etc.) |

Types of policies I came across:

- **AWS managed** - written by AWS, like `ReadOnlyAccess`.
- **Customer managed** - written by you, reusable.
- **Inline** - attached directly to one user/group/role.
- **Resource-based** - attached to a resource, like an S3 bucket policy.

## Permissions

How AWS decides if a request is allowed:

1. Everything is denied by default.
2. An explicit `Allow` in any policy allows it.
3. An explicit `Deny` always wins, even over an Allow.

So if a user has `Allow s3:*` from one policy and `Deny s3:DeleteObject` from another, they cannot delete objects.

## Least privilege

Least privilege means giving only the permissions needed for the job and nothing extra.

Example: an app only needs to read files from one bucket. Instead of giving it `AmazonS3FullAccess`, I would write this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-app-reports"
    },
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-app-reports/*"
    }
  ]
}
```

`ListBucket` goes on the bucket ARN and `GetObject` goes on the objects (`/*`). I got this wrong the first time and the list call failed.

IAM Access Analyzer can also look at what a role actually used and suggest a tighter policy.

## IAM best practices

- Do not use the root user for daily work. Turn on MFA for it.
- Turn on MFA for all human users.
- Use roles instead of access keys wherever possible.
- If you must use access keys, rotate them and never commit them to Git.
- Give permissions to groups, not to individual users.
- Start with least privilege and add more only when needed.
- Remove users, keys and roles that are no longer used.
- Use CloudTrail to see who did what.

## Common use cases

- Giving each team member their own login with only the access they need.
- Letting EC2 or Lambda talk to other AWS services without storing keys.
- Letting a CI/CD pipeline deploy to AWS through a role.
- Giving a third party or another account limited access through a cross-account role.
- Blocking risky actions (like deleting production data) with explicit Deny rules.
