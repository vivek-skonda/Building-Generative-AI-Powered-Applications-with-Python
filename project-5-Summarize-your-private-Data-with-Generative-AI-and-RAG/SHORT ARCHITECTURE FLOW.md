User (browser)
   ↓
index.html + script.js
   ↓ sends message via fetch()
POST /process-message
   ↓
server.py → process_message_route()
   ↓ calls
worker.py → process_prompt()
   ↓ calls
conversation_retrieval_chain.invoke()
     ├─ llm_hub (WatsonxLLM) [init_llm()]
     ├─ embeddings (HuggingFaceEmbeddings) [init_llm()]
     ├─ vector DB (Chroma) [process_document()]
     ├─ retriever (db.as_retriever()) [process_document()]
     └─ RAG chain (RetrievalQA.from_chain_type()) [process_document()]
   ↓
LLM generates answer
   ↓
worker.py → chat_history.append()
   ↓
server.py → jsonify()
   ↓
Frontend displays answer
   ↓
User asks next question
   ↓
POST /process-message again
   ↓
worker.py → chat_history grows
