import json
from pathlib import Path
from wdcuration import today_in_quickstatements


category = "American drinks"

HERE = Path(__file__).parent.resolve()


category_file_name = category.lower()
category_file_name = category_file_name.replace(" ", "_")

category_entries = json.loads(HERE.joinpath(f"{category_file_name}.json").read_text())


P279_value = False
P31_value = False


P279_value = "Q40050"
P31_value = False


statements = ""

for k, v in category_entries.items():
    today = today_in_quickstatements()
    category_for_url = category.replace(" ", "_")

    if P279_value:
        statements += f'{v}|P279|{P279_value}|S4656|"https://en.wikipedia.org/wiki/Category:{category_for_url}"|S813|{today}\n'
    if P31_value:
        statements += f'{v}|P31|{P31_value}|S4656|"https://en.wikipedia.org/wiki/Category:{category_for_url}"|S813|{today}\n'

HERE.joinpath(f"{category_file_name}.qs").write_text(statements)
