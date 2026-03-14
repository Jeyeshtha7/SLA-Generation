import os
import json
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "chroma_db"
TICKET_FILE = "tickets.json"

def _get_retriever(collection_name: str):
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embed, collection_name=collection_name)
    return vectordb.as_retriever(search_kwargs={"k":5})

def load_chain(collection_name: str):
    retriever = _get_retriever(collection_name)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return ConversationalRetrievalChain.from_llm(llm, retriever)

def ask_question_and_maybe_act(collection_name: str, question: str):
    chain = load_chain(collection_name)
    result = chain({"question": question, "chat_history": []})
    answer = result.get("answer", "No answer produced.")

    ticket = None
    if any(kw in question.lower() for kw in ["create ticket","open ticket","raise ticket"]):
        ticket = _create_ticket(question, collection_name)
        answer += f"\n\nAction: Created ticket {ticket['id']} (simulated)."

    return {"answer": answer, "ticket_created": ticket is not None, "ticket": ticket}

def _create_ticket(summary: str, collection_name: str):
    ticket = {
        "id": int(os.path.getmtime(__file__)) + len(summary),
        "summary": summary,
        "collection": collection_name,
        "status": "OPEN"
    }
    tickets = []
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE,"r",encoding="utf-8") as f:
            try:
                tickets = json.load(f)
            except:
                tickets=[]
    tickets.append(ticket)
    with open(TICKET_FILE,"w",encoding="utf-8") as f:
        json.dump(tickets,f,indent=2)
    return ticket
