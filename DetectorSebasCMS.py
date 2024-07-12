import requests
from bs4 import BeautifulSoup
import random
import re
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'}
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
        response = session.get(url, allow_redirects=False, headers = headers, verify=True)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa

        # Analiza el contenido HTML de la página
        soup = BeautifulSoup(response.content,'html.parser')
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
                response = session.get(urlDestino, allow_redirects=False, headers=headers, verify=True)
                if response.history:
                    if response.history[0].status_code == 200:
                        return 'WordPress'
                else:
                    if response.status_code == 200:
                        return 'WordPress'
        response = session.get(url, allow_redirects=False, headers = headers, verify=True)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Drupal ')}) or 'sites/default' in response.text:
            return 'Drupal'
        else: 
            with open('DrupalDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = requests.get(urlDestino, allow_redirects=False, headers = headers, verify=True)
                if response.history:
                    if response.history[0].status_code == 200:
                        return 'Drupal'
                else:
                    if response.status_code == 200:
                        return 'Drupal'
        response = session.get(url, allow_redirects=False, headers = headers, verify=True)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Joomla')}):
            return 'Joomla'
        else: 
            with open('JoomlaDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = requests.get(urlDestino, allow_redirects=False, headers = headers, verify=True)
                if response.history:
                    if response.history[0].status_code == 200:
                        return 'Joomla'
                else:
                    if response.status_code == 200:
                        return 'Joomla'
        response = session.get(url, allow_redirects=False, headers = headers, verify=True)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Ghost')}):
            return 'Ghost'
        else:
            with open('GhostDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = requests.get(urlDestino, allow_redirects=True, headers = headers, verify=True)
                if 'ghost.io'in response.url:
                        return 'Ghost'
        # Si no se detecta ningún CMS conocido
        return 'no esta programado para detectar el CMS de esta pagina'
    except requests.RequestException as error:
        if requests.exceptions.SSLError:
            print('Porfavor use el modo sin verificacion de certificados')
            return None
        print(f"Error al solicitar la URL: {error}")
        return None
cms = detectarCMS(url)
print(cms)