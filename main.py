import re
import json
import yaml

def convert_type(key, value, config):
    if key in config["types"]["float"]:
        return float(value)
    if key in config["types"]["int"]:
        return int(value)
    return value

def parse_receipt(file_path, config):
    
    items_list = []
    receipt = {}
    previous_line = "" 

    with open(file_path, "r", encoding="utf-16") as file:
                   
        item_pattern = config["items"]["pattern"].format(
        separator=config["items"]["separator"],
        currency=re.escape(config["currency"]))
        
        for line in file:

            line = line.strip()
            item_match = re.search(item_pattern, line)

            # Everything but the date/time and items should be in key:value format.
            if ":" in line and line.count(":") < 2:

                line = line.strip().replace(config["currency"], "")
                
                key, value = line.split(":", 1)
                clean_key = key.strip().lower()
                value = value.strip()
                value = convert_type(clean_key, value, config)
                receipt[clean_key] = value

            # Date and time might not be on the same line, so we check for both patterns indepandantly.
            for rule in config["date_time"]:

                match = re.search(rule["pattern"], line)

                if match:
                    receipt[rule["field"]] = match.group(0)
                      
            # Items are often on the line after the item name, so we use the previous line as the item name if we find a match for quantity and price.
            if item_match:
                
                item = {
                    "name": previous_line.strip(),
                    "quantity": convert_type("quantity", item_match.group(1), config),
                    "price": convert_type("price", item_match.group(2), config)   
                }

                items_list.append(item)

                receipt["Items"] = items_list
            
            previous_line = line

    print(json.dumps(receipt, indent=4))

parse_receipt("data/receipt.txt", yaml.safe_load(open("config/config.yaml")))