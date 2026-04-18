┌──────────────────────────────────────────────────────────────────────────────┐
│                                USER (BROWSER)                                │
│                          Types a question in UI                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (index.html + script.js)                    │
│                                                                              │
│  FILES:                                                                      │
│     • templates/index.html                                                   │
│     • static/script.js                                                       │
│                                                                              │
│  - Captures user input                                                       │
│  - Sends POST /process-message                                               │
│  - Receives JSON { botResponse }                                             │
│  - Updates chat window                                                       │
│                                                                              │
│  JavaScript:                                                                 │
│     fetch("/process-message", {                                              │
│        method: "POST",                                                       │
│        body: JSON.stringify({ userMessage })                                 │
│     })                                                                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                             BACKEND (server.py)                              │
│                                                                              │
│  FILE: server.py                                                             │
│                                                                              │
│  Route: /process-message                                                     │
│     def process_message_route():                                             │
│         userMessage = request.json["userMessage"]                            │
│         botResponse = worker.process_prompt(userMessage)                     │
│         return jsonify({ "botResponse": botResponse })                       │
│                                                                              │
│  Route: /process-document                                                    │
│     def process_document_route():                                            │
│         worker.process_document(pdf_path)                                    │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                               WORKER ENGINE (worker.py)                      │
│                                                                              │
│  FILE: worker.py                                                             │
│                                                                              │
│  GLOBALS:                                                                    │
│     llm_hub → WatsonX Llama model (LangChain LLM wrapper)                    │
│     embeddings → HuggingFaceEmbeddings (LangChain)                           │
│     conversation_retrieval_chain → RetrievalQA (LangChain)                   │
│     chat_history → list of (question, answer)                                │
│                                                                              │
│  FUNCTIONS:                                                                  │
│                                                                              │
│  init_llm():                                                                 │
│     - Creates WatsonX LLM (llm_hub)                                          │
│     - Creates HuggingFace embeddings                                         │
│                                                                              │
│  process_document(path):                                                     │
│     - loader = PyPDFLoader(path)                                             │
│     - documents = loader.load()                                              │
│     - splitter = RecursiveCharacterTextSplitter()                            │
│     - chunks = splitter.split_documents(documents)                           │
│     - embeddings = HuggingFaceEmbeddings()                                   │
│     - db = Chroma.from_documents(chunks, embeddings)                         │
│     - retriever = db.as_retriever(search_type="mmr")                         │
│     - conversation_retrieval_chain = RetrievalQA.from_chain_type(            │
│           llm=llm_hub, retriever=retriever                                   │
│       )                                                                       │
│                                                                              │
│  process_prompt(prompt):                                                     │
│     - output = conversation_retrieval_chain.invoke({                         │
│           "question": prompt,                                                │
│           "chat_history": chat_history                                       │
│       })                                                                      │
│     - chat_history.append((prompt, output))                                  │
│     - return output                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              RAG PIPELINE (LangChain)                        │
│                                                                              │
│  LangChain Components:                                                       │
│     • PyPDFLoader                                                            │
│     • RecursiveCharacterTextSplitter                                         │
│     • HuggingFaceEmbeddings                                                  │
│     • Chroma (Vector DB)                                                     │
│     • Retriever (MMR search)                                                 │
│     • RetrievalQA chain                                                      │
│     • LLM wrapper (WatsonxLLM)                                               │
│                                                                              │
│  RetrievalQA.invoke():                                                       │
│     1. Convert question → embedding                                          │
│     2. Search vector DB (Chroma) for relevant chunks                         │
│     3. Pass chunks + question + chat_history to LLM                          │
│     4. LLM generates grounded answer                                         │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           LLM (WatsonX Llama Model)                          │
│                                                                              │
│  - Receives: question + retrieved chunks + chat history                      │
│  - Synthesizes final answer                                                  │
│  - Returns answer to RAG chain                                               │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           BACK TO WORKER (worker.py)                         │
│                                                                              │
│  - process_prompt() receives answer                                           │
│  - chat_history.append((prompt, answer))                                     │
│  - Returns answer to Flask                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           BACK TO FLASK (server.py)                          │
│                                                                              │
│  - Returns JSON { botResponse }                                              │
└──────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND DISPLAYS ANSWER                             │
│                                                                              │
│  - Chat window updates                                                       │
│  - User asks next question                                                   │
│  - Loop repeats                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
