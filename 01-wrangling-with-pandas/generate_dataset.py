import pandas as pd
import csv
import pathlib
import random

def submit_manually(item: str, effect: int) -> str:
    if effect == 0:
        return item
    elif effect == 1:
        return item.capitalize()
    elif effect == 2:
        return item.upper()
    else:
        return None

csv_datatset = pathlib.Path("store_data_20230116.csv")
csv_header = ["Tran ID", "Cat", "Item", "Qty", "Unit Price"]

with csv_datatset.open(mode="w") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header, lineterminator="\n")
    csv_writer.writeheader()

    trans_id = 25000
    products = {
        "fruits": ["bananas", "oranges", "apples", "grapes"],
        "legumes": ["lentils", "navy beans", "black-eyed peas", "chickpeas"],
        "vegetables": ["carrots", "broccoli", "lettuce", "potatos"]
    }

    prices = {}
    for item in products["fruits"] + products["legumes"] + products["vegetables"]:
        prices[item] = round(random.random() * 10, 2)
       

    for _ in range(5000):
        items_count = random.randint(1, 5)
        trans_id += random.randint(0, 10)
        manual = random.randint(1, 50) == 50

        for i in range(1, items_count):
            
            cat = random.choice(list(products.keys()))
            item = random.choice(products[cat])
            qty = random.randint(1, 5)
            unit_price = prices[item]

            if manual:
                effect = random.randint(0, 4)
                cat = submit_manually(cat, effect)
                item = submit_manually(item, effect)

            data = {
                "Tran ID": trans_id,
                "Cat": cat,
                "Item": item,
                "Qty": qty,
                "Unit Price": unit_price
            }
            csv_writer.writerow(data)
            
        trans_id += 1