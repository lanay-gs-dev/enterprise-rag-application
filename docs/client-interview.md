# Client Interview - Discovery Before Design

**Why this file exists:** RAG requirements should come from stakeholder needs,
not from assumptions. This simulated client interview explains why Project 1
requires metadata, source ownership, security labels, citations, refusals, and
repeatable ingestion.

---

**Client:** Maya Ellis, VP of Operations Enablement  
**Company:** Northstar Services Group, fictional multi-location services company  
**Interviewer:** Solutions engineering  
**Context:** Northstar employees search across handbooks, policies, SOPs, and
operations reports. The current knowledge repository is difficult to search,
contains stale documents, and gives employees inconsistent answers.

## Q1. What problem are you trying to solve?

> "Employees waste too much time trying to find the right policy or procedure.
> Search returns whole documents, not answers, and people often find old or
> duplicated guidance. I need a system that can answer common operational
> questions and show exactly where the answer came from."

## Q2. Who uses this?

> "Frontline employees ask policy and operations questions. Support and IT teams
> maintain the source documents. Operations leaders want to see which answers
> are supported by evidence and where the knowledge base has gaps. Engineers
> need retrieval debug information so they can improve quality."

## Q3. What data do you trust?

> "A document is trustworthy enough to index only if we know its title, owner,
> source ID, department, document type, effective date, and security level. If
> we do not know who owns it or whether employees are allowed to see it, I do
> not want the system using it to answer questions."

## Q4. What data should be excluded?

> "Drafts, stale documents, documents with missing ownership, and anything with
> unclear security classification. If a document is missing required metadata,
> do not index it. Put it on an exception list so the owner can fix it."

## Q5. What risks are unacceptable?

> "The worst outcome is a confident answer that is not backed by the documents.
> I also cannot have confidential guidance shown to the wrong audience. If the
> evidence is missing, ambiguous, or not retrieved, the system should say it
> does not have enough information instead of guessing."

## Q6. What does success look like?

> "Employees get cited answers in seconds for common questions. Every answer
> links back to source chunks. Unsupported questions are refused. The team can
> see which documents failed ingestion, which chunks were retrieved, and which
> questions need better source material."

---

## What We Heard -> What We Built

| Interview signal | Requirement | Where it lives |
|---|---|---|
| "show exactly where the answer came from" | Stable `source_id`, chunk IDs, and citation IDs | `src/enterprise_rag/models.py`, `src/enterprise_rag/retrieval.py`, `src/enterprise_rag/generation.py` |
| "support and IT teams maintain source documents" | Required `owner` and `department` metadata | `src/enterprise_rag/models.py` |
| "engineers need retrieval debug information" | Deterministic ingestion, stable chunk IDs, ranked retrieved chunks | `src/enterprise_rag/ingestion.py`, `src/enterprise_rag/chunking.py`, `src/enterprise_rag/retrieval.py` |
| "title, owner, source ID, department, document type, effective date, security level" | Required metadata contract | `REQUIRED_METADATA_FIELDS` in `src/enterprise_rag/models.py` |
| "do not index it; put it on an exception list" | Fail-fast validation now; future quarantine workflow | `validate_metadata`, future ingestion reporting |
| "confidential guidance shown to wrong audience" | Security label required before indexing | `security_level` validation |
| "say it does not have enough information instead of guessing" | Deterministic refusal behavior now; LLM-backed refusal later | `src/enterprise_rag/generation.py` |
| "which documents failed ingestion" | Clear validation errors and tests | `MetadataValidationError`, `tests/test_ingestion_chunking.py` |

## Data Contract For Phase 1

Every Markdown document must include front matter with:

- `title`: human-readable document name
- `source_id`: stable ID used for citations, chunk IDs, and debugging
- `document_type`: policy, SOP, handbook, report, or guide
- `department`: accountable business area
- `effective_date`: date the guidance became valid
- `owner`: team or person accountable for updates
- `security_level`: one of `public`, `internal`, or `confidential`

## Phase 1 Policy Decision

For this prototype, missing required metadata causes ingestion to fail. In a
production enterprise workflow, the document would usually be routed to a
quarantine bucket, remediation queue, or data-quality report instead of being
silently indexed.

## Interview Line

Before coding, I simulated a stakeholder discovery interview and turned the
answers into a data contract. That is why ingestion rejects documents missing
ownership, security labels, source IDs, or effective dates: the RAG system
should only answer from governed, traceable source material.
