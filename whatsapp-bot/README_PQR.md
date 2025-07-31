# Sistema PQR WhatsApp Bot - Empresa de Energía ⚡

## 🚀 Descripción del Sistema

Este bot inteligente de WhatsApp está diseñado específicamente para empresas de energía para manejar **PQR (Peticiones, Quejas y Recursos)** de manera automatizada y profesional.

### ✨ Características Principales

- **Clasificación Automática**: Identifica automáticamente el tipo de consulta (Petición/Queja/Recurso/Solicitud)
- **Generación de ID Único**: Cada consulta recibe un ID de seguimiento único
- **Respuestas Personalizadas**: Utiliza GPT-4 con prompts específicos para empresas de energía
- **Detección de Emergencias**: Identifica y prioriza situaciones de emergencia
- **Categorización Inteligente**: Clasifica consultas por categorías (Facturación, Servicio Técnico, etc.)

## 🛠️ Funcionamiento del Sistema

### 1. **Recepción de Mensajes**
- El usuario envía un mensaje por WhatsApp
- El bot detecta si es una emergencia, saludo o consulta normal

### 2. **Clasificación Inteligente**
```python
# El sistema clasifica automáticamente:
{
    "tipo_pqr": "Queja/Petición/Recurso/Solicitud",
    "asunto": "Resumen del problema",
    "categoria": "Facturación/Servicio técnico/etc.",
    "subcategoria": "Detalle específico",
    "descripcion": "Descripción completa"
}
```

### 3. **Generación de Respuesta**
- **ID único**: `PQR-20240115-A1B2C3D4`
- **Respuesta empática** y profesional
- **Tiempos de resolución** estimados
- **Canales alternativos** de contacto

## 📋 Categorías de PQR

### 🧾 Facturación
- Facturas altas o incorrectas
- Consultas de consumo
- Métodos de pago
- Subsidios y tarifas
- **Tiempo respuesta**: 2-5 días hábiles

### 🔧 Servicio Técnico  
- Fallas en el suministro
- Daños en medidores
- Instalaciones nuevas
- Revisiones técnicas
- **Tiempo respuesta**: 24-48 horas

### 📞 Atención al Cliente
- Información general
- Cambio de titular
- Certificados y constancias
- **Tiempo respuesta**: 1-3 días hábiles

### ⚡ Suministro
- Suspensión del servicio
- Reconexiones
- Nuevas acometidas
- **Tiempo respuesta**: 3-7 días hábiles

## 🚨 Sistema de Emergencias

El bot detecta automáticamente emergencias con palabras clave como:
- `electrocutado`, `cable caído`, `explosión`
- `incendio`, `humo`, `chispas`
- `peligro`, `urgente`, `emergencia`

**Respuesta inmediata** con:
- 📞 Línea de emergencias: 123
- ⚡ Reporte a técnicos de campo
- 🚨 Prioridad máxima

## 💬 Ejemplos de Uso

### Usuario dice: *"Hola"*
```
¡Bienvenido al Sistema de Atención al Cliente de Energía! 💡

Soy su asistente virtual para atender sus:
• ⚡ Consultas sobre facturación
• 🔧 Reportes de fallas técnicas  
• 📋 Solicitudes de servicio
• 📞 Quejas y reclamos

¿En qué puedo ayudarle hoy?
```

### Usuario dice: *"Mi factura llegó muy alta este mes"*
```
Estimado Usuario 1234,

He registrado su queja sobre facturación con el ID: PQR-20240115-A1B2C3D4

Comprendo su preocupación por el incremento en su factura de energía...

[Respuesta completa y profesional generada por GPT-4]

Canales adicionales:
📞 018000-ENERGIA
✉️ atencion@empresa-energia.com
```

### Usuario dice: *"Hay un cable caído en mi calle"*
```
🚨 EMERGENCIA DETECTADA 🚨

Su solicitud ha sido clasificada como EMERGENCIA...

📞 Línea de Emergencias: 123 (24 horas)
⚡ Reporte inmediato a técnicos de campo
```

## ⚙️ Configuración Técnica

### Variables de Entorno Requeridas
```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
AZURE_OPENAI_ENDPOINT=tu_azure_endpoint
AZURE_OPENAI_API_KEY=tu_api_key
```

### Archivos del Sistema
- `app.py` - Servidor Flask principal
- `openai_client.py` - Integración con GPT-4
- `pqr_config.py` - Configuraciones y categorías
- `README_PQR.md` - Esta documentación

### Instalación
```bash
pip install -r requirements.txt
python app.py
```

## 📊 Ventajas del Sistema

1. **Eficiencia**: Respuestas 24/7 automatizadas
2. **Profesionalidad**: Respuestas empáticas y estructuradas
3. **Trazabilidad**: Cada consulta tiene ID único
4. **Escalabilidad**: Maneja múltiples conversaciones simultáneas
5. **Inteligencia**: Clasificación automática por IA
6. **Seguridad**: Detección proactiva de emergencias

## 🎯 Casos de Uso Ideales

- **Empresas de Energía Eléctrica**
- **Empresas de Gas Natural** 
- **Cooperativas de Energía**
- **Distribuidoras Eléctricas**
- **Empresas de Servicios Públicos**

---
*Desarrollado con ❤️ para mejorar la atención al cliente en el sector energético* 