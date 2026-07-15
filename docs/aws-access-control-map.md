# AWS Access Control Map

Project 1A uses S3 prefixes and IAM policies to model document-level access
before the full RAG app authorization layer is built.

## Account Pattern

```text
root account
  -> billing, organization setup, emergency access only

lanay-rag-admin
  -> non-root admin user for project setup
  -> creates S3, IAM policies, ECR, ECS, and CloudWatch resources

test users
  -> limited users for proving access boundaries
```

## S3 Bucket

```text
enterprise-rag-project-1a-lgs-123456789012
```

## S3 Prefixes

```text
documents/public/
documents/internal/
documents/confidential/
ingestion/raw/
ingestion/rejected/
evaluation/
```

## IAM Groups And Policies

| Group | Policy | Intended access |
| --- | --- | --- |
| `rag-public-readers` | `rag-public-readers-s3-read` | Read `documents/public/` only |
| `rag-internal-readers` | `rag-internal-readers-s3-read` | Read `documents/public/` and `documents/internal/` |
| `rag-content-owners` | `rag-content-owners-s3-access` | Upload/read `ingestion/raw/`, read `ingestion/rejected/` |
| `rag-engineers` | `rag-engineers-s3-admin` | Manage objects in the Project 1A bucket |

## Access Model

```text
public reader
  -> public documents

internal reader
  -> public documents
  -> internal documents

content owner
  -> raw submissions
  -> rejected documents

engineer
  -> project bucket management
```

## Why This Matters

This gives the project an AWS-level security layer:

```text
IAM group
  -> IAM policy
  -> S3 bucket prefix
```

The future RAG app should still filter by metadata, but S3 access is no longer
treated as an afterthought. Storage access and application access become
separate layers.

## Next AWS Step

After the S3/IAM layer is in place, move to the deployment layer:

```text
Docker image
  -> Amazon ECR
  -> ECS Express Mode
  -> FastAPI /health, /docs, /ask
```
