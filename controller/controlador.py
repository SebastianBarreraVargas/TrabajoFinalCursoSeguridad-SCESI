class Controlador:
    def __init__(self, cms_detector, url_utils):
        self.cms_detector = cms_detector
        self.url_utils = url_utils

    def detectar_cms(self, url):
        cleaned_url = self.url_utils.clean_url(url)

        resultado = self.cms_detector.detect(cleaned_url)
        return resultado