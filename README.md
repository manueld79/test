Link Extractor Program

Este proyecto contiene un script para extraer enlaces de varias URLs HTTP proporcionadas como parámetros de línea de comandos. El script puede generar los enlaces en dos formatos diferentes, dependiendo de la opción "-o" especificada.

Part 1: Descripción de la Tarea

Este script permite, utilizando cualquier lenguaje de programación, recibir una serie de URLs HTTP como parámetros desde la línea de comandos. Se conectará a cada URL, extraerá todos los enlaces presentes en ella y, según la opción "-o" especificada, devolverá el resultado de una de las siguientes maneras:

Formato 1: URL Absolutas en Salida Estándar

Con la opción "stdout", el programa mostrará cada URL absoluta extraída en una nueva línea.

Ejemplo de uso:

$ ./mi_programa -u "https://news.ycombinator.com/" -o "stdout"
https://news.ycombinator.com/newest
https://news.ycombinator.com/newcomments
https://news.ycombinator.com/ask

Formato 2: Hash JSON

Con la opción "json", el programa devolverá un objeto JSON donde la clave es el dominio base y el valor es un array con los paths relativos de los enlaces encontrados.

Ejemplo de uso:

$ ./mi_programa -u "https://news.ycombinator.com/" -u "https://arstechnica.com/" -o 'json'
{
  "https://news.ycombinator.com": ["/newest", "/newcomments", "/ask", ...],
  "https://arstechnica.com": ["/", "/civis/", "/store/product/subscriptions/", ...]
}

Requisitos

El script debe aceptar cualquier cantidad de URLs como parámetros.

Debe soportar las opciones "-u" para especificar las URLs y "-o" para definir el formato de salida.

El programa puede estar implementado en cualquier lenguaje de programación.

Ejecución

El script se puede ejecutar desde la línea de comandos con el siguiente formato:

$ ./mi_programa -u "<URL1>" -u "<URL2>" ... -o "<stdout|json>"

Ejemplo

Para extraer enlaces de Hacker News y mostrarlos en formato JSON:

$ ./mi_programa -u "https://news.ycombinator.com/" -u "https://arstechnica.com/" -o "json"

Este comando extraerá todos los enlaces de las URLs proporcionadas y los mostrará en formato JSON, como se describe anteriormente.

Explicación del Código

Importaciones

aiohttp: Biblioteca para realizar peticiones HTTP de manera asíncrona.

asyncio: Biblioteca para manejar la programación asíncrona en Python.

BeautifulSoup: Biblioteca para analizar documentos HTML y extraer datos.

json: Biblioteca para trabajar con datos en formato JSON.

urljoin, urlparse: Funciones para manipular URLs.

argparse: Biblioteca para manejar argumentos de línea de comandos.

Función fetch_links

Esta función toma una sesión HTTP (session) y una URL (url).

Realiza una petición GET a la URL de manera asíncrona.

Analiza el contenido HTML de la respuesta usando BeautifulSoup.

Extrae todos los enlaces (<a href="...">) y los convierte a URLs absolutas usando urljoin.

Devuelve un diccionario con la URL original y la lista de enlaces encontrados.

Si ocurre un error, imprime un mensaje de error y devuelve la URL con una lista vacía.

Función extract_links

Esta función toma una lista de URLs (urls).

Crea una sesión HTTP asíncrona (ClientSession).

Crea una lista de tareas (tasks) para obtener los enlaces de cada URL usando fetch_links.

Ejecuta todas las tareas de manera concurrente usando asyncio.gather.

Devuelve un diccionario con los resultados de todas las tareas.

En resumen, este código define dos funciones asíncronas para extraer enlaces de una lista de URLs. Utiliza aiohttp para realizar peticiones HTTP de manera asíncrona y BeautifulSoup para analizar el contenido HTML y extraer los enlaces.

Part 2: Docker

Empaquetado en una Imagen Docker

Para facilitar la ejecución del script, se ha creado una imagen Docker que permite ejecutar el programa en un entorno aislado. A continuación, se describen los requisitos y características de esta imagen Docker:

La imagen Docker se ejecuta como un usuario que no es root para mejorar la seguridad.

Permite pasar argumentos al script mediante la línea de comandos, por ejemplo:

$ docker run -it mi_imagen_docker -u "https://news.ycombinator.com/" -o "stdout"

Requisitos para el Dockerfile

Ejecutar como usuario no root: En el Dockerfile se define un usuario no root para evitar riesgos de seguridad asociados con la ejecución de contenedores como root.

Paso de Argumentos: La imagen debe ser capaz de recibir los mismos argumentos que el script acepta, como URLs y opciones de formato de salida.

Seguridad: Idealmente, la imagen debe pasar un análisis de seguridad (security scan). Se recomienda utilizar herramientas como Docker Bench for Security o Trivy para asegurar que la imagen no contenga vulnerabilidades conocidas.

Modificaciones del Dockerfile

Se ha modificado el Dockerfile para actualizar parte de lo que salía en la primera prueba realizada con Trivy. Ya que solo es para una demo, y para demostrar que se entiende las vulnerabilidades, solo he corregido varias de ellas. Los archivos trivy.txt y trivy_fix.txt contienen los detalles de las vulnerabilidades encontradas y las correcciones aplicadas.

