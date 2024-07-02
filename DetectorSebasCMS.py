import requests
from bs4 import BeautifulSoup
import random
import os
url = input("Ingresa una URL: ")
def detectar_cms(url):
    try:
        print(os.getcwd())
        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa

        # Analiza el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')
        # Busca pistas específicas en el contenido HTML para identificar el CMS
        # Detectar WordPress
        if soup.find('meta', {'name': 'generator', 'content': 'WordPress'}) or 'wp-content' in response.text:
            return 'WordPress'
        else: 
            with open('WordPressDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = requests.get(urlDestino)
                if response.status_code == 200:
                    return 'WordPress'
        # Si no se detecta ningún CMS conocido
        return 'no esta programado para detectar el CMS de esta pagina'
    except requests.RequestException as error:
        print(f"Error al solicitar la URL: {error}")
        return None
cms = detectar_cms(url)
print(cms)
