import re
import requests
import sys
from bs4 import BeautifulSoup
from wiki import wiki_url_or_raw

people = {}
queue = []

def main():
    # if command line arguments are given, use them as the starting student ids
    # otherwise, use the default student id
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
    else:
        student_id = '211165'

    depth = 0
    queue.append((student_id,depth))


    # markdown likes a blank line at the beginning
    print("")
    while len(queue) > 0:
        (student_id,depth) = queue.pop()
        if student_id in people:
            #print(f"{' '*3*(depth)} - {people[student_id]['name']} (see above)")
            print(f"{' '*2*(depth)} {people[student_id]['name']} (see above)  ")
            continue
        url = f"https://mathgenealogy.org/id.php?id={student_id}"
        content = download_website(url)
        soup = BeautifulSoup(content, 'html.parser')
        student_name = extract_name(soup)
        advisor_ids = extract_advisors(soup)
        people[student_id] = {'name': student_name, 'advisor_ids': advisor_ids}
        student_name_str = wiki_url_or_raw(student_name)
        #print(f"{' '*3*(depth)} - {student_name_str}")
        print(f"{' '*2*(depth)} {student_name_str}  ")
        queue.extend([(a,depth+1) for a in advisor_ids])

    print(f"""
```
{people}
```""")

def download_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f'Error: Unable to download the website (status code {response.status_code})')
        return None

def extract_name(soup):
    h2_tags = soup.find_all('h2')
    name = h2_tags[0].get_text()
    # trim whitespace from name
    name = name.strip()
    # Remove double spaces from name
    name = re.sub(' +', ' ', name)
    return name


def extract_advisors(soup):
    p_tags = soup.find_all('p')
    pattern = "Advisor[^:]*: <a href=\"id.php\?id=([0-9]+)\">([^<]+)</a>"
    A = []
    for p in p_tags:
        match_groups = re.findall(pattern, p.decode_contents())
        for res in match_groups:
            advisor_id = res[0]
            # We'll get name later
            #advisor_name = res[1]
            A.insert(0,advisor_id)
    return A

if __name__ == "__main__":
    main()
