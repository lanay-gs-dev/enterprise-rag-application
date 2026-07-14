
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


REQUIRED_METADATA_FIELDS = {
    "title",
    "source_id",
    "document_type",
    "department",
    "effective_date",
    "owner",
    "security_level",
}

ALLOWED_SECURITY_LEVELS = {"public", "internal", "confidential"}


class MetadataValidationError(ValueError):
    """Raised when a document is missing required or valid metadata."""


@dataclass(frozen=True)
class Document:
    source_path: str
    content: str
    metadata: dict[str, str]

    @property
    def source_id(self) -> str:
        return self.metadata["source_id"]

    @property
    def title(self) -> str:
        return self.metadata["title"]


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source_id: str
    text: str
    metadata: dict[str, str]
    start_char: int
    end_char: int


def validate_metadata(metadata: dict[str, str]) -> None:
    missing_fields = sorted(REQUIRED_METADATA_FIELDS - metadata.keys())
    if missing_fields:
        raise MetadataValidationError(f"Missing metadata fields: {', '.join(missing_fields)}")

    blank_fields = sorted(field for field in REQUIRED_METADATA_FIELDS if not metadata[field].strip())
    if blank_fields:
        raise MetadataValidationError(f"Blank metadata fields: {', '.join(blank_fields)}")

    security_level = metadata["security_level"].strip().lower()
    if security_level not in ALLOWED_SECURITY_LEVELS:
        allowed = ", ".join(sorted(ALLOWED_SECURITY_LEVELS))
        raise MetadataValidationError(
            f"Invalid security_level '{metadata['security_level']}'. Expected one of: {allowed}"
        )

    try:
        date.fromisoformat(metadata["effective_date"])
    except ValueError as exc:
        raise MetadataValidationError("effective_date must use YYYY-MM-DD format") from exc
