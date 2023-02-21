import json
from pathlib import Path
from wdcuration import today_in_quickstatements

HERE = Path(__file__).parent.resolve()

ny_exchange_companies = json.loads(HERE.joinpath("new_york_exchange.json").read_text())


statements = ""

for k, v in ny_exchange_companies.items():
    today = today_in_quickstatements()
    statements += f'{v}|P414|Q13677|S4656|"https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_New_York_Stock_Exchange"|S813|{today}\n'
    statements += f'{v}|P31|Q891723|S4656|"https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_New_York_Stock_Exchange"|S813|{today}\n'

HERE.joinpath("new_york_exchange.qs").write_text(statements)
