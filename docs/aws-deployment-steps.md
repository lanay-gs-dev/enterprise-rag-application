# AWS Deployment Steps

## Goal

Deploy the FastAPI RAG service to AWS so Project 1 has a production-style
deployment path.

The local app has two interfaces:

- Streamlit demo: `app.py`
- FastAPI service: `api.py`

For AWS, deploy the FastAPI service first.

## Before AWS

1. Confirm budget alerts are active.
2. Confirm GitHub is up to date.
3. Confirm local tests pass.

```bash
git status
python -m unittest discover -s tests
python evals/eval_runner.py
```

## Recommended First AWS Path

Use AWS App Runner if it is available in your AWS account.

Why:

- It is simpler than ECS for a first deployment.
- It is designed for web apps and APIs.
- It can connect to GitHub or deploy from a container image.
- It gives a public HTTPS endpoint.

If App Runner is not available in your account, use ECS Fargate as the fallback.

## Option A: App Runner From GitHub Source

This avoids Docker at first.

1. Open AWS Console.
2. Go to App Runner.
3. Create service.
4. Choose source code repository.
5. Connect GitHub.
6. Select:

```text
Repository: lanay-gs-dev/enterprise-rag-application
Branch: main
Source directory: /
```

7. Configure build:

```text
Runtime: Python 3
Build command: pip install .
Start command: uvicorn api:app --host 0.0.0.0 --port 8000
Port: 8000
```

8. Configure service:

```text
Service name: enterprise-rag-api
CPU/memory: smallest available option
Deployment: manual for first deployment
```

9. Create and deploy.
10. Wait for status: `Running`.
11. Open the default App Runner URL.
12. Test:

```text
/health
/docs
```

## Option B: Docker Image To ECR, Then App Runner Or ECS

Use this if you want to practice container deployment.

Local build:

```bash
docker build -t enterprise-rag-api .
docker run -p 8000:8000 enterprise-rag-api
```

Test locally:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

Then:

1. Create an ECR repository.
2. Authenticate Docker to ECR.
3. Tag the image.
4. Push the image.
5. Create App Runner or ECS Fargate service from that image.

## First Production Checks

After deployment, verify:

```text
GET /health returns {"status": "ok"}
POST /ask returns answer, citations, refused, retrieved
CloudWatch logs show startup and request logs
```

Example request:

```bash
curl -X POST https://YOUR-AWS-URL/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Is multi-factor authentication required?"}'
```

## Cost Safety

After testing:

1. Review App Runner or ECS service status.
2. Review CloudWatch logs.
3. Check AWS Billing.
4. Pause or delete the service if you are done testing.

Do not create OpenSearch, Bedrock Knowledge Bases, or SageMaker resources until
the basic API deployment is working and costs are reviewed.

## Next AWS-Native Upgrade

After the FastAPI deployment works:

1. Move sample Markdown documents to S3.
2. Trigger ingestion from S3 changes.
3. Replace local embeddings with Bedrock embeddings.
4. Replace Chroma with OpenSearch Serverless or Bedrock Knowledge Bases.
5. Add Bedrock-backed answer generation.
6. Add IAM-scoped access, Secrets Manager, and CloudWatch metrics.
