import unittest
from unittest.mock import patch, MagicMock
from chatbot import get_stock_price_from_input, search_google, extract_text_from_url

class TestChatbot(unittest.TestCase):
    
    def test_get_stock_price_valid_company(self):
        with patch('yfinance.Ticker') as mock_ticker:
            mock_instance = MagicMock()
            mock_instance.info = {'currentPrice': 150.25}
            mock_ticker.return_value = mock_instance
            
            resultado = get_stock_price_from_input("¿Cuál es el precio de la accion de Apple?")
            self.assertIn("150.25", resultado)
            self.assertIn("AAPL", resultado)

    def test_get_stock_price_invalid_company(self):
        resultado = get_stock_price_from_input("¿Cuál es el precio de la accion de EmpresaInexistente?")
        self.assertEqual(resultado, "No reconocí el nombre de la empresa. Por favor, especifica una empresa válida.")

    @patch('requests.post')
    def test_search_google(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"organic": [{"title": "Test", "link": "http://test.com"}]}
        mock_post.return_value = mock_response

        resultados = search_google("prueba de búsqueda")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["title"], "Test")

    @patch('requests.get')
    def test_extract_text_from_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '<html><body><p>Texto de prueba 1</p><p>Texto de prueba 2</p></body></html>'
        mock_get.return_value = mock_response

        texto = extract_text_from_url("http://test.com")
        self.assertIn("Texto de prueba 1", texto)
        self.assertIn("Texto de prueba 2", texto)

    def test_get_stock_price_no_stock_query(self):
        resultado = get_stock_price_from_input("¿Cuál es el clima hoy?")
        self.assertIsNone(resultado)

    @patch('requests.post')
    def test_search_google_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        resultados = search_google("prueba error")
        self.assertEqual(resultados, [])

if __name__ == '__main__':
    unittest.main()
