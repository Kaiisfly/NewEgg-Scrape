from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for? ")
if "Ti" not in search_term.lower():
    search_regex = re.compile(rf"\b{search_term}\b", flags=re.IGNORECASE)
else:
    search_regex = re.compile(rf"\b{search_term}ti\b", flags=re.IGNORECASE)

url = f"https://www.newegg.com/global/hk-en/p/pl?d={search_term}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/global/hk-en/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=search_regex)

    for item in items:
        if "ti" not in search_term.lower() and "ti" in item.lower():
            continue

        parent = item.parent
        if parent.name != "a":
            continue

        link = parent['href']
        next_parent = item.find_parent(class_="item-container")
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("-------------------------------")
