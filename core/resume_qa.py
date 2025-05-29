# core/resume_qa.py (LangChain 2024+ compliant)

import os
import fitz
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEndpoint

# Replace this with your Hugging Face token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_xxxxxxxx"

def load_resume_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def qa_on_resume(resume_text, question):
    # Text chunking
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(resume_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Embeddings
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embedder)

    # LLM - flan-t5-xl or another light endpoint
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        task="text-generation",
        temperature=0.5,
        max_new_tokens=256,
        )



    # Retrieval-based QA
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(),
        chain_type="stuff",
        return_source_documents=False,
    )

    result = qa.invoke({"query": question})
    return result['result']

def main():
    resume_path = input("📁 Enter path to your resume PDF: ").strip()
    if not os.path.exists(resume_path):
        print("❌ File not found.")
        return

    question = input("📝 Ask something about your resume: ").strip()
    print("⏳ Thinking...")

    resume_text = load_resume_text(resume_path)
    answer = qa_on_resume(resume_text, question)
    print("\n🤖 Abeera Says:\n", answer)

if __name__ == "__main__":
    main()
