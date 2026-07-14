from __future__ import annotations

from pathlib import Path
from enterprise_rag.models import Document, MetadataValidationError, validate_metadata


def load_markdown_documents(path: str | Path) -> list[Document]:
    root = Path(path)
    files = sorted(root.rglob("*.md")) if root.is_dir() else [root]
    return [load_markdown_document(file_path) for file_path in files]


def load_markdown_document(path: str | Path) -> Document:
    source_path = Path(path)
    raw_text = source_path.read_text(encoding="utf-8")
    metadata, content = parse_front_matter(raw_text)
    validate_metadata(metadata)
    return Document(source_path=str(source_path), content=content.strip(), metadata=metadata)


def parse_front_matter(raw_text: str) -> tuple[dict[str, str], str]:
    if not raw_text.startswith("---\n"):
        raise MetadataValidationError("Markdown document must start with YAML-style front matter")

    try:
        _, metadata_block, content = raw_text.split("---\n", maxsplit=2)
    except ValueError as exc:
        raise MetadataValidationError("Markdown front matter must be closed with ---") from exc

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(metadata_block.splitlines(), start=2):
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if ":" not in stripped_line:
            raise MetadataValidationError(f"Invalid metadata line {line_number}: {line}")
        key, value = stripped_line.split(":", maxsplit=1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, content
