import requests
import time
from tqdm import tqdm
import json
from os.path import exists
from pathlib import Path

HERE = Path(__file__).parent.resolve()


def extract_ids_from_category(category, get_subcategories=False):
    category_with_prefix = f"Category:{category}"

    if not get_subcategories:
        pages = get_pages_under_category(category_with_prefix)
        non_category_pages = [a for a in pages if "Category:" not in a]
        non_category_pages = [a for a in non_category_pages if "List of" not in a]
        non_category_pages = [a for a in non_category_pages if "list of" not in a]

        pages_with_wikidata_ids = {}

        for pages in tqdm(chunks(non_category_pages, 50)):
            pages_with_wikidata_ids.update(get_ids_from_pages(pages))
            time.sleep(0.2)

        print(pages_with_wikidata_ids)

        category_file_name = category.lower()
        category_file_name = category_file_name.replace(" ", "_")
        HERE.joinpath(f"{category_file_name}.json").write_text(
            json.dumps(pages_with_wikidata_ids, indent=4, sort_keys=True)
        )


def get_ids_from_pages(pages):
    """
    Returns a dictionary with page titles as keys and Wikidata QIDs as values
    """
    url = "https://en.wikipedia.org/w/api.php?action=query"
    params = {
        "format": "json",
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "redirects": "1",
        "titles": "|".join(pages),
    }
    r = requests.get(url, params)
    print(r)
    data = r.json()
    print(data)
    id_dict = {}
    for key, values in data["query"]["pages"].items():
        title = values["title"]
        qid = values["pageprops"]["wikibase_item"]
        id_dict[title] = qid

    return id_dict


def get_pages_under_category(category_name):
    url = "https://en.wikipedia.org/w/api.php?action=query"
    params = {
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category_name,
        "cmlimit": "500",
    }
    r = requests.get(url, params)
    data = r.json()
    pages = []
    for response in data["query"]["categorymembers"]:
        pages.append(response["title"])
    while "continue" in data:
        params.update(data["continue"])
        r = requests.get(url, params)
        data = r.json()
        for response in data["query"]["categorymembers"]:
            pages.append(response["title"])
    return pages


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
