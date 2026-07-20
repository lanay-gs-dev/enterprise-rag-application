# Enterprise RAG Application

A Retrieval-Augmented Generation prototype that answers questions over an internal document corpus with retrieved evidence, citations, and refusal behavior.

**Status:** Active prototype. The local RAG pipeline, demo interfaces, tests, evaluation harness, Docker packaging, and AWS backend deployment slice are implemented. LLM-backed generation, authentication, and a polished public UI are planned.

## Problem

Important company knowledge is often scattered across policies, procedures, and operating documents. Traditional search can locate files, but employees still have to find the relevant passage and decide whether it supports an answer.

This project tests a more traceable approach: validate the source documents, retrieve relevant evidence, return citations, and refuse questions the corpus cannot support.

## Implemented

- Markdown ingestion with required front matter
- Metadata validation before indexing
- Deterministic, section-aware chunking
- Local embeddings with `sentence-transformers`
- Chroma vector indexing and ranked retrieval
- Deterministic answer/refusal response shaping
- Streamlit demo and FastAPI `/ask` endpoint
- Docker packaging
- AWS Project 1A deployment of the FastAPI backend with S3, IAM, ECR, ECS/Fargate, ALB, and CloudWatch
- Unit tests and a 25-question evaluation dataset

LLM-backed generation, application-level access-control enforcement, and a polished public UI are not yet implemented.

## Architecture

```text
Documents
  -> metadata validation
  -> chunking
  -> local embeddings
  -> Chroma vector index
  -> ranked retrieval
  -> answer or refusal with citations
  -> evaluation
```

Streamlit provides the local user demo. FastAPI exposes the same pipeline to other applications through an HTTP interface.

Project 1A deploys the FastAPI backend API to AWS. The live endpoint is intentionally not published in this repository because the demo API is unauthenticated.

## Run Locally

Install dependencies and run the tests:

```bash
pip install -r requirements.txt
python3 -m unittest discover -s tests
```

Run the command-line demo and evaluation harness:

```bash
python3 scripts/run_rag_demo.py
python3 evals/eval_runner.py
```

Run either interface:

```bash
streamlit run app.py
uvicorn api:app --reload
```

Example API request:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Is multi-factor authentication required?"}'
```

Build the API container:

```bash
docker build -t enterprise-rag-api .
docker run -p 8000:8000 enterprise-rag-api
```

## AWS Deployment Slice

The backend API has been deployed as a containerized FastAPI service using:

```text
S3 document storage
IAM users, groups, task role, and execution role
Amazon ECR image repository
Amazon ECS/Fargate service
Application Load Balancer
CloudWatch logs and ECS metrics
```

The deployed service exposes:

```text
GET /health
GET /docs
POST /ask
```

The public load balancer URL is not included because the prototype does not yet have authentication, rate limiting, or a polished user-facing interface.

## Evaluation Baseline

The current 25-question golden dataset produced:

```text
Overall: 22/25
Retrieval: 25/25
Refusal: 22/25
```

The three failures are unsupported questions that retrieved weakly related evidence above the current refusal threshold. They identify the next quality task: improve unsupported-question detection without reducing retrieval accuracy.

See [Evaluation](docs/evaluation.md) for the method and known failure cases.

## Repository Layout

```text
data/sample/              Fictional source documents
docs/                     Architecture, decisions, requirements, and evaluation
evals/                    Golden questions and evaluation runner
scripts/                  Local demos and utilities
src/enterprise_rag/       Application package
tests/                    Focused unit tests
```

## Documentation

- [Project blueprint](docs/project-blueprint.md)
- [Architecture](docs/architecture.md)
- [Requirements discovery](docs/requirements-discovery.md)
- [Engineering decisions](docs/engineering-decisions.md)
- [Evaluation](docs/evaluation.md)
- [Deployment plan](docs/deployment.md)
- [AWS access control map](docs/aws-access-control-map.md)
- [S3 sample data map](docs/s3-sample-data-map.md)

## AWS Production Mapping

| Local prototype | AWS production option |
| --- | --- |
| Local document files | Amazon S3 |
| Local ingestion pipeline | AWS Lambda or an ECS task |
| `sentence-transformers` | Amazon Bedrock embedding model |
| Chroma vector index | Amazon OpenSearch or Bedrock Knowledge Bases |
| Dockerized FastAPI service | Amazon ECR, ECS/Fargate, and an Application Load Balancer |
| Planned LLM-backed generation | Amazon Bedrock |
| Local logs and configuration | CloudWatch, IAM, and Secrets Manager |

## Next Steps

- Add authentication before publishing a public demo URL
- Add a polished user-facing UI that calls the deployed FastAPI backend
- Add LLM-backed grounded generation
- Improve refusal behavior against the evaluation set
- Compare the custom retrieval pipeline with Bedrock Knowledge Bases
- Add application-level metadata-based access controls

## Repository Note

All sample documents are fictional. No private client, employer, or personal business data is included.
