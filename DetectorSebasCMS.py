import requests
from bs4 import BeautifulSoup
url = input("Ingresa una URL: ")
def detectar_cms(url):
    try:
        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa

        # Analiza el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')
        # Busca pistas específicas en el contenido HTML para identificar el CMS
        # Detectar WordPress
        if soup.find('meta', {'name': 'generator', 'content': 'WordPress'}) or 'wp-content' in response.text:
            return 'WordPress'
        # Si no se detecta ningún CMS conocido
        return 'no esta programado para detectar el CMS de esta pagina'
    except requests.RequestException as error:
        print(f"Error al solicitar la URL: {error}")
        return None
cms = detectar_cms(url)
print(cms)
