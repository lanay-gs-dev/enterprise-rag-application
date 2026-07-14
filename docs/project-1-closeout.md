# Project 1 Closeout

## What I Built

This project implements a local Enterprise RAG foundation for answering
questions from internal documents with traceable evidence.

Implemented components:

- Markdown document ingestion
- Required metadata validation
- Deterministic paragraph-aware chunking
- Local text and query embeddings
- Local Chroma vector store wrapper
- Retrieval layer for ranked evidence chunks
- Deterministic answer/refusal contract
- Streamlit demo interface
- FastAPI service layer with `/health` and `/ask`
- Docker deployment files for the FastAPI service
- Unit tests for ingestion, chunking, embeddings, vector storage, retrieval,
  generation/refusal, and API behavior

## Why It Works

The system separates the RAG pipeline into clear stages:

```text
documents
  -> metadata validation
  -> chunks
  -> embeddings
  -> vector store
  -> retrieval
  -> answer/refusal
```

Each stage has one job and passes a structured object to the next stage. This
makes the project easier to test, explain, debug, and extend.

## Common Failure Modes

- Missing or invalid metadata prevents reliable citations and ownership.
- Poor chunking can split context and reduce retrieval quality.
- Embedding model downloads can fail without network access.
- Vector stores can return weak evidence if chunks are too broad or too small.
- A system without refusal behavior may answer unsupported questions.
- A demo UI can hide backend issues if the API and pipeline are not tested
  separately.

## AWS Equivalent

| Local Project Component | AWS / Enterprise Equivalent |
| --- | --- |
| `data/sample` Markdown files | S3, SharePoint, Confluence, internal repositories |
| Python ingestion code | Lambda, ECS task, Glue job |
| Metadata validation | Data governance rules, catalog checks, access policies |
| Local chunking | Batch processing pipeline |
| `sentence-transformers` embeddings | Amazon Bedrock embeddings or SageMaker endpoint |
| Chroma vector store | OpenSearch Serverless or Bedrock Knowledge Bases |
| FastAPI service | ECS Express Mode, ECS Fargate, or API Gateway + Lambda |
| Streamlit demo | Internal portal, React UI, or prototype dashboard |
| Local logs/tests | CloudWatch, CI/CD checks, evaluation reports |
| `.env` / local config | IAM, Secrets Manager, Parameter Store |

## 30-Second Interview Explanation

I built a local Enterprise RAG system that turns internal Markdown documents
into validated, searchable evidence. I started with ingestion and metadata
validation because reliable RAG depends on trusted source documents. Then I
added deterministic chunking, local embeddings, a Chroma vector store, retrieval,
and a refusal-aware answer contract. I also built both a Streamlit demo and a
FastAPI service layer, with tests covering the core pipeline. The local version
maps naturally to AWS using S3, Lambda or ECS, Bedrock embeddings, OpenSearch or
Bedrock Knowledge Bases, ECS Express Mode, and CloudWatch.

## What I Would Improve Next

- Replace the deterministic placeholder answer with Bedrock-backed generation.
- Add citation verification against retrieved chunk IDs.
- Add an evaluation set for retrieval accuracy and refusal behavior.
- Move sample documents to S3 and run ingestion from an AWS service.
- Replace local Chroma with OpenSearch Serverless or Bedrock Knowledge Bases.
- Deploy the FastAPI service using ECS Express Mode.
- Add authentication, request logging, and cost monitoring.
