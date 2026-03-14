# Load a PDF file
from langchain.document_loaders.unstructured import UnstructuredFileLoader

loader = UnstructuredFileLoader("example.pdf")
docs = loader.load()
print(docs[:2])  # prints first 2 loaded documents

# Load a text file
from langchain.document_loaders.text import TextLoader

loader_txt = TextLoader("example.txt")
docs_txt = loader_txt.load()
print(docs_txt[:2])  # prints first 2 loaded documents
