import requests
import os

# Obtener URLs desde variables de entorno (definidas en .env)
backend_url = os.getenv('backend_url', 'http://localhost:5000/')
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', 'http://localhost:5000/')


def get_request(endpoint, **kwargs):
    """
    Realiza una petición GET al backend (Node.js) con parámetros opcionales.
    endpoint: string, ej: '/fetchDealers'
    kwargs: parámetros de query (ej: dealerId=3)
    Retorna: respuesta JSON como diccionario o lista.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def post_review(data_dict):
    """
    Envía una nueva reseña al backend (Node.js) mediante POST.
    data_dict: diccionario con los campos de la reseña.
    Retorna: respuesta JSON del servidor.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    """
    Consulta el microservicio de análisis de sentimientos.
    text: string con el texto de la reseña.
    Retorna: diccionario con el sentimiento (ej: {'sentiment': 'positive'}).
    Si falla, retorna {'sentiment': 'neutral'}.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Sentiment analysis error: {err}")
        return {'sentiment': 'neutral'}
