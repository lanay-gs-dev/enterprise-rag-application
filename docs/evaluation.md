# Evaluation Harness

The evaluation harness checks whether the local RAG pipeline retrieves expected
evidence and refuses unsupported questions.

## Files

- `evals/golden_questions.csv`: small golden dataset of supported and
  unsupported questions
- `evals/eval_runner.py`: builds the local sample index, runs each question, and
  reports pass/fail counts

## What It Measures

- Retrieval match: did the system retrieve the expected source and expected
  supporting text?
- Refusal match: did the system refuse when the dataset says the question is
  unsupported?
- Overall pass: both retrieval and refusal checks passed for the question.

## Run It

```bash
python evals/eval_runner.py
```

The first run may load the local embedding model. If the model is not cached,
network access may be required.

## Initial Local Result

On the current 25-question golden dataset:

```text
Total questions: 25
Overall passed: 22/25
Retrieval checks passed: 25/25
Refusal checks passed: 22/25
```

The current retrieval layer found the expected evidence for supported
questions. The remaining failures are unsupported questions that still received
retrieved chunks with scores above the current refusal threshold.

Known failure examples:

- "What is the parental leave policy?"
- "What is the laptop replacement schedule?"
- "What are the office parking rules?"

These failures are useful because they show the next quality improvement: tune
the refusal threshold, add better unsupported-question detection, or introduce a
stronger LLM-backed citation/refusal check.

## Why This Matters

RAG quality should be measured before and after changes. The evaluation file
gives a repeatable way to check whether chunking, embeddings, vector search, and
refusal rules are improving or regressing.

## AWS Connection

In an AWS-native version, this same evaluation pattern can test:

- S3 document ingestion
- Bedrock embeddings
- OpenSearch Serverless or Bedrock Knowledge Bases retrieval
- Bedrock answer generation
- refusal behavior for unsupported questions

The services may change, but the quality question stays the same: did the system
retrieve the right evidence and avoid unsupported answers?
