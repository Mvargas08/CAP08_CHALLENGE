import unittest
from unittest.mock import patch, Mock
import requests

# Función a probar
def search_google(query: str):
    url = "https://google.serper.dev/search"
    headers = {"Content-Type": "application/json", "X-API-KEY": "dummy_api_key"}
    payload = {"q": query}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("organic", [])
    else:
        print(f"Error en la búsqueda: {response.status_code}, {response.text}")
        return []

class TestSearchGoogle(unittest.TestCase):

    @patch("requests.post")
    def test_search_google_success(self, mock_post):
        # Simular una respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organic": [
                {"title": "Result 1", "link": "http://example.com/1"},
                {"title": "Result 2", "link": "http://example.com/2"}
            ]
        }
        mock_post.return_value = mock_response

        # Llamar a la función
        results = search_google("Python programming")
        
        # Verificar resultados
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Result 1")
        self.assertEqual(results[0]["link"], "http://example.com/1")

    @patch("requests.post")
    def test_search_google_error(self, mock_post):
        # Simular una respuesta con error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        # Llamar a la función
        results = search_google("Python programming")
        
        # Verificar que se maneja el error
        self.assertEqual(results, [])

# Función a probar
def extract_text_from_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs[:5]])
    except Exception as e:
        print(f"Error extrayendo texto de {url}: {e}")
        return ""

class TestExtractTextFromURL(unittest.TestCase):

    @patch("requests.get")
    def test_extract_text_from_url_success(self, mock_get):
        # Simular una respuesta exitosa con contenido HTML
        mock_response = Mock()
        mock_response.content = b"<html><body><p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p><p>Fourth paragraph.</p><p>Fifth paragraph.</p></body></html>"
        mock_get.return_value = mock_response

        # Llamar a la función
        text = extract_text_from_url("http://example.com")

        # Verificar que se extraen correctamente los primeros 5 párrafos
        self.assertEqual(text, "First paragraph. Second paragraph. Third paragraph. Fourth paragraph. Fifth paragraph.")

    @patch("requests.get")
    def test_extract_text_from_url_error(self, mock_get):
        # Simular una excepción en la solicitud
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        # Llamar a la función
        text = extract_text_from_url("http://example.com")

        # Verificar que se maneja correctamente el error
        self.assertEqual(text, "")

if __name__ == "__main__":
    unittest.main()
