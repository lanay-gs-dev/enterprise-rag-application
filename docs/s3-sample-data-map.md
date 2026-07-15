# S3 Sample Data Map

Use this map while uploading Project 1A sample documents to S3.

## Bucket Layout

```text
s3://YOUR-BUCKET/
  documents/
    public/
    internal/
    confidential/
  ingestion/
    raw/
    rejected/
  evaluation/
```

## Upload Map

| Local file | Security level | S3 prefix |
| --- | --- | --- |
| `data/sample/company-overview.md` | public | `documents/public/` |
| `data/sample/wellness-services-overview.md` | public | `documents/public/` |
| `data/sample/holiday-calendar.md` | public | `documents/public/` |
| `data/sample/employee-handbook.md` | internal | `documents/internal/` |
| `data/sample/it-support-guide.md` | internal | `documents/internal/` |
| `data/sample/procurement-guidelines.md` | internal | `documents/internal/` |
| `data/sample/security-policy.md` | confidential | `documents/confidential/` |
| `data/sample/incident-response-playbook.md` | confidential | `documents/confidential/` |
| `data/sample/vendor-risk-review.md` | confidential | `documents/confidential/` |

## Rule

The S3 prefix should match the document metadata:

```yaml
security_level: public
```

goes to:

```text
documents/public/
```

Documents with missing or invalid metadata should go to:

```text
ingestion/raw/
```

Then the validation process can move or copy failed files to:

```text
ingestion/rejected/
```
