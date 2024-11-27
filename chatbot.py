import os
import requests
import yfinance as yf
import json
import openai
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from typing import List
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()
# Configuración de las API Keys


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Memoria para el historial de conversación
conversation_history = []

import yfinance as yf

import yfinance as yf
import unicodedata

def get_stock_price_from_input(user_input: str):
    # Función para normalizar texto eliminando acentos
    def normalize_text(text):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        ).lower()

    # Normalizar la entrada del usuario
    normalized_input = normalize_text(user_input)

    # Diccionario de nombres de empresas y sus símbolos
    company_symbols = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "amazon": "AMZN",
        "google": "GOOGL",
        "tesla": "TSLA",
        "facebook": "META",  # Meta Platforms
        "netflix": "NFLX"
    }
    
    # Verificar si el usuario está preguntando por el precio de una acción
    if "precio" in normalized_input and "accion" in normalized_input:
        # Buscar en el input el nombre de una empresa
        for company, symbol in company_symbols.items():
            if company in normalized_input:
                try:
                    stock = yf.Ticker(symbol)
                    price = stock.info.get("currentPrice")
                    if price:
                        return (f"El precio actual de la acción de {company.capitalize()} ({symbol}) es ${price:.2f}.\n"
                                f"Fuente: Yahoo Finance (https://finance.yahoo.com/quote/{symbol})")
                    else:
                        return f"No se pudo obtener el precio actual de la acción de {company.capitalize()}."
                except Exception as e:
                    return f"Error obteniendo el precio de la acción de {company.capitalize()}: {e}"
        return "No reconocí el nombre de la empresa. Por favor, especifica una empresa válida."
    else:
        return None  # No se detectó una consulta sobre acciones




# Función para realizar búsquedas en serper.dev
def search_google(query: str):
    url = "https://google.serper.dev/search"
    headers = {"Content-Type": "application/json", "X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("organic", [])
    else:
        print(f"Error en la búsqueda: {response.status_code}, {response.text}")
        return []

# Función para extraer texto de una URL
def extract_text_from_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs[:5]])
    except Exception as e:
        print(f"Error extrayendo texto de {url}: {e}")
        return ""

# Generar respuesta usando OpenAI en streaming
def generate_response(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Eres un asistente útil y conocedor."}] + prompt,
        stream=True
    )
    print("Chatbot:", end="", flush=True)
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            print(delta['content'], end="", flush=True)
    print("\n")

# Función principal del chatbot
def chatbot():
    print("Bienvenido al chatbot. Escribe 'salir' para terminar.")
    
    while True:
        user_input = input("Usuario: ").strip()
        if user_input.lower() == "salir":
            break

        conversation_history.append({"role": "user", "content": user_input})
        print("Chatbot: ** Realizando búsqueda en Internet... **")

        # Intentar obtener el precio de una acción
        stock_response = get_stock_price_from_input(user_input)
        if stock_response:
            print(stock_response)
            continue
        
        search_results = search_google(user_input)
        content_list = []
        sources = []
        
        for result in search_results[:5]:  # Limitar a los 5 primeros resultados
            url = result.get("link")
            title = result.get("title")
            content = extract_text_from_url(url)
            
            if content:
                content_list.append(f"Título: {title}\nContenido: {content[:200]}...")
                sources.append(f"{title}: {url}")

        if content_list:
            context = "\n\n".join(content_list)
            conversation_history.append({"role": "assistant", "content": context})
        
        prompt = conversation_history + [{"role": "system", "content": "Utiliza los datos anteriores para responder la pregunta."}]
        generate_response(prompt)
        
        # Mostrar referencias
        print("\nReferencias:")
        for source in sources:
            print("-", source)

if __name__ == "__main__":
    chatbot()
