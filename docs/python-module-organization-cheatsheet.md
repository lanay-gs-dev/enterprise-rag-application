# Python Module Organization Cheat Sheet

## The Big Idea

A Python file is easier to understand when each block has a clear job.

Use this mental order:

```text
imports
  -> rules
  -> errors
  -> shapes
  -> helpers
  -> main functions
  -> script runner
```

This is not a law. It is a default structure that keeps the file readable.

## 1. Imports - Tools I Need

Imports bring in tools from Python or other libraries.

```python
from dataclasses import dataclass
from pathlib import Path
```

Ask:

```text
What outside tools does this file need?
```

## 2. Constants / Rules - Fixed Business Or System Rules

Constants are values that stay the same during the program run.

```python
REQUIRED_FIELDS = {"title", "owner", "security_level"}
ALLOWED_SECURITY_LEVELS = {"public", "internal", "confidential"}
```

Ask:

```text
What rules should be easy to see and reuse?
```

## 3. Custom Errors - Named Ways The Program Can Fail

Custom errors make failures easier to understand.

```python
class MetadataValidationError(ValueError):
    pass
```

Ask:

```text
What failure needs a clear name?
```

## 4. Data Shapes - What Clean Data Looks Like

A data shape defines what fields an object should have.

```python
@dataclass
class Document:
    source_path: str
    content: str
    metadata: dict[str, str]
```

Ask:

```text
What should a clean record/object contain?
```

SAS bridge:

```text
Data shape = expected dataset/table structure
```

## 5. Helper Functions - Small Support Steps

Helpers do one small job that supports the main function.

```python
def has_required_fields(metadata: dict[str, str]) -> bool:
    return REQUIRED_FIELDS <= metadata.keys()
```

Ask:

```text
What small repeatable step would make the main function cleaner?
```

## 6. Main Functions - The Main Job Of The File

Main functions are what other files are likely to call.

```python
def load_document(path: str) -> Document:
    text = Path(path).read_text()
    metadata = {"title": "Example", "owner": "team"}

    if not has_required_fields(metadata):
        raise MetadataValidationError("Missing required fields")

    return Document(source_path=path, content=text, metadata=metadata)
```

Ask:

```text
What is this file responsible for doing?
```

## 7. Script Runner - Run This File Directly

This block only runs when the file is executed directly.

```python
if __name__ == "__main__":
    document = load_document("example.md")
    print(document)
```

Ask:

```text
Do I need a quick demo or command-line entry point for this file?
```

## The Most Important Placement Rule

Put things above the code that needs them.

```text
If a function uses REQUIRED_FIELDS, define REQUIRED_FIELDS above the function.
If a function returns Document, define Document above the function.
```

## Rule / Shape / Action Framework

When you are not sure where code belongs, classify it:

```text
rule   -> near the top
shape  -> middle
action -> lower
run    -> bottom
```

Examples:

| Code | Category |
|---|---|
| `REQUIRED_FIELDS = {...}` | rule |
| `class Document` | shape |
| `def validate_metadata(...)` | action |
| `if __name__ == "__main__"` | run |

## How This Applies To Project 1

`models.py` owns rules and shapes:

```text
required metadata fields
allowed security levels
custom metadata error
Document shape
DocumentChunk shape
metadata validation
```

`ingestion.py` owns loading:

```text
find Markdown files
read text
parse front matter
validate metadata
return Document objects
```

## Pre-Code Checklist

Before writing a module, ask:

1. What is this file responsible for?
2. What inputs does it receive?
3. What rules does it need?
4. What clean object/data should come out?
5. What can fail?
6. What small helper steps support the main job?
7. What is the main function someone else will call?

## Interview Line

I organize Python modules around responsibility. I put imports first, visible
rules near the top, data shapes before the functions that return them, helper
functions before or near the main workflow, and executable demo code at the
bottom. That makes the file easier to read, test, and extend.
