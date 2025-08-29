"""
Configuración del Sistema Yamaki para gestión de solicitudes y PQRs.

Este módulo define categorías, palabras clave, marcas, FAQs y disparadores
de escalamiento para adaptar el chatbot al negocio de Yamaki.
"""

from typing import List, Dict


# Categorías principales
CATEGORIAS_YAMAKI: Dict[str, Dict] = {
    "BIENVENIDA": {
        "name": "Bienvenida",
        "subcategorias": [
            "Saludo inicial",
            "Presentación",
            "Solicitud de ayuda general",
            "Buenos días/tardes/noches",
            "Necesito ayuda",
        ],
        "tiempo_respuesta": "Inmediato",
    },
    "PRODUCTOS": {
        "name": "Productos",
        "subcategorias": [
            "Disponibilidad",
            "Compatibilidad",
            "Características",
            "Modelos",
            "Accesorios",
        ],
        "tiempo_respuesta": "1-3 días hábiles",
    },
    "GARANTIAS": {
        "name": "Garantías",
        "subcategorias": [
            "Términos y condiciones",
            "Proceso de garantía",
            "Tiempo de respuesta",
            "Estado de garantía",
        ],
        "tiempo_respuesta": "2-5 días hábiles",
    },
    "SOPORTE_TECNICO": {
        "name": "Soporte técnico",
        "subcategorias": [
            "Diagnóstico",
            "Firmware/Drivers",
            "Instalación",
            "Configuración avanzada",
            "RMA/Servicio",
        ],
        "tiempo_respuesta": "24-48 horas",
    },
    "DISTRIBUIDORES": {
        "name": "Distribuidores autorizados",
        "subcategorias": [
            "Ubicaciones",
            "Cobertura",
            "Contacto",
        ],
        "tiempo_respuesta": "1-3 días hábiles",
    },
    "COTIZACIONES": {
        "name": "Cotizaciones",
        "subcategorias": [
            "Solicitud de precio",
            "Tiempo de entrega",
            "Opciones de pago",
            "Proyectos especiales",
        ],
        "tiempo_respuesta": "1-3 días hábiles",
    },
    "CAPACITACIONES": {
        "name": "Capacitaciones",
        "subcategorias": [
            "Calendario",
            "Contenido",
            "Certificaciones",
            "Inscripción",
        ],
        "tiempo_respuesta": "3-5 días hábiles",
    },
}


# Marcas distribuidas (incompleta; se puede extender)
MARCAS: List[str] = [
    "blackmagic",
    "d&b audiotechnik",
    "muxlab",
    "presonus",
    "fujifilm",
    "kino flo",
    "e-image",
]


# Palabras clave por categoría
PALABRAS_CLAVE_YAMAKI: Dict[str, List[str]] = {
    "BIENVENIDA": [
        "hola",
        "hello",
        "hi",
        "buenos días",
        "buenas tardes",
        "buenas noches",
        "buenas",
        "saludos",
        "necesito ayuda",
        "ayuda",
        "qué tal",
        "inicio",
        "empezar",
    ],
    "PRODUCTOS": [
        "producto",
        "disponibilidad",
        "stock",
        "característica",
        "modelo",
        "compatibilidad",
        "accesorio",
        "precio",
        "especificación",
    ]
    + MARCAS,
    "GARANTIAS": [
        "garantía",
        "rma",
        "devolución",
        "falla",
        "defecto",
        "soporte de garantía",
    ],
    "SOPORTE_TECNICO": [
        "soporte",
        "técnico",
        "configuración",
        "instalación",
        "firmware",
        "driver",
        "actualización",
        "diagnóstico",
        "no funciona",
    ],
    "DISTRIBUIDORES": [
        "distribuidor",
        "autorizado",
        "tienda",
        "punto de venta",
        "dónde comprar",
        "ubicación",
        "ciudad",
        "región",
    ],
    "COTIZACIONES": [
        "cotización",
        "precio",
        "descuento",
        "propuesta",
        "tiempo de entrega",
        "plazo",
    ],
    "CAPACITACIONES": [
        "capacitación",
        "curso",
        "entrenamiento",
        "certificación",
        "agenda",
        "calendario",
        "inscripción",
    ],
}


# Disparadores de escalamiento a agente humano
ESCALAMIENTO: List[str] = [
    "hablar con un asesor",
    "asesor",
    "soporte técnico avanzado",
    "cotización especial",
    "prioridad",
    "urgente",
    "llamar",
    "agente humano",
]


# FAQs base (plantillas). Consumo recomendado vía faq.answer_faq_or_none
FAQS: List[Dict] = [
    {
        "name": "garantias_basico",
        "keywords": ["garantía", "rma", "defecto", "falla"],
        "answer": (
            "Sobre garantías: Yamaki gestiona RMA para productos de marcas como Blackmagic, d&b audiotechnik, "
            "MuxLab, PreSonus, Fujifilm, Kino Flo y E-Image según términos del fabricante. "
            "Comparte marca, modelo, número de serie y factura para iniciar el proceso."
        ),
    },
    {
        "name": "disponibilidad_productos",
        "keywords": ["disponibilidad", "stock", "producto", "modelo"],
        "answer": (
            "Disponibilidad de productos: indícanos marca y modelo (por ejemplo, Blackmagic ATEM Mini) y ciudad. "
            "Te confirmamos stock y tiempos de entrega. También trabajamos con distribuidores autorizados."
        ),
    },
    {
        "name": "distribuidores_autorizados",
        "keywords": ["distribuidor", "autorizado", "dónde comprar", "punto de venta", "ubicación"],
        "answer": (
            "Distribuidores: cuéntanos tu ciudad/país y la marca de interés. "
            "Te compartimos el contacto del distribuidor autorizado más cercano."
        ),
    },
    {
        "name": "capacitaciones_programa",
        "keywords": ["capacitación", "curso", "entrenamiento", "certificación", "calendario"],
        "answer": (
            "Capacitaciones: ofrecemos sesiones sobre productos y soluciones de nuestras marcas. "
            "Compártenos el tema o marca y te enviaremos calendario y requisitos de inscripción."
        ),
    },
    {
        "name": "cotizaciones_tiempos",
        "keywords": ["cotización", "precio", "tiempo de entrega", "plazo", "descuento"],
        "answer": (
            "Cotizaciones: indícanos marca, modelo, cantidad y ciudad de entrega. "
            "Te enviaremos una propuesta con precios, disponibilidad y tiempos estimados."
        ),
    },
]


# Canales de contacto (pueden complementarse con variables de entorno en app)
CANALES_ATENCION_YAMAKI = {
    "whatsapp": "+57 000 0000000",  # Placeholder; configurar en variables de entorno
    "email": "contacto@yamaki.com.co",
    "soporte": "soporte@yamaki.com.co",
    "web": "https://www.yamaki.com.co/",
}


