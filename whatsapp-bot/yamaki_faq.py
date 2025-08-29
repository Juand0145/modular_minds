"""
FAQs y lógica de respuesta corta para Yamaki.
"""

from typing import Optional

from yamaki_config import FAQS


def answer_faq_or_none(message: str) -> Optional[str]:
    """Devuelve una respuesta de FAQ si el mensaje coincide con palabras clave.

    Estrategia simple: si alguna palabra clave de una FAQ aparece en el mensaje,
    se devuelve su respuesta. En caso contrario, None.
    """
    if not message:
        return None

    lower_message = message.lower()

    for faq in FAQS:
        for keyword in faq.get("keywords", []):
            if keyword.lower() in lower_message:
                return faq.get("answer")

    return None


