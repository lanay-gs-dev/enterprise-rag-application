from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.pipeline import RagRuntime, answer_question, build_sample_index


@st.cache_resource(show_spinner="Building local document index...")
def build_demo_index() -> RagRuntime:
    return build_sample_index(ROOT / "data" / "sample")


def main() -> None:
    st.set_page_config(page_title="Enterprise RAG Demo", layout="wide")
    st.title("Enterprise RAG Demo")
    st.caption("Ask a question against the sample internal document set.")

    with st.sidebar:
        st.write("Sample questions")
        st.code("Is multi-factor authentication required?")
        st.code("Can employees share passwords in chat?")
        st.code("Do vacation days roll over?")

    runtime = build_demo_index()
    st.success(f"Indexed {runtime.chunk_count} chunks from sample documents.")

    question = st.text_input(
        "Question",
        value="Is multi-factor authentication required?",
        placeholder="Ask about the sample company documents...",
    )

    if st.button("Ask", type="primary") and question.strip():
        answer, retrieved = answer_question(question, runtime, k=2)

        st.subheader("Answer")
        if answer.refused:
            st.warning(answer.text)
        else:
            st.write(answer.text)

        st.subheader("Citations")
        if answer.citations:
            for citation in answer.citations:
                st.code(citation)
        else:
            st.write("No citations available.")

        with st.expander("Retrieved evidence"):
            for chunk in retrieved:
                st.markdown(f"**Rank {chunk.rank}: `{chunk.chunk_id}`**")
                st.write(f"Score: {chunk.score:.3f}")
                st.write(chunk.text)


if __name__ == "__main__":
    main()
