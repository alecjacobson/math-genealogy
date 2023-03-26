import sys
import wikipedia
import random
import warnings
import requests
from fuzzywuzzy import fuzz

# for ignoring "GuessedAtParserWarning"
warnings.catch_warnings()
warnings.simplefilter("ignore")

def closest_wiki_page(name):
    wiki_search_results = wikipedia.search(name,results = 1)
    if len(wiki_search_results) == 0:
        return None

    page_name = wiki_search_results[0]
    try:
        page = wikipedia.page(page_name, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        return None

    similarity_ratio = fuzz.ratio(name, page_name)
    if similarity_ratio < 50:
        return None

    return page

def wiki_url_or_raw(name):
    page = closest_wiki_page(name)
    if page is None:
        return name
    url = page.url
    return f"[{name}]({url})"

def wiki_thumbnail(page_url, pithumbsize = 300):
    # strip off the https://en.wikipedia.org/wiki/
    url_name = page_url.split('/')[-1]
    # https://stackoverflow.com/a/20311613/148668
    props_image_url = f"http://en.wikipedia.org/w/api.php?action=query&titles={url_name}&prop=pageimages&format=json&pithumbsize={pithumbsize}"
    # get request from props_image_url
    response = requests.get(props_image_url)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        for _, page in pages.items():
            thumbnail = page.get("thumbnail", {})
            source = thumbnail.get("source", "")
            
            if source:
                return source
            else:
                return None
    else:
        return None


# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'Galileo Galilei'
    page = closest_wiki_page(name)
    if page is None:
        print('No page found')

    print(page.url)
    thumbnail_url = wiki_thumbnail(page.url)
    if thumbnail_url is not None:
        print(thumbnail_url)

    
