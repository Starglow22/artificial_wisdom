# from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import json

ROOT = 'https://www.organism.earth/library/'

# SRC_URL = ['http://www.example.com/one', 'https://www.example.com/two']  # A comma-separated list of URLs to scrape
# WEB_CONTEXT = ['span', 'h2']  # A comma-separated list of the tag or object to search for in each page above.
# WEB_ATTRIBUTES = [{'class': 'example-text'}, {}] # A list of dictionaries containing the attributes for each page.
def scrape_page(src_url, web_context, fn):
    links = []
    last_url = ""
    for i in range(len(src_url)):
        if src_url[i] != last_url:
            last_url = src_url[i]
            print(">>> Scraping {0}".format(src_url[i]))
            try:
                page = requests.get(src_url[i])
            except Exception:
                last_url = "ERROR"
                import traceback
                print(">>> Error scraping {0}:".format(src_url[i]))
                print(traceback.format_exc())
                continue
            soup = BeautifulSoup(page.text, 'html.parser')
        hits = soup.find_all(web_context)
        if not hits:
            print(">>> No results found!")
            continue
        else:
            errors = 0
            for hit in hits:
                try:
                    result = fn(hit)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    errors += 1
                    continue
                if result:
                    links.append(result)
            if errors > 0:
                print(">>> We had trouble reading {} result{}.".format(errors, "s" if errors > 1 else ""))
    return(links)

def get_link(hit):
    if hit.li and "title=\"Text\"" in str(hit.li): # Hacky workaround to the fact I can't figure out how to access the second span tag
        return hit.get('href')
    else:
        return False

def strip_text(hit):
    return re.sub(r"</?\w+>", "", hit.get_text()).strip()


if __name__ == "__main__":
    links = scrape_page([ROOT + 'author/10'], 'a', get_link)
    links = list(map(lambda link: ROOT + link, links))
    text = scrape_page(links, 'p', strip_text)
    print(len(text))

    processed = []
    for string in text:
        if '.' in string:
            processed += list(map(lambda s: s+'.', filter(lambda s: len(s) > 3, string.split('.'))))

    # save_file = open('alan_watts.txt', 'w')
    # save_file.write(processed.encode('utf8'))

    with open('alan_watts.json', 'w') as f:
        json.dump(processed, f)

