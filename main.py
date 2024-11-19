import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import argparse

# Function to fetch links from a given URL
async def fetch_links(session, url):
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
            return url, links
    except Exception as e:
        print(f"Error fetching {url}: {type(e).__name__} - {e}")
        return url, []

# Function to extract links from a list of URLs
async def extract_links(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_links(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(results)

# Helper function to organize links into the desired JSON format
def organize_links(links_dict):
    organized = {}
    for base_url, links in links_dict.items():
        parsed_base = urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
        
        if base_domain not in organized:
            organized[base_domain] = []
        
        for link in links:
            parsed_link = urlparse(link)
            if parsed_link.netloc == parsed_base.netloc:  # Only add relative paths
                organized[base_domain].append(parsed_link.path)
    
    return organized

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', nargs='+', help='List of URLs', required=True)
    parser.add_argument('-o', '--output', choices=['stdout', 'json'], required=True)
    args = parser.parse_args()

    # Run the extract_links function with the provided URLs
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    results = loop.run_until_complete(extract_links(args.url))

    # Output the results based on the chosen output format
    if args.output == 'stdout':
        for url, links in results.items():
            for link in links:
                print(link)
    elif args.output == 'json':
        organized_results = organize_links(results)
        print(json.dumps(organized_results, indent=2))

if __name__ == "__main__":
    main()