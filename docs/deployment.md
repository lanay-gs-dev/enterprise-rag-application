# Deployment

**Status:** Project 1A backend deployment completed. The FastAPI service has
been containerized, pushed to Amazon ECR, and run on Amazon ECS/Fargate behind
an Application Load Balancer.

The live URL is intentionally not published in this repository because the
prototype API is unauthenticated.

## Implemented Deployment Slice

```text
Developer
  -> Docker image
  -> Amazon ECR
  -> Amazon ECS/Fargate service
  -> Application Load Balancer
  -> FastAPI /health, /docs, /ask
  -> Amazon CloudWatch logs
```

ECS/Fargate is the first deployment host because it runs the same Dockerized
FastAPI service that was tested locally while exposing real AWS deployment
concepts: task definitions, task roles, task execution roles, services, load
balancing, health checks, CloudWatch logs, and deployment rollbacks.

## Implemented AWS Resources

| Layer | Resource |
| --- | --- |
| Document storage | S3 bucket with `documents/`, `ingestion/`, and `evaluation/` prefixes |
| Human access model | IAM groups and scoped S3 policies |
| App runtime permissions | ECS task role with S3 document read access |
| ECS startup permissions | ECS task execution role for ECR pull and CloudWatch logs |
| Image storage | ECR repository `enterprise-rag-api` |
| Runtime | ECS/Fargate service `enterprise-rag-api` |
| Routing | Application Load Balancer and target group |
| Health check | Target group HTTP health check on `/health` |
| Observability | CloudWatch log group `/ecs/enterprise-rag-api` |

## Key Deployment Lessons

- Docker packages the Python FastAPI app and dependencies; it does not replace
  the Python RAG logic.
- ECR stores the Docker image; ECS runs the image as a container.
- The task role is for application permissions after startup.
- The task execution role is for ECS startup actions such as ECR image pull and
  CloudWatch log setup.
- Images built on Apple Silicon may default to ARM64. The ECS task used
  Linux/X86_64, so the image had to be rebuilt and pushed for `linux/amd64`.
- The container health check was left blank. The load balancer target group uses
  `/health` as the HTTP health check path.
- The initial `.25 vCPU` and `.5 GB` task size was too small for this Python AI
  stack, so the task definition was increased to `1 vCPU` and `3 GB`.

## Verification

The deployed backend exposes:

```text
GET /health
GET /docs
POST /ask
```

Expected checks:

```text
/health returns {"status":"ok"}
/docs opens FastAPI Swagger UI
/ask returns answer, citations, refusal flag, and retrieved chunks
CloudWatch receives container logs
```

The Swagger UI is a developer testing interface, not a polished public website.
A user-facing UI should be added only after authentication and cost controls are
in place.

## AWS-Native RAG Upgrade

After the API is reachable:

```text
S3 documents
  -> ingestion job
  -> Bedrock embeddings
  -> OpenSearch vector index or Bedrock Knowledge Bases
  -> FastAPI retrieval service
  -> Bedrock grounded generation
  -> CloudWatch logs and metrics
```

Bedrock Knowledge Bases can manage document ingestion, chunking, embeddings, and supported vector stores. The project will compare that managed path with the custom local pipeline before choosing a production design. See [AWS Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-it-works.html).

## Service Choices

| Need | Preferred option | Reason |
| --- | --- | --- |
| Host the containerized FastAPI service | ECS/Fargate | Runs the Dockerized backend without managing EC2 instances |
| Process document uploads asynchronously | Lambda or an ECS task | Event-driven ingestion should be separate from the request API |
| Store source documents | S3 | Durable object storage with event and lifecycle support |
| Generate embeddings and answers | Bedrock | Managed model access without hosting model infrastructure |
| Store and search vectors | OpenSearch or Bedrock Knowledge Bases | Managed retrieval with metadata filtering options |
| Observe the system | CloudWatch | Central logs, metrics, and alarms |

## Cost Considerations

- ECS charges come from the underlying Fargate, load balancer, networking, and logging resources.
- Bedrock cost grows with embedding and generation usage.
- A managed vector store may become the largest fixed prototype expense, so it should be tested against lower-cost or fully managed alternatives.
- CloudWatch retention should be bounded, and logs should avoid full sensitive document content.
- Development resources should be tagged and removed when they are no longer needed.

## Security Requirements

- Use least-privilege IAM roles for ECR, ECS, S3, Bedrock, and vector access.
- Store secrets in Secrets Manager or Parameter Store, not source control.
- Enforce document authorization before retrieved text reaches a model.
- Encrypt data in transit and at rest.
- Keep sensitive source text out of application logs.
