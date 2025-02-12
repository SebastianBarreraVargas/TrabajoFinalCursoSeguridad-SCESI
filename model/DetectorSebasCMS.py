import requests
from bs4 import BeautifulSoup
import random
import re
from difflib import SequenceMatcher
import sys

class RequestHandler:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        self.verify_ssl = True

    def get(self, url, allow_redirects=False):
        return self.session.get(
            url,
            headers=self.headers,
            verify=self.verify_ssl,
            allow_redirects=allow_redirects
        )

class CMSDetector:
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.cms_modules = [
            WordPressModule(request_handler),
            DrupalModule(request_handler),
            JoomlaModule(request_handler),
            GhostModule(request_handler),
            PrestaShopModule(request_handler)
        ]

    def detect(self, url):
        try:
            for module in self.cms_modules:
                if module.detect(url):
                    return module.name
            return 'no esta programado para detectar el CMS de esta pagina'
        except requests.RequestException as error:
            print(f"Error al solicitar la URL: {error}")
            return None

class CMSModule:
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.name = "BaseCMS"
        self.directories_file = None
        self.robots_keywords = []
        self.meta_generator_pattern = ""

    def detect(self, url):
        if self._check_headers(url) or \
           self._check_robots(url) or \
           self._check_meta_tags(url) or \
           self._check_directories(url):
            return True
        return False

    def _check_headers(self, url):
        response = self.request_handler.get(url)
        return any(self._header_checks(response.headers))

    def _header_checks(self, headers):
        return False

    def _check_robots(self, url):
        robots_url = f"{url}/robots.txt"
        response = self.request_handler.get(robots_url)
        return any(keyword in response.text for keyword in self.robots_keywords)

    def _check_meta_tags(self, url):
        response = self.request_handler.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find('meta', {'name': 'generator', 'content': re.compile(self.meta_generator_pattern)})

    def _check_directories(self, url):
        with open(self.directories_file, 'r') as file:
            directories = random.sample(file.readlines(), 30)
        
        similarity_threshold = 0.95
        previous_response = ""
        match_count = 0

        for directory in directories:
            test_url = f"{url}/{directory.strip()}"
            response = self.request_handler.get(test_url)
            
            if response.status_code == 200:
                current_similarity = SequenceMatcher(None, previous_response, response.text).ratio()
                if current_similarity < similarity_threshold:
                    match_count += 1
                    if match_count >= 2:
                        return True
                previous_response = response.text
        return False

class WordPressModule(CMSModule):
    def __init__(self, request_handler):
        super().__init__(request_handler)
        self.name = "WordPress"
        self.directories_file = 'WordPressDirectorios.txt'
        self.robots_keywords = ['wp-']
        self.meta_generator_pattern = r'WordPress\s'

    def _header_checks(self, headers):
        return [
            'Link' in headers and 'rel="https://api.w.org/' in headers['Link'],
            'X-Redirect-By' in headers and 'WordPress' in headers['X-Redirect-By'],
            any(re.search(r'wordpress|wp', headers.get(h, ''), re.I) for h in ['X-Powered-By', 'Link'])
        ]

class DrupalModule(CMSModule):
    def __init__(self, request_handler):
        super().__init__(request_handler)
        self.name = "Drupal"
        self.directories_file = 'DrupalDirectorios.txt'
        self.robots_keywords = ['/core/']
        self.meta_generator_pattern = r'Drupal\s'
        self.drupal_headers = [
            'X-Drupal-Cache', 'X-Drupal-Dynamic-Cache', 'X-Drupal-Cache-Contexts',
            'X-Drupal-Cache-Tags', 'X-Drupal-Cache-Max-Age', 'X-Drupal-Fast-404'
        ]

    def _header_checks(self, headers):
        return [
            headers.get('x-generator', '').startswith('Drupal'),
            any(h in headers for h in self.drupal_headers)
        ]

class JoomlaModule(CMSModule):
    def __init__(self, request_handler):
        super().__init__(request_handler)
        self.name = "Joomla"
        self.directories_file = 'JoomlaDirectorios.txt'
        self.robots_keywords = ['joomla']
        self.meta_generator_pattern = r'Joomla!?\s'

    def _header_checks(self, headers):
        return [
            any(re.search(r'joomla', headers.get(h, ''), re.I) 
            for h in ['X-Content-Encoded-By', 'X-Powered-By', 'X-Generator']),
            'X-Joomla-Cache' in headers
        ]

class GhostModule(CMSModule):
    def __init__(self, request_handler):
        super().__init__(request_handler)
        self.name = "Ghost"
        self.directories_file = 'GhostDirectorios.txt'
        self.robots_keywords = ['/ghost/']
        self.meta_generator_pattern = r'Ghost\s'
        self.ghost_headers = ['Ghost-Age', 'Ghost-Cache', 'Ghost-Fastly']

    def _header_checks(self, headers):
        return [
            any(h in headers for h in self.ghost_headers),
            re.search(r'ghost', headers.get('X-Powered-By', '')), re.I
        ]

class PrestaShopModule(CMSModule):
    def __init__(self, request_handler):
        super().__init__(request_handler)
        self.name = "PrestaShop"
        self.directories_file = 'PrestaShopDirectorios.txt'
        self.meta_generator_pattern = r'PrestaShop\s'

    def _header_checks(self, headers):
        return [
            re.search(r'prestashop', headers.get('Powered-By', ''), re.I),
            'X-PrestaShop' in headers,
            re.search(r'prestashop', headers.get('Set-Cookie', ''), re.I)
        ]

class URLUtils:
    @staticmethod
    def clean_url(url):
        if url.startswith("-w "):
            url = url.replace("-w ", "")
        if '/' in url:
            parts = url.split('/')
            return f"{parts[0]}//{parts[2]}"
        return url