# Link Extractor Program

This project contains a script to extract links from multiple HTTP URLs provided as command-line parameters. The script can generate the links in two different formats, depending on the specified "-o" option.

## Part 1: Task Description

This script allows, using any programming language, to receive a set of HTTP URLs as command-line parameters. It will connect to each URL, extract all the links present in it, and, depending on the "-o" option specified, return the result in one of the following ways:

### Format 1: Absolute URLs in Standard Output

With the "stdout" option, the program will display each extracted absolute URL on a new line.

Usage example:

```
$ ./my_program -u "https://news.ycombinator.com/" -o "stdout"
https://news.ycombinator.com/newest
https://news.ycombinator.com/newcomments
https://news.ycombinator.com/ask
```

### Format 2: JSON Hash

With the "json" option, the program will return a JSON object where the key is the base domain and the value is an array of the relative paths of the links found.

Usage example:

```
$ ./my_program -u "https://news.ycombinator.com/" -u "https://arstechnica.com/" -o 'json'
{
  "https://news.ycombinator.com": ["/newest", "/newcomments", "/ask", ...],
  "https://arstechnica.com": ["/", "/civis/", "/store/product/subscriptions/", ...]
}
```

## Requirements

- The script must accept any number of URLs as parameters.
- It must support the options "-u" to specify URLs and "-o" to define the output format.
- The program can be implemented in any programming language.

## Execution

The script can be executed from the command line with the following format:

```
$ ./my_program -u "<URL1>" -u "<URL2>" ... -o "<stdout|json>"
```

## Example

To extract links from Hacker News and display them in JSON format:

```
$ ./my_program -u "https://news.ycombinator.com/" -u "https://arstechnica.com/" -o "json"
```

This command will extract all the links from the provided URLs and display them in JSON format, as described above.

## Code Explanation

### Imports

- **aiohttp**: Library for making HTTP requests asynchronously.
- **asyncio**: Library for handling asynchronous programming in Python.
- **BeautifulSoup**: Library for parsing HTML documents and extracting data.
- **json**: Library for working with JSON data.
- **urljoin, urlparse**: Functions to manipulate URLs.
- **argparse**: Library for handling command-line arguments.

### Function `fetch_links`

- This function takes an HTTP session (`session`) and a URL (`url`).
- It makes an asynchronous GET request to the URL.
- Parses the HTML content of the response using **BeautifulSoup**.
- Extracts all links (`<a href="...">`) and converts them to absolute URLs using **urljoin**.
- Returns a dictionary with the original URL and the list of extracted links.
- If an error occurs, it prints an error message and returns the URL with an empty list.

### Function `extract_links`

- This function takes a list of URLs (`urls`).
- Creates an asynchronous HTTP session (**ClientSession**).
- Creates a list of tasks (`tasks`) to get the links from each URL using `fetch_links`.
- Executes all tasks concurrently using **asyncio.gather**.
- Returns a dictionary with the results of all tasks.

In summary, this code defines two asynchronous functions to extract links from a list of URLs. It uses **aiohttp** to make HTTP requests asynchronously and **BeautifulSoup** to parse the HTML content and extract the links.

## Part 2: Docker

### Packaging into a Docker Image

To facilitate the execution of the script, a Docker image has been created that allows running the program in an isolated environment. Below are the requirements and features of this Docker image:

- The Docker image runs as a non-root user to improve security.
- It allows passing arguments to the script via the command line, for example:
  ```
  $ docker run -it my_docker_image -u "https://news.ycombinator.com/" -o "stdout"
  ```

### Dockerfile Requirements

- **Run as Non-Root User**: In the Dockerfile, a non-root user is defined to avoid security risks associated with running containers as root.
- **Argument Passing**: The image must be able to accept the same arguments that the script accepts, such as URLs and output format options.
- **Security**: Ideally, the image should pass a security scan. Tools like **Docker Bench for Security** or **Trivy** are recommended to ensure that the image does not contain known vulnerabilities.

### Dockerfile Modifications

The Dockerfile has been modified to update some of the issues that appeared during the initial **Trivy** scan. Since this is only a demo, and to demonstrate an understanding of the vulnerabilities, only a few of them have been fixed. The files **trivy.txt** and **trivy_fix.txt** contain details of the vulnerabilities found and the applied fixes.

