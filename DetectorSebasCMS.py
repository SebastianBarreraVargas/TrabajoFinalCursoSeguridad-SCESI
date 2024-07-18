import requests
from bs4 import BeautifulSoup
import random
import re
from difflib import SequenceMatcher
import sys
session = requests.Session()
verificacion = True
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'}
url = input("Ingresa una URL: ")
if url.startswith("-w "):
    verificacion = False
    url = url.replace("-w ", "")
if url.startswith("-h" or "-h " or "--help"):
    with open('TextoAyuda.txt', 'r') as archivoAyuda:
        contenido = archivoAyuda.read()
        print(contenido)
    sys.exit()
def calcular_similitud(texto1, texto2):
    return SequenceMatcher(None, texto1, texto2).ratio()
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
        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa, solo se realiza una vez para asegurar que la pagina exista
        cabeceras_de_respuesta =  response.headers
        print('Analizando WordPress')
        #Analisis Cabeceras
        if 'Link' in cabeceras_de_respuesta and 'rel="https://api.w.org/' in cabeceras_de_respuesta['Link']:
            return 'WordPress'
        elif 'X-Redirect-By' in cabeceras_de_respuesta and 'WordPress' in cabeceras_de_respuesta['X-Redirect-By']:
            return 'WordPress'
        elif 'X-Powered-By' in cabeceras_de_respuesta and re.search('wordpress', cabeceras_de_respuesta['X-Powered-By'], re.IGNORECASE):
            return 'WordPress'
        elif 'X-Powered-By' in cabeceras_de_respuesta and re.search('wp', cabeceras_de_respuesta['X-Powered-By'], re.IGNORECASE):
            return 'WordPress'
        #Analiza robots.txt
        urlRobots = url + '/' + 'robots.txt'
        response = session.get(urlRobots, allow_redirects=False, headers = headers, verify=verificacion)
        if 'wp-' in response.text or re.search('WordPress', response.text, re.IGNORECASE):
            return 'WordPress'
        # Analiza el contenido HTML de la página
        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        soup = BeautifulSoup(response.content,'html.parser')
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'WordPress ')}):
            return 'WordPress'
        else: 
            with open('WordPressDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            bandera = False
            similitud = 1
            verificacion_autenticidad = 0
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = session.get(urlDestino, allow_redirects=False, headers=headers, verify=verificacion)
                if bandera == True:
                    similitud = calcular_similitud(response.text, past_response)
                if response.history:
                    if response.history[0].status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'WordPress'
                else:
                    if response.status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'WordPress'
                if response.status_code == 200:
                    bandera = True
                    past_response = response.text
        print('Analizando Drupal')
        #Analisis Cabeceras
        drupal_cabeceras = [
            'X-Drupal-Cache', 'X-Drupal-Dynamic-Cache', 'X-Drupal-Cache-Contexts',
            'X-Drupal-Cache-Tags', 'X-Drupal-Cache-Max-Age', 'X-Drupal-Fast-404', 'X-Drupal-Route-Normalizer',
            'X-Drupal-Quickedit', 'X-Drupal-Regions', 'X-Drupal-Theme', 'X-Drupal-Site']
        if 'x-generator' in cabeceras_de_respuesta and 'Drupal' in cabeceras_de_respuesta['x-generator']:
            return 'Drupal'
        else:
            for cabeceras in drupal_cabeceras:
                if cabeceras in cabeceras_de_respuesta:
                    return 'Drupal'
        urlRobots = url + '/' + 'robots.txt'
        response = session.get(urlRobots, allow_redirects=False, headers = headers, verify=verificacion)
        if '/core/' in response.text:
            return 'Drupal'
        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Drupal ')}) or 'sites/default' in response.text:
            return 'Drupal'
        else: 
            with open('DrupalDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            bandera = False
            similitud = 1
            verificacion_autenticidad = 0
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = session.get(urlDestino, allow_redirects=False, headers=headers, verify=verificacion)
                if bandera == True:
                    similitud = calcular_similitud(response.text, past_response)
                if response.history:
                    if response.history[0].status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'Drupal'
                else:
                    if response.status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'Drupal'
                if response.status_code == 200:
                    bandera = True
                    past_response = response.text
        print('Analizando Joomla')
        #Analisis cabeceras
        if 'X-Content-Encoded-By' in cabeceras_de_respuesta and re.search('joomla', cabeceras_de_respuesta['X-Content-Encoded-By'], re.IGNORECASE):
            return 'Joomla'
        elif 'X-Powered-By' in cabeceras_de_respuesta and re.search('joomla', cabeceras_de_respuesta['X-Powered-By'], re.IGNORECASE):
            return 'Joomla'
        elif 'X-Generator' in cabeceras_de_respuesta and re.search('joomla', cabeceras_de_respuesta['X-Generator'], re.IGNORECASE):
            return 'Joomla'
        elif 'X-Joomla-Cache' in cabeceras_de_respuesta:
            return 'Joomla'

        urlRobots = url + '/' + 'robots.txt'
        response = session.get(urlRobots, allow_redirects=False, headers = headers, verify=verificacion)
        if re.search('joomla', response.text, re.IGNORECASE):
            return 'Joomla'
        
        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Joomla')}):
            return 'Joomla'
        else: 
            with open('JoomlaDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            bandera = False
            similitud = 1
            verificacion_autenticidad = 0
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = session.get(urlDestino, allow_redirects=False, headers=headers, verify=verificacion)
                if bandera == True:
                    similitud = calcular_similitud(response.text, past_response)
                if response.history:
                    if response.history[0].status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'Joomla'
                else:
                    if response.status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'Joomla'
                if response.status_code == 200:
                    bandera = True
                    past_response = response.text
        print('Analizando Ghost')
        #Analisis cabeceras
        ghost_cabeceras = ['Ghost-Age', 'Ghost-Cache', 'Ghost-Fastly']
        if 'X-Powered-By' in cabeceras_de_respuesta and re.search('ghost', cabeceras_de_respuesta['X-Powered-By'], re.IGNORECASE):
            return 'Ghost'
        else:
            for cabeceras in ghost_cabeceras:
                if cabeceras in cabeceras_de_respuesta:
                    return 'Ghost'

        urlRobots = url + '/' + 'robots.txt'
        response = session.get(urlRobots, allow_redirects=False, headers = headers, verify=verificacion)
        if re.search('Ghost', response.text, re.IGNORECASE):
            return 'Ghost'

        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'Ghost')}):
            return 'Ghost'
        else:
            with open('GhostDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = session.get(urlDestino, allow_redirects=True, headers = headers, verify=verificacion)
                if 'ghost.io'in response.url:
                        return 'Ghost'
        print('Analizando PrestaShop')
        #Analisis Cabeceras
        if 'Powered-By' in cabeceras_de_respuesta and re.search('prestashop', cabeceras_de_respuesta['Powered-By'], re.IGNORECASE):
            return 'PrestaShop'
        elif 'X-PrestaShop' in cabeceras_de_respuesta:
            return 'PrestaShop'
        elif 'Set-Cookie' in cabeceras_de_respuesta and re.search('prestashop', cabeceras_de_respuesta['Set-Cookie'], re.IGNORECASE):
            return 'PrestaShop'
        urlRobots = url + '/' + 'robots.txt'
        response = session.get(urlRobots, allow_redirects=False, headers = headers, verify=verificacion)
        with open('PrestaShopRobots.txt', 'r') as file:
            textoPrueba = file.readlines()
        for palabrasClave in textoPrueba:
            palabrasClave = palabrasClave.strip()
            if palabrasClave in response.text:
                return 'PrestaShop'

        response = session.get(url, allow_redirects=False, headers = headers, verify=verificacion)
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'PrestaShop')}) or re.search('prestashop', response.text, re.IGNORECASE):
            return 'PrestaShop'
        else:
            with open('PrestaShopDirectorios.txt', 'r') as file:
                urls = file.readlines()
            urlsSeleccionadas = random.sample(urls, 30)
            bandera = False
            similitud = 1
            verificacion_autenticidad = 0
            for pruebaUrl in urlsSeleccionadas:
                pruebaUrl = pruebaUrl.strip()  # Eliminar espacios en blanco al principio y al final
                urlDestino = url + '/' + pruebaUrl
                response = session.get(urlDestino, allow_redirects=False, headers=headers, verify=verificacion)
                if bandera == True:
                    similitud = calcular_similitud(response.text, past_response)
                if response.history:
                    if response.history[0].status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'PrestaShop'
                else:
                    if response.status_code == 200 and similitud<0.95:
                        verificacion_autenticidad = verificacion_autenticidad + 1
                        if verificacion_autenticidad == 2:
                            return 'PrestaShop'
                if response.status_code == 200:
                    bandera = True
                    past_response = response.text
        # Si no se detecta ningún CMS conocido
        return 'no esta programado para detectar el CMS de esta pagina'
    except requests.RequestException as error:
        print(f"Error al solicitar la URL: {error}")
        return None
cms = detectarCMS(url)
print(cms)