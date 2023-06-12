from base_functions import *
from pathlib import Path


def main():
    category = "Caffeinated soft drinks"
    P17_value = False
    P279_value = "Q116869244"
    category_entries = extract_ids_from_category(category, save_json=False)
    statements = render_quickstatements_for_category(
        category, category_entries, P279_value=P279_value, P17_value=P17_value
    )
    HERE = Path(__file__).parent.resolve()
    category_file_name = category.lower()
    category_file_name = category_file_name.replace(" ", "_")
    HERE.joinpath(f"quickstatements.qs").write_text(statements)


if __name__ == "__main__":
    main()
