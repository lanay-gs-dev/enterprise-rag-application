# AWS Deployment Steps

## Goal

Deploy the FastAPI RAG service to AWS so Project 1 has a production-style
deployment path.

The local app has two interfaces:

- Streamlit demo: `app.py`
- FastAPI service: `api.py`

For AWS, deploy the FastAPI service first.

## Important AWS Update

AWS App Runner is no longer accepting new customers as of April 30, 2026.

For this project, the recommended first AWS path is now:

```text
Docker image -> Amazon ECR -> Amazon ECS Express Mode -> public HTTPS API
```

App Runner should only be used if the AWS account already has existing App
Runner access. Otherwise, use ECS Express Mode.

## Before AWS

1. Confirm AWS budget alerts are active.
2. Confirm GitHub is up to date.
3. Confirm local tests pass.
4. Confirm Docker Desktop is installed and running.

```bash
git status
python -m unittest discover -s tests
python evals/eval_runner.py
```

## What We Are Deploying

The deployable service is the FastAPI app:

```text
api.py
```

The API exposes:

```text
GET /health
POST /ask
GET /docs
```

Streamlit remains the local demo UI for now. The first AWS deployment should be
the API because it is smaller, easier to test, and closer to a production
service boundary.

## Deployment Architecture

```text
Local code
  -> Dockerfile
  -> local Docker image
  -> Amazon ECR image repository
  -> ECS Express Mode service
  -> public HTTPS endpoint
  -> /health, /docs, /ask
```

## Step 1: Build And Test The Container Locally

From the project root:

```bash
docker build -t enterprise-rag-api .
docker run -p 8000:8000 enterprise-rag-api
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

Expected health response:

```json
{"status":"ok"}
```

## Step 2: Create An ECR Repository

In AWS Console:

1. Open Amazon ECR.
2. Create a private repository.
3. Name it:

```text
enterprise-rag-api
```

4. Save the repository URI.

It will look similar to:

```text
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag-api
```

## Step 3: Push The Docker Image To ECR

Use the commands AWS gives you in the ECR "View push commands" screen.

They will look like this pattern:

```bash
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag enterprise-rag-api:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag-api:latest

docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/enterprise-rag-api:latest
```

Replace:

```text
ACCOUNT_ID
us-east-1
```

with the values from your AWS account and region.

## Step 4: Create The ECS Express Mode Service

In AWS Console:

1. Open Amazon ECS.
2. Choose ECS Express Mode.
3. Create a service.
4. Use the ECR image URI from Step 3.
5. Configure:

```text
Service name: enterprise-rag-api
Container port: 8000
Health check path: /health
CPU/memory: smallest option available for first deployment
Desired tasks: 1
```

6. Use or create the required ECS roles:

```text
ECS task execution role
ECS infrastructure role
```

7. Create the service.
8. Wait for it to reach a running state.
9. Copy the public service URL.

## Step 5: Test The AWS API

Open:

```text
https://YOUR-ECS-URL/health
https://YOUR-ECS-URL/docs
```

Then test `/ask` from Swagger or curl:

```bash
curl -X POST https://YOUR-ECS-URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Is multi-factor authentication required?"}'
```

Expected response fields:

```text
answer
citations
refused
retrieved
```

## Cost Safety

After testing:

1. Review the ECS service status.
2. Review CloudWatch logs.
3. Check AWS Billing.
4. Delete the ECS service if you are done testing.
5. Delete unused load balancers, target groups, and ECR images if needed.

Do not create OpenSearch, Bedrock Knowledge Bases, or SageMaker resources until
the basic API deployment is working and costs are reviewed.

## Next AWS-Native Upgrade

After the FastAPI deployment works:

1. Move sample Markdown documents to S3.
2. Trigger ingestion from S3 changes with Lambda, ECS, or Glue.
3. Replace local embeddings with Bedrock embeddings.
4. Replace Chroma with OpenSearch Serverless or Bedrock Knowledge Bases.
5. Add Bedrock-backed answer generation.
6. Add IAM-scoped access, Secrets Manager, and CloudWatch metrics.

## Interview Explanation

I containerized the FastAPI RAG service and deployed it through the AWS container
path: ECR for image storage and ECS Express Mode for running the service. The
local system still uses Markdown, metadata validation, chunking, embeddings,
retrieval, citations, and refusal checks, but the deployment boundary now looks
like a real production API. This gives me a clean path to replace local pieces
with AWS-native services like S3, Bedrock, OpenSearch, IAM, and CloudWatch.
