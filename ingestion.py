import os
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "chroma_db"

def _load_file(path: str):
    if path.lower().endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.lower().endswith(".txt"):
        loader = TextLoader(path)
    elif path.lower().endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(path)
    else:
        raise ValueError("Unsupported file type")
    return loader.load()

def ingest_document(path: str, collection_name: str = "default_sla"):
    docs = _load_file(path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = splitter.split_documents(docs)
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma.from_documents(
        texts,
        embedding=embed,
        persist_directory=CHROMA_DIR,
        collection_name=collection_name
    )
    vectordb.persist()
    return vectordb

def list_collections():
    if not os.path.exists(CHROMA_DIR):
        return []
    return [name for name in os.listdir(CHROMA_DIR) if os.path.isdir(os.path.join(CHROMA_DIR, name))]

def delete_collection(name: str):
    colpath = os.path.join(CHROMA_DIR, name)
    if os.path.exists(colpath):
        import shutil
        shutil.rmtree(colpath)
        return True
    return False
