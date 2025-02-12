# main.py
from view.vista import Vista
from controller.controlador import Controlador
from model.DetectorSebasCMS import CMSDetector, RequestHandler, URLUtils

def main():
    # Inicializar el modelo
    request_handler = RequestHandler()
    cms_detector = CMSDetector(request_handler)

    # Inicializar el controlador
    controlador = Controlador(cms_detector, URLUtils)

    # Inicializar la vista y pasarle el controlador
    vista = Vista(controlador)

    # Ejecutar la aplicación
    vista.iniciar()

if __name__ == "__main__":
    main()