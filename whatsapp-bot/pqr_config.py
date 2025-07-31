# Configuración del Sistema PQR para Erco Energía S.A.S.

# Categorías principales de PQR
CATEGORIAS_PQR = {
    "BIENVENIDA": {
        "name": "Bienvenida",
        "subcategorias": [
            "Saludo inicial",
            "Presentación",
            "Solicitud de ayuda general",
            "Buenos días/tardes/noches",
            "Necesito ayuda"
        ],
        "tiempo_respuesta": "Inmediato"
    },
    "FACTURACION": {
        "name": "Facturación",
        "subcategorias": [
            "Factura de energía solar",
            "Consulta de generación",
            "Métodos de pago",
            "Tarifas y ahorros",
            "Contratos PPA y leasing"
        ],
        "tiempo_respuesta": "2-5 días hábiles"
    },
    "SERVICIO_TECNICO": {
        "name": "Servicio técnico",
        "subcategorias": [
            "Falla en paneles solares",
            "Mantenimiento del sistema",
            "Instalación nueva",
            "Revisión técnica",
            "Monitoreo ENRG",
            "Eficiencia energética"
        ],
        "tiempo_respuesta": "24-48 horas"
    },
    "ATENCION_CLIENTE": {
        "name": "Atención al cliente",
        "subcategorias": [
            "Información sobre energía solar",
            "Cambio de titular",
            "Certificados y garantías",
            "Horarios de atención",
            "Canales de atención"
        ],
        "tiempo_respuesta": "1-3 días hábiles"
    },
    "ENERGIA_SOLAR": {
        "name": "Energía Solar",
        "subcategorias": [
            "Cotización de paneles",
            "Instalación residencial",
            "Instalación comercial",
            "Ampliación del sistema",
            "Movilidad eléctrica",
            "Almacenamiento de energía"
        ],
        "tiempo_respuesta": "3-5 días hábiles"
    }
}

# Palabras clave para clasificación automática
PALABRAS_CLAVE = {
    "BIENVENIDA": ["hola", "hello", "hi", "buenos días", "buenas tardes", "buenas noches", "buenas", "saludos", "me presento", "necesito ayuda", "ayuda", "qué tal", "inicio", "empezar"],
    "FACTURACION": ["factura", "cobro", "pago", "valor", "cuenta", "tarifa", "ahorro", "generación", "recibo", "ppa", "leasing"],
    "SERVICIO_TECNICO": ["falla", "daño", "paneles", "solar", "medidor", "instalación", "técnico", "reparación", "mantenimiento", "enrg", "monitoreo"],
    "ENERGIA_SOLAR": ["paneles", "solar", "cotización", "instalación", "residencial", "comercial", "ampliación", "movilidad eléctrica", "almacenamiento", "baterías"],
    "ATENCION_CLIENTE": ["información", "certificado", "constancia", "titular", "horario", "contacto", "garantía"]
}

# Canales de atención Erco Energía
CANALES_ATENCION = {
    "whatsapp": "+57 601 6659652 (opción 3)",
    "email": "soporte@erco.energy", 
    "web": "www.er-co.com",
    "plataforma": "App ENRG - Monitoreo en tiempo real",
    "oficinas": "Medellín y Sabaneta, Antioquia - Lunes a Viernes 8:00 AM - 5:00 PM",
    "emergencias": "+57 601 6659652 (24 horas)"
}

# Plantilla de respuesta de emergencia
RESPUESTA_EMERGENCIA = """🚨 EMERGENCIA - PRIORIDAD MÁXIMA

📞 Llama YA: +57 601 6659652 (24h)
⚡ Técnicos solares en camino

Mantente seguro y alejado de paneles dañados.

- Ercobot, Erco Energía"""

# Palabras clave de emergencia
EMERGENCIAS = ["electrocutado", "cable caído", "explosión", "incendio", "humo", "chispas", "peligro", "urgente", "emergencia", "panel roto", "inversor dañado"] 