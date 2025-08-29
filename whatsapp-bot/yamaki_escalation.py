"""
Notificaciones de escalamiento a un agente humano (vía email SMTP si está configurado).
"""

import os
import smtplib
from email.mime.text import MIMEText
from typing import Optional, Dict, Any


def notify_human_escalation(payload: Dict[str, Any]) -> Optional[str]:
    """Envía un correo de escalamiento si hay configuración SMTP.

    Variables de entorno: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, YAMAKI_ESCALATION_EMAIL
    Devuelve un string con resultado o None si no hay configuración.
    """
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "0") or 0)
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    to_email = os.getenv("YAMAKI_ESCALATION_EMAIL")

    if not (host and port and user and password and to_email):
        return None

    subject = f"[Yamaki Bot] Escalamiento - ID {payload.get('id', '')}"
    body = (
        f"Se ha solicitado escalamiento a humano.\n\n"
        f"ID: {payload.get('id')}\n"
        f"Usuario: {payload.get('usuario')}\n"
        f"Mensaje: {payload.get('mensaje')}\n"
        f"Clasificación: {payload.get('clasificacion')}\n"
        f"Categoría: {payload.get('categoria')}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [to_email], msg.as_string())
        return "Email de escalamiento enviado"
    except Exception as e:
        return f"Fallo envío de email de escalamiento: {e}"


