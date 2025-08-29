# Yamaki WhatsApp Bot (PQR + Solicitudes)

## Description
Chatbot for Yamaki (import and distribution of professional audio, video and lighting equipment) with:
- Classification and responses via GPT-4o (Azure OpenAI)
- WhatsApp integration (Twilio)
- Quick FAQs (warranty, availability, distributors, trainings, quotes)
- Escalation to a human agent
- Database persistence (SQLAlchemy)

## Structure
- `app_yamaki.py`: Flask server (Twilio webhook)
- `yamaki_openai.py`: Classification/Response with GPT
- `yamaki_config.py`: Categories, brands, FAQs and triggers
- `yamaki_faq.py`: Quick FAQ responses
- `yamaki_db.py`: DB models and save logic
- `yamaki_escalation.py`: Email notification for escalations (optional)

## Environment Variables
```
# Twilio
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...

# Yamaki contacts (optional)
YAMAKI_CONTACT_EMAIL=contacto@yamaki.com.co
YAMAKI_SUPPORT_EMAIL=soporte@yamaki.com.co
YAMAKI_WHATSAPP=+57 000 0000000

# Database (optional to persist)
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db

# Demo mode (no DB writes)
DEMO_MODE=1

# SMTP Email (optional for escalation)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=bot@example.com
SMTP_PASS=...
YAMAKI_ESCALATION_EMAIL=soporte@yamaki.com.co
```

## Run locally
```
cd whatsapp-bot
python app_yamaki.py
ngrok http 5000
```
Configure Twilio webhook to `http://<host>/webhook`.

## Examples
- User: "Hola" → Bot: Yamaki welcome message
- User: "¿Tienen stock del Blackmagic ATEM Mini?" → Bot: availability FAQ + next steps
- User: "Necesito garantía para un PreSonus" → Bot: RMA guidance and requirements
- User: "Quiero cotización especial para 10 unidades" → Bot: escalate to human recognized
- User: "Capacitaciones de d&b audiotechnik" → Bot: training process and info request

## Notes
- If `DATABASE_URL` is not set, the bot works without persistence.
- If SMTP is not configured, escalation emails are not sent.
