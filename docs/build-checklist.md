# Build Checklist

## Current Phase: Phase 1 - Ingestion

### Objective

Load Markdown documents, validate required metadata, and return clean `Document`
objects ready for chunking.

### Where We Are

- [x] Scenario reviewed at a high level
- [x] Business problem connected to messy internal knowledge repositories
- [x] Phase 1 input/output clarified
- [x] Project 1 source-of-truth folder clarified
- [ ] Phase 1 implementation reviewed line by line
- [ ] Tests run successfully
- [ ] Phase 1 explained in interview form

### Before Coding

- [x] What problem are we solving?
- [x] What are the inputs?
- [x] What are the outputs?
- [ ] How will we test it?
- [ ] What could fail?

### Definition Of Done

- [ ] I can explain what ingestion does.
- [ ] Loader reads one Markdown file.
- [ ] Loader reads a folder of Markdown files.
- [ ] Required metadata is validated.
- [ ] Missing metadata fails loudly.
- [ ] Invalid security level fails loudly.
- [ ] Tests pass.
- [ ] I can explain the AWS equivalent.

### Files

- `data/sample/*.md`
- `src/enterprise_rag/models.py`
- `src/enterprise_rag/ingestion.py`
- `tests/test_ingestion_chunking.py`

### Phase 1 Data Flow

```text
Markdown file
  -> read raw text
  -> split front matter metadata from body content
  -> validate required metadata
  -> return Document object
  -> ready for chunking
```

### Why Predictable Folder Loading Matters

Folder order is an engineering reliability issue. If files load in a different
order every run, tests can become flaky and chunk IDs can be harder to debug.
Sorting files gives the same input order every time.

### Common Failure Modes

- Missing required metadata
- Blank metadata values
- Invalid `security_level`
- Bad `effective_date` format
- Missing or malformed front matter
- Wrong source folder path
- Empty or unusable content

### AWS Equivalent

Local Markdown files are like objects in S3. The ingestion loader is like a
Lambda function or container job that validates documents before they are
chunked, embedded, and indexed.

### Interview Explanation Draft

Ingestion is the quality gate for the RAG system. Before documents can be
chunked or retrieved, the system validates that each source has required
metadata like owner, security level, source ID, and effective date. This
prevents unowned, stale, or improperly classified content from entering the
retrieval pipeline.
