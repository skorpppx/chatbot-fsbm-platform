"""
Sous-package LLM (Large Language Model) du chatbot-service.

Composants :
    - groq_client.py  : client pour l'API Groq (heberge LLaMA 3.x gratuit)
    - hf_client.py    : client pour HuggingFace Inference API (fallback)
    - rag.py          : Retrieval-Augmented Generation (TF-IDF + LLM)
    - llm_service.py  : orchestrateur principal avec fallback automatique
"""
