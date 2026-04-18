# Project‑4 Architecture: Generative AI Powered Meeting Assistant

## Full Flow (Detailed)

USER UPLOADS LECTURE AUDIO  
        ↓  
GRADIO UI RECEIVES AUDIO FILE  
        ↓  
GRADIO PASSES AUDIO FILE PATH TO WHISPER  
        ↓  
WHISPER (OpenAI) PROCESSES AUDIO  
        ↓  
WHISPER TRANSCRIBES AUDIO → RAW TEXT TRANSCRIPT  
        ↓  
TRANSCRIPT RETURNED TO PYTHON BACKEND  
        ↓  
PYTHON INSERTS TRANSCRIPT INTO PROMPT TEMPLATE  
        ↓  
PYTHON SENDS FORMATTED PROMPT → IBM WATSONX LLAMA‑3  
        ↓  
IBM WATSONX LLAMA‑3 PROCESSES THE TRANSCRIPT  
        ↓  
LLAMA‑3 GENERATES:  
    - SUMMARY  
    - KEY POINTS  
    - INSIGHTS (IF PROMPTED)  
        ↓  
SUMMARY + KEY POINTS RETURNED TO PYTHON  
        ↓  
PYTHON SENDS RESULTS BACK TO GRADIO  
        ↓  
GRADIO DISPLAYS TO USER:  
    - FULL TRANSCRIPT  
    - SUMMARY  
    - KEY POINTS  

---

## Ultra‑Short Version

Audio → Gradio → Whisper → Transcript → WatsonX Llama‑3 → Summary → Gradio UI
