import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import json
import re


archive_url = 'http://www.ascii-art.de/ascii/'

page_urls = [
    'http://www.ascii-art.de/ascii/index.shtml',        # ab
    'http://www.ascii-art.de/ascii/index_c.shtml',      # c
    'http://www.ascii-art.de/ascii/index_def.shtml',    # def
    'http://www.ascii-art.de/ascii/index_ghi.shtml',    # ghi
    'http://www.ascii-art.de/ascii/index_jkl.shtml',    # jkl
    'http://www.ascii-art.de/ascii/index_mno.shtml',    # mno
    'http://www.ascii-art.de/ascii/index_pqr.shtml',    # pqr
    'http://www.ascii-art.de/ascii/index_s.shtml',      # s
    'http://www.ascii-art.de/ascii/index_t.shtml',      # t
    'http://www.ascii-art.de/ascii/index_uvw.shtml',    # vwx
    'http://www.ascii-art.de/ascii/index_xyz.shtml'      # yz
]

def fetch_ascii_art(url):
    response = requests.get(url)
    # print(response.text)
    if response.status_code == 200:
        return response.text  # Assuming the content is plain text
    else:
        print(f"Failed to fetch {url}: Status code {response.status_code}")
        return None
    
def parse_name_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1]
    name = unquote(filename.split('.')[0])
    return name

# Function to scrape ASCII art and its metadata from a page
def scrape_ascii_art(page_url):
    text = fetch_ascii_art(page_url)
    ascii_art_list = []

    if text:
        ascii_art_list.append({
            'name': parse_name_from_url(page_url),
            'description': '',  # You can fetch description if available in the future
            'ascii_art': text
        })
    
    return ascii_art_list

# print(scrape_ascii_art(archive_url))

# Function to get links to ASCII art pages
def get_ascii_art_links_from_page(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.txt'):
            full_url = urljoin(main_url, href)
            links.append(full_url)
    return links

# Get all links to ASCII art pages
# ascii_art_links = get_ascii_art_links(archive_url)
# print(ascii_art_links)

# noticed it was only getting links from index page, coz only one page was given and the data was paginated, found the structure for pages and ran a for loop
# Function to get all links to ASCII art pages from all structured pages
def get_all_ascii_art_links(page_urls):
    links = []
    for url in page_urls:
        links.extend(get_ascii_art_links_from_page(url))
    return links


# Get all links to ASCII art pages
ascii_art_links = get_all_ascii_art_links(page_urls)


# print(ascii_art_links)



# Scrape ASCII art from each page and store it in a dictionary
ascii_art_data = {}
for link in ascii_art_links:
    # print(link)
    art_data = scrape_ascii_art(link)
    # Use the name of the ASCII art as the key
    # # print(art_data)
    print("art_data",art_data )
    if art_data:
        key = art_data[0]['name'].lower().replace(' ', '_')
    # print("key", key, "art_data",art_data )
        ascii_art_data[key] = art_data

# Save the data to a JSON file
with open('ascii_art.json', 'w') as json_file:
    json.dump(ascii_art_data, json_file, indent=2)

print('ASCII art data has been saved to ascii_art.json')
