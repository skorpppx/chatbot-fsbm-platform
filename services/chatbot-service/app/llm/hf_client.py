"""
============================================================================
 Client HuggingFace Inference API (fallback gratuit)
============================================================================

POURQUOI HUGGINGFACE EN FALLBACK ?
  - Si Groq down ou rate limit atteint, on bascule sur HF
  - Tier gratuit : ~30 000 caracteres/mois (~1000 requetes courtes)
  - Modeles open source : Llama-3, Mistral, Falcon, etc.
  - URL : https://huggingface.co/inference-api

COMMENT OBTENIR LA CLE :
  1. Aller sur https://huggingface.co/settings/tokens
  2. Sign up gratuit
  3. "Create new token" → role: "Read"
  4. Copier le token qui commence par hf_...
  5. Mettre dans .env : HF_API_KEY=hf_...
============================================================================
"""

from __future__ import annotations
import os
import time
from typing import Optional

import httpx

from .groq_client import LLMResponse


HF_MODELS = {
    "llama":     "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistral":   "mistralai/Mistral-7B-Instruct-v0.3",
    "default":   "meta-llama/Meta-Llama-3-8B-Instruct",
}


class HFClient:
    """Client HuggingFace Inference API (fallback)."""

    BASE_URL = "https://api-inference.huggingface.co/models"

    def __init__(self, api_key: Optional[str] = None, model: str = "default"):
        self.api_key = api_key or os.environ.get("HF_API_KEY", "").strip()
        self.model = HF_MODELS.get(model, model)
        self.available = bool(self.api_key)

        if not self.available:
            print("[HF] HF_API_KEY non defini (fallback indispo)")

    def chat(
        self,
        system: str,
        user: str,
        history: Optional[list[dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> LLMResponse:
        """Genere une reponse via HF Inference API."""
        if not self.available:
            return LLMResponse(content="", model=self.model, provider="hf",
                              error="HF non configure")

        # Format de prompt Llama-3 (chat template officiel)
        prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system}<|eot_id|>"
        if history:
            for turn in history[-6:]:
                role = turn.get("role", "user")
                content = turn.get("content", "")
                prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>"
        prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|>"
        prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

        start = time.perf_counter()
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(
                    f"{self.BASE_URL}/{self.model}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "temperature": temperature,
                            "max_new_tokens": max_tokens,
                            "return_full_text": False,
                        },
                    },
                )
                latency_ms = int((time.perf_counter() - start) * 1000)
                resp.raise_for_status()
                data = resp.json()
                # HF renvoie [{"generated_text": "..."}]
                if isinstance(data, list) and data:
                    text = data[0].get("generated_text", "").strip()
                    return LLMResponse(content=text, model=self.model,
                                      provider="hf", latency_ms=latency_ms)
                return LLMResponse(content="", model=self.model, provider="hf",
                                  error=f"Reponse HF inattendue : {data}")
        except httpx.HTTPStatusError as e:
            return LLMResponse(content="", model=self.model, provider="hf",
                              error=f"HF HTTP {e.response.status_code}: {e.response.text[:120]}")
        except Exception as e:
            return LLMResponse(content="", model=self.model, provider="hf",
                              error=f"HF erreur : {e}")
