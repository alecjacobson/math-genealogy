import sys
import wikipedia
import random
import warnings
from fuzzywuzzy import fuzz

# for ignoring "GuessedAtParserWarning"
warnings.catch_warnings()
warnings.simplefilter("ignore")

def wiki_url_or_raw(name):
    wiki_search_results = wikipedia.search(name,results = 1)
    if len(wiki_search_results) == 0:
        return name

    page_name = wiki_search_results[0]
    try:
        page = wikipedia.page(page_name, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        return name

    similarity_ratio = fuzz.ratio(name, page_name)
    if similarity_ratio < 50:
        return name

    url = page.url
    return f"[{name}]({url})"



# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'Galileo Galilei'
    print(wiki_url_or_raw(name))
