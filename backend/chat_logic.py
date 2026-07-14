from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

CHROMA_PATH = "./chroma_db"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask_question(query: str) -> str:

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful document assistant. Answer the user's question based strictly on the provided context below.\n\nContext:\n{context}\n\nIf the answer is not in the context, simply say 'I cannot find the answer in the provided document.' Do not guess."),
        ("user", "{question}")
    ])


    llm = ChatOllama(model="llama3.2", temperature=0)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(query)
