# TrabajoFinalCursoSeguridad-SCESI [![Logo de la SCESI][logo-SCESI]][enlaceSCESI]
## Presentando: SebasCMSDetector v1.0 Version Linux
### Trabajo hecho por: Sebastian Barrera Vargas
## Librerias necesarias
Para que el programa pueda funcionar de manera adecuada necesitara las siguientes librerias y programas instalados:

* Python, en Linux (distribución Debian en este caso) puedes instarlo desde la terminal con el comando: `sudo apt install python3`.

* Instalar pip, en Linux podrias llegar a necesitar usar este comando `sudo apt install python3-pip`

* Instala las siguientes librerias:
    * beautifulsoup4

        * Puedes usar `sudo apt install python3-bs4` en Debian.
    * requests
        * Puedes usar `sudo apt install python3-requests` en Debian.

## Instrucciones de uso:
* Ejecute el programa luego de instalar el archivo .deb
* Usa la terminal escribiendo el comando `detectorCMS <tu_url>`
* La url debe tener la siguiente estructura:

    * https://`tu_direccion_web`

        o sino 

    * http://`tu_direccion_web`

      segun la url que elegiste lo requiera
* Si la pagina da una excepcion como la que se muestra en el recuadro de abajo le recomiendo usar el modo sin verificacion de certificados, al cual puede acceder usando `-w "tu_url"`, de esta forma no se solicitaran certificados a la pagina web. 

    * `HTTPSConnectionPool(host='www.umss.edu.bo', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')))`
* El programa analizara los 5 CMS para los que esta programado y si su pagina a analizar usa uno de estos gestores de contenido se le devolvera el nombre de ese CMS.
* Puedes usar `detectorCMS -h` para ver informacion del programa.

## CMS soportados por el programa:

SebasCMSDetector v1.0 soporta la siguiente lista de CMS:

* Wordpress
* Drupal
* Joomla
* Ghost
* PrestaShop

[logo-SCESI]: https://github.com/SebastianBarreraVargas/Git/blob/main/Imagenes/scesi-para-fondo-claro-1.png
[enlaceSCESI]: https://www.scesi.org