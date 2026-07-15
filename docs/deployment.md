# Deployment Plan

**Status:** Planned. The FastAPI service is containerized locally; no live AWS deployment is claimed in this repository.

## First Deployment Slice

```text
Developer
  -> Docker image
  -> Amazon ECR
  -> Amazon ECS Express Mode
  -> public HTTPS FastAPI endpoint
  -> Amazon CloudWatch logs
```

Amazon ECS Express Mode is the preferred first host because it deploys a container on Fargate and configures supporting infrastructure such as networking, load balancing, TLS, monitoring, and auto scaling. See the [AWS ECS Express Mode overview](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.html).

## Deployment Steps

1. Confirm an AWS budget and billing alerts.
2. Build and test the Docker image locally.
3. Create an ECR repository and push the tagged image.
4. Create the required ECS task execution and infrastructure roles.
5. Deploy the image with ECS Express Mode.
6. Verify `/health`, `/docs`, and `/ask`.
7. Review CloudWatch logs and remove unused resources after testing.

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
| Host the containerized FastAPI service | ECS Express Mode | Fits an HTTP container and reduces initial infrastructure setup |
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
