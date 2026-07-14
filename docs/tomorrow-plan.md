# Tomorrow Plan

## Goal

Use Project 1 as the base for AWS learning by first understanding the complete
local system, then running the evaluation harness, then preparing the AWS
deployment path.

## Part 1: Walk The Project Top To Bottom

1. `README.md`
2. `docs/project-1-closeout.md`
3. `docs/architecture.md`
4. `docs/project-blueprint.md`
5. `src/enterprise_rag/models.py`
6. `ingestion.py`
7. `chunking.py`
8. `embeddings.py`
9. `vectorstore.py`
10. `retrieval.py`
11. `generation.py`
12. `pipeline.py`
13. `app.py`
14. `api.py`
15. `tests/`
16. `evals/`

## Part 2: Run Verification

```bash
python -m unittest discover -s tests
python main.py
python scripts/run_rag_demo.py
python evals/eval_runner.py
```

## Part 3: Interpret Evaluation Results

For each failure, ask:

- Did retrieval miss the right source?
- Did the expected text live in a different chunk?
- Was the question actually unsupported?
- Is the score threshold too strict or too loose?
- Does the sample corpus need better source material?

## Part 4: AWS Deployment Setup

Start with the safest AWS path:

1. Confirm budget alerts are active.
2. Install Docker Desktop or choose an App Runner source deployment path.
3. Build and test the FastAPI container locally.
4. Deploy FastAPI to AWS App Runner.
5. Confirm `/health` and `/ask`.
6. Watch CloudWatch logs.

## Part 5: AWS-Native Upgrade Roadmap

After the FastAPI service is deployed:

- Move sample documents to S3.
- Replace local embeddings with Bedrock embeddings.
- Replace Chroma with OpenSearch Serverless or Bedrock Knowledge Bases.
- Add Bedrock-backed answer generation.
- Add IAM permissions, Secrets Manager, and CloudWatch metrics.

## Definition Of Done For The Next Session

- I can explain every local component.
- I can run the evaluation harness.
- I understand what the eval results mean.
- I know the first AWS deployment target.
- I know which local components map to AWS services.
