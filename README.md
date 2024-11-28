# Chatbot con Búsqueda en Internet y Precios de Acciones

## 🤖 Descripción
Un chatbot interactivo de línea de comandos que responde preguntas basándose en:
- Contexto de conversación 
- Búsquedas en internet
- Precios actualizados de acciones usando `yfinance`
- Citación de fuentes

## ✨ Funcionalidades Principales
- **🔍 Búsqueda en Internet:** Integración con API de [Serper.dev](https://serper.dev/)
- **📈 Precios de Acciones:** Datos en tiempo real vía `yfinance`
- **🧠 Memoria Contextual:** Mantiene el hilo de la conversación
- **📚 Citación de Fuentes:** Referencias transparentes

## 🏗️ Estructura del Proyecto

```plaintext
CAP08_CHALLENGE/
├── chatbot.py           # Archivo principal del chatbot
├── requirements.txt     # Lista de dependencias del proyecto
├── .env                 # Archivo de configuración de variables de entorno
├── .gitignore           # Exclusiones para el control de versiones
└── README.md            # Documentación del proyecto
```

## 🚀 Configuración

### Requisitos Previos
- Python 3.8+
- API Keys:
  - [Serper.dev](https://serper.dev/)
  - [OpenAI](https://openai.com/)

### Instalación

1. **Crear entorno virtual:**
# Windows
```
python -m venv chatbot_env
chatbot_env\Scripts\activate
```
# Linux/Mac
```
python -m venv chatbot_env
source chatbot_env/bin/activate
```
2. **Instalar dependencias:**
pip install -r requirements.txt

3. **Configurar variables de entorno:**
Crear archivo `.env`:
```
SERPER_API_KEY=tu_clave_serper
OPENAI_API_KEY=tu_clave_openai
```
## 💡 Ejemplos de Uso

### Consulta de Acciones
Usuario: ¿Cuál es el precio de la acción de Apple?

Chatbot: El precio actual de Apple Inc. (AAPL) es $175.23
        [Fuente: Yahoo Finance]

### Búsqueda en Internet
Usuario: ¿Cómo plantar un árbol de manzanas?

Chatbot: Según GardeningKnowHow, el mejor momento es al inicio de primavera:

1. Elige un lugar soleado
2. Cava un hoyo profundo
3. Agrega compost orgánico

[Fuentes: 
- GardeningKnowHow.com
- WikiHow.com/plant-apple-trees]

### Consulta General
Usuario: ¿Qué es la inteligencia artificial?

Chatbot: La IA es el campo que desarrolla sistemas capaces de realizar tareas que requieren inteligencia humana, como:
- Aprendizaje automático
- Procesamiento de lenguaje natural
- Visión por computadora

## 📝 Notas
- Usa 'salir' para terminar la conversación
- Mantén tus API keys seguras
- Verifica la conexión a internet
