from __future__ import annotations

from dataclasses import dataclass

from enterprise_rag.models import Document, DocumentChunk


@dataclass(frozen=True)
class ChunkingConfig:
    max_chars: int = 900
    overlap_chars: int = 150

    def __post_init__(self) -> None:
        if self.max_chars <= 0:
            raise ValueError("max_chars must be positive")
        if self.overlap_chars < 0:
            raise ValueError("overlap_chars cannot be negative")
        if self.overlap_chars >= self.max_chars:
            raise ValueError("overlap_chars must be smaller than max_chars")


def chunk_document(document: Document, config: ChunkingConfig | None = None) -> list[DocumentChunk]:
    active_config = config or ChunkingConfig()
    paragraphs = _paragraphs_with_offsets(document.content)
    chunks: list[DocumentChunk] = []
    current_text = ""
    current_start = 0
    current_end = 0

    for paragraph, start, end in paragraphs:
        candidate = paragraph if not current_text else f"{current_text}\n\n{paragraph}"
        if current_text and len(candidate) > active_config.max_chars:
            chunks.append(_build_chunk(document, current_text, current_start, current_end, len(chunks)))
            current_text, current_start, current_end = _start_next_chunk(
                current_text, paragraph, start, end, active_config.overlap_chars
            )
        else:
            if not current_text:
                current_start = start
            current_text = candidate
            current_end = end

        while len(current_text) > active_config.max_chars:
            text_slice = current_text[: active_config.max_chars].rstrip()
            slice_end = current_start + len(text_slice)
            chunks.append(_build_chunk(document, text_slice, current_start, slice_end, len(chunks)))
            overlap = current_text[max(0, len(text_slice) - active_config.overlap_chars) :].lstrip()
            current_start = max(current_start, slice_end - len(overlap))
            current_text = overlap
            current_end = current_start + len(current_text)

    if current_text.strip():
        chunks.append(_build_chunk(document, current_text.strip(), current_start, current_end, len(chunks)))

    return chunks


def _build_chunk(
    document: Document,
    text: str,
    start_char: int,
    end_char: int,
    index: int,
) -> DocumentChunk:
    chunk_id = f"{document.source_id}::chunk-{index:04d}"
    return DocumentChunk(
        chunk_id=chunk_id,
        source_id=document.source_id,
        text=text,
        metadata=dict(document.metadata),
        start_char=start_char,
        end_char=end_char,
    )


def _paragraphs_with_offsets(text: str) -> list[tuple[str, int, int]]:
    paragraphs: list[tuple[str, int, int]] = []
    cursor = 0
    for raw_paragraph in text.split("\n\n"):
        start = text.find(raw_paragraph, cursor)
        end = start + len(raw_paragraph)
        paragraph = raw_paragraph.strip()
        if paragraph:
            stripped_start = start + len(raw_paragraph) - len(raw_paragraph.lstrip())
            stripped_end = end - (len(raw_paragraph) - len(raw_paragraph.rstrip()))
            paragraphs.append((paragraph, stripped_start, stripped_end))
        cursor = end + 2
    return paragraphs


def _start_next_chunk(
    previous_text: str,
    paragraph: str,
    paragraph_start: int,
    paragraph_end: int,
    overlap_chars: int,
) -> tuple[str, int, int]:
    if overlap_chars == 0:
        return paragraph, paragraph_start, paragraph_end

    overlap = previous_text[-overlap_chars:].lstrip()
    if not overlap:
        return paragraph, paragraph_start, paragraph_end

    next_text = f"{overlap}\n\n{paragraph}"
    next_start = max(0, paragraph_start - len(overlap) - 2)
    return next_text, next_start, paragraph_end
