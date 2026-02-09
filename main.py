import re
import json

def parse_receipt(file_path):
    
    items_list = []
    receipt = {}
    previous_line = None
    dt_pattern = r"(\d+[-/.]\d+[-/.]\d+)\s+(\d{2}:\d{2}:\d{2})"
    item_pattern = r"(\d+)\s+x\s+\$(\d+\.\d{2})"

    with open(file_path, "r", encoding="utf-16") as file:
        
        for line in file:

            line = line.strip()
            dt_match = re.search(dt_pattern, line)
            item_match = re.search(item_pattern, line)

            if ":" in line and line.count(":") < 2:
                key, value = line.split(":", 1)
                receipt[key.strip()] = value.strip()

            # elif ":" in line and line.count(":") >= 2:
            #     date, time = line.split(" ", 1)
            #     receipt["Date"] = date.strip()
            #     receipt["Time"] = time.strip()

            elif dt_match:
                receipt["Date"], receipt["Time"] = dt_match.groups()
            
            elif item_match:
                quantity, price = item_match.groups()
                item = {
                    "name": previous_line.strip(),
                    "quantity": quantity.strip(),
                    "price": price.split()[0].strip()
                }
                items_list.append(item)
                receipt["Items"] = items_list
            
            previous_line = line

    output_path = file_path.rsplit(".", 1)[0] + ".json"
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(receipt, json_file, indent=4)
    print(f"Exported to {output_path}")


parse_receipt("data/receipt.txt")