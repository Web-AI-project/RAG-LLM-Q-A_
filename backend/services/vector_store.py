from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from config import CHROMA_DIR, EMBEDDING_MODEL
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
import os

def load_documents():
    loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma.from_documents(
        documents=docs,
        persist_directory=CHROMA_DIR,
        collection_name="pdf_docs",
        embedding=embedding
    )
    vectorstore.persist()
    return vectorstore

def get_vectorstore():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=CHROMA_DIR,
        collection_name="pdf_docs",
        embedding_function=embedding
    )
