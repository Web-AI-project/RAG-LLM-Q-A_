from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from config import MODEL_NAME
from services.vector_store import get_vectorstore

def get_llm():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512, truncation=True)
    return HuggingFacePipeline(pipeline=pipe)

llm = get_llm()
vectorstore = get_vectorstore()
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)
