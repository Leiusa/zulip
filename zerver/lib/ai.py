import logging
from typing import List, Optional

import requests
from django.conf import settings
from django.utils.html import escape

logger = logging.getLogger(__name__)

def generate_message_recap(messages: List[str], message_ids: List[int], max_tokens: int = 800) -> str:
    """
    Generate a concise HTML recap for the provided message texts, in the order of message_ids.
    Returns a (mostly) safe HTML string.
    """
    if not messages:
        return "<p>(no messages)</p>"

    # Config
    api_key: Optional[str] = getattr(settings, "LLM_API_KEY", None)
    provider: str = getattr(settings, "LLM_PROVIDER", "openai")
    model: str = getattr(settings, "LLM_MODEL", "gpt-4o-mini")

    # Bound prompt size (avoid huge prompts)
    labelled: List[str] = []
    for mid, text in zip(message_ids, messages):
        labelled.append(text[:3000])
    labelled = labelled[:200]

    if not api_key:
        logger.warning("LLM_API_KEY not configured; returning fallback recap")
        joined = "\n\n---\n\n".join(labelled[:10])
        # fallback: show first N messages
        return "<p><strong>Recap (fallback):</strong></p><pre>{}</pre>".format(escape(joined[:4000]))

    prompt_system = (
        "You are a concise assistant.\n"
        "Return ONLY valid HTML.\n"
        "DO NOT use Markdown.\n"
        "DO NOT wrap output in ``` or ```html.\n"
        "DO NOT include message IDs like MSG 12.\n"
        "Use <p>, <ul>, <li>, <strong> only.\n"
    )
    prompt_user = "Messages:\n\n" + "\n\n---\n\n".join(labelled)

    try:
        if provider != "openai":
            raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        logger.warning("LLM status=%s", resp.status_code)
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            return "<p>(empty recap)</p>"
        logger.warning("LLM content len=%s head=%r", len(content), content[:200])

    except Exception:
        logger.exception("LLM request failed; returning fallback recap")
        joined = "\n\n---\n\n".join(labelled[:10])
        return "<p><strong>Recap (fallback):</strong></p><pre>{}</pre>".format(escape(joined[:4000]))

    import bleach

    ALLOWED_TAGS = [
        "div","p","br","strong","em","ul","ol","li","a","code","pre","blockquote",
        "h1","h2","h3","h4","h5","h6","span"
    ]
    ALLOWED_ATTRS = {
        "a": ["href", "title", "target", "rel"],
        "span": ["class"],
        "div": ["class"],
    }
    
    clean = bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    def strip_code_fence(s: str) -> str:
        s = s.strip()
        if s.startswith("```"):
            s = s.split("\n", 1)[1]
            s = s.rsplit("```", 1)[0]
        return s.strip()
    
    content = strip_code_fence(content)
    return f"<div class='ai-recap'>{clean}</div>"