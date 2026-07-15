# Requirements Discovery

This document summarizes the requirements behind the public prototype. The scenario is representative and uses fictional documents; it does not describe a private client environment.

## Business Problem

Employees need reliable answers from policies, procedures, and operating documents. Existing search may locate a file, but users still spend time finding the relevant passage and confirming that it supports the answer.

## Users

- Employees asking policy and operations questions
- Document owners maintaining source content
- Engineers and risk partners reviewing retrieval quality and traceability

## Core Requirements

| Requirement | Why it matters | Prototype status |
| --- | --- | --- |
| Validate document metadata before indexing | Prevents unowned or improperly classified content from entering retrieval | Implemented |
| Preserve source identity through chunking and retrieval | Makes citations and troubleshooting possible | Implemented |
| Retrieve evidence relevant to the question | Grounds the response in the document corpus | Implemented |
| Return source citations | Lets users inspect the supporting material | Implemented |
| Refuse unsupported questions | Reduces confident answers without evidence | Implemented and under evaluation |
| Expose the workflow through an API | Allows integration with other applications | Implemented locally |
| Enforce user access at retrieval time | Prevents unauthorized evidence from reaching the model | Planned |
| Generate natural-language answers with an LLM | Improves response quality while retaining evidence constraints | Planned |

## Nonfunctional Requirements

- **Explainability:** retrieval results, scores, and source identifiers should be inspectable.
- **Testability:** ingestion, chunking, retrieval, and refusal behavior should have repeatable checks.
- **Security:** source classification and user authorization must be enforced before production use.
- **Maintainability:** each pipeline stage should have a clear input and output contract.
- **Cost awareness:** the local prototype should establish a baseline before managed AWS services are introduced.

## Acceptance Criteria

The prototype should:

1. Reject documents missing required metadata.
2. Create stable chunks that preserve source metadata.
3. Retrieve expected evidence for supported evaluation questions.
4. Return citation identifiers with supported responses.
5. Refuse unsupported questions based on an explicit threshold.
6. Provide the same pipeline through local demo and API interfaces.

## Open Production Questions

- Which identity provider and authorization model will control document access?
- How frequently will documents change, and should indexing be batch or event-driven?
- What latency and availability targets are required?
- Which managed vector option provides the right balance of control, cost, and operational effort?
- What evidence and model activity may be retained in logs?
