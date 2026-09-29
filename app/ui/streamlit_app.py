
import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_document_id" not in st.session_state:
    st.session_state.selected_document_id = None

if "selected_filename" not in st.session_state:
    st.session_state.selected_filename = None


# ============================================================
# HEADER
# ============================================================

st.title("📚 AI Research & Document Intelligence Agent")

st.caption(
    "Ask questions about your documents using "
    "Retrieval-Augmented Generation (RAG)."
)


# ============================================================
# GET DOCUMENTS
# ============================================================

try:
    response = requests.get(
        f"{API_URL}/documents/",
        timeout=10
    )

    if response.status_code == 200:
        documents = response.json()
    else:
        documents = []

except requests.RequestException:
    documents = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button(
            "Upload & Index",
            use_container_width=True
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:

                upload_response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files,
                    timeout=120
                )

                if upload_response.status_code == 200:

                    data = upload_response.json()

                    st.success(
                        "Document uploaded and indexed successfully."
                    )

                    st.write(
                        f"Pages: **{data['pages']}**"
                    )

                    st.write(
                        f"Chunks: **{data['chunks']}**"
                    )

                    st.write(
                        f"Vectors: **{data['vectors_stored']}**"
                    )

                    st.session_state.selected_document_id = (
                        data["document_id"]
                    )

                    st.session_state.selected_filename = (
                        data["filename"]
                    )

                    st.session_state.messages = []

                    st.rerun()

                elif upload_response.status_code == 409:

                    st.warning(
                        "This document has already been uploaded."
                    )

                else:

                    try:
                        detail = upload_response.json().get(
                            "detail",
                            "Upload failed."
                        )
                    except Exception:
                        detail = "Upload failed."

                    st.error(detail)

            except requests.RequestException:

                st.error(
                    "Could not connect to the FastAPI server."
                )

    st.divider()

    st.header("📚 Documents")


    # ========================================================
    # DOCUMENT LIST
    # ========================================================

    if documents:

        document_ids = [
            document["document_id"]
            for document in documents
        ]

        document_names = [
            document["filename"]
            for document in documents
        ]


        # ----------------------------------------------------
        # Ensure a valid selected document
        # ----------------------------------------------------

        if (
            st.session_state.selected_document_id is None
            or
            st.session_state.selected_document_id not in document_ids
        ):

            st.session_state.selected_document_id = (
                document_ids[0]
            )

            st.session_state.selected_filename = (
                document_names[0]
            )

            st.session_state.messages = []


        # ----------------------------------------------------
        # Find current selection
        # ----------------------------------------------------

        current_index = document_ids.index(
            st.session_state.selected_document_id
        )


        # ----------------------------------------------------
        # Select document
        # ----------------------------------------------------

        selected_filename = st.selectbox(
            "Select document",
            document_names,
            index=current_index
        )


        selected_document = next(
            document
            for document in documents
            if document["filename"] == selected_filename
        )

        selected_document_id = selected_document["document_id"]


        # ----------------------------------------------------
        # Detect document change
        # ----------------------------------------------------

        if (
            selected_document_id
            != st.session_state.selected_document_id
        ):

            st.session_state.selected_document_id = (
                selected_document_id
            )

            st.session_state.selected_filename = (
                selected_filename
            )

            st.session_state.messages = []

            st.rerun()


        document_id = st.session_state.selected_document_id
        selected_filename = st.session_state.selected_filename


        st.caption(
            f"ID: {document_id[:16]}..."
        )


        # ----------------------------------------------------
        # Delete document
        # ----------------------------------------------------

        st.divider()

        if st.button(
            "🗑️ Delete Document",
            use_container_width=True
        ):

            try:

                delete_response = requests.delete(
                    f"{API_URL}/documents/{document_id}",
                    timeout=30
                )

                if delete_response.status_code == 200:

                    st.session_state.messages = []

                    st.session_state.selected_document_id = None

                    st.session_state.selected_filename = None

                    st.success(
                        "Document deleted successfully."
                    )

                    st.rerun()

                else:

                    try:
                        detail = delete_response.json().get(
                            "detail",
                            "Unable to delete document."
                        )
                    except Exception:
                        detail = "Unable to delete document."

                    st.error(detail)

            except requests.RequestException:

                st.error(
                    "Could not connect to the API."
                )

    else:

        st.info(
            "Upload a PDF to get started."
        )


# ============================================================
# NO DOCUMENTS
# ============================================================

if not documents:

    st.info(
        "👈 Upload a PDF from the sidebar."
    )

    st.stop()


# ============================================================
# MAIN CHAT
# ============================================================

st.subheader(
    f"💬 Chat with {selected_filename}"
)


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("📑 Sources"):

                for index, source in enumerate(
                    message["sources"],
                    start=1
                ):

                    st.write(
                        f"**Source {index}**"
                    )

                    st.write(
                        f"Document: {source['source']}"
                    )

                    st.write(
                        f"Page: {source['page']}"
                    )

                    st.write(
                        f"Vector score: "
                        f"{source['vector_score']:.4f}"
                    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about this document..."
)


if question:

    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Conversation history
    # --------------------------------------------------------

    chat_history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in st.session_state.messages[:-1]
    ]


    # --------------------------------------------------------
    # Ask FastAPI
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching document and generating answer..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/documents/"
                    f"{document_id}/ask",

                    json={
                        "question": question,
                        "chat_history": chat_history
                    },

                    timeout=120
                )


                # ------------------------------------------------
                # SUCCESS
                # ------------------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    answer = data["answer"]

                    sources = data["sources"]

                    validation = data["citation_validation"]


                    st.markdown(answer)


                    # ------------------------------------------------
                    # Sources
                    # ------------------------------------------------

                    if sources:

                        with st.expander(
                            "📑 Sources"
                        ):

                            for index, source in enumerate(
                                sources,
                                start=1
                            ):

                                st.write(
                                    f"**Source {index}**"
                                )

                                st.write(
                                    f"Document: "
                                    f"{source['source']}"
                                )

                                st.write(
                                    f"Page: "
                                    f"{source['page']}"
                                )

                                st.write(
                                    f"Vector score: "
                                    f"{source['vector_score']:.4f}"
                                )


                    # ------------------------------------------------
                    # Citation validation
                    # ------------------------------------------------

                    if validation["all_valid"]:

                        st.success(
                            "✓ Citations validated"
                        )

                    else:

                        st.warning(
                            "⚠ Some citations could not be validated."
                        )


                    # ------------------------------------------------
                    # Save assistant response
                    # ------------------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )


                # ------------------------------------------------
                # API ERROR
                # ------------------------------------------------

                else:

                    try:

                        error_message = response.json().get(
                            "detail",
                            "Unable to generate answer."
                        )

                    except Exception:

                        error_message = (
                            "Unable to generate answer."
                        )

                    st.error(error_message)


            except requests.RequestException:

                st.error(
                    "Could not connect to the FastAPI server."
                )