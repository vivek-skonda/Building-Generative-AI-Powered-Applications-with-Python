User
 ↓
index.html + script.js → fetch("/process-message")
 ↓
server.py → process_message_route()
 ↓
worker.py → process_prompt()
 ↓
conversation_retrieval_chain.invoke()
     ├─ llm_hub (WatsonxLLM) [init_llm()]
     ├─ embeddings (HuggingFaceEmbeddings) [init_llm()]
     ├─ vector DB (Chroma) [process_document()]
     ├─ retriever (db.as_retriever()) [process_document()]
     └─ RAG chain (RetrievalQA.from_chain_type()) [process_document()]
 ↓
LLM answer
 ↓
worker.py → chat_history.append()
 ↓
server.py → jsonify()
 ↓
Frontend displays answer
 ↓
Loop repeats
