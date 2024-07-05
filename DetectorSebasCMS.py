import requests
from bs4 import BeautifulSoup
import random
import re
url = input("Ingresa una URL: ")
def quitarDirectorio(url):
    # Verificar si la URL contiene un directorio
    if '/' in url:
        # Dividir la URL en partes usando '/'
        partes = url.split('/')
        # Tomar la primera parte (la URL original)
        url_original = partes[0] + '//' + partes[2]
        return url_original
    else:
        # Si no hay directorio, devolver la URL tal cual
        return url_original
url = (quitarDirectorio(url))
def detectarCMS(url):
    try:

        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url)
        print(response.text)
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
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Drupal ')}) or 'sites/default' in response.text:
            return 'Drupal'
        # Si no se detecta ningún CMS conocido
        return 'no esta programado para detectar el CMS de esta pagina'
    except requests.RequestException as error:
        print(f"Error al solicitar la URL: {error}")
        return None
cms = detectarCMS(url)
print(cms)
