import json
import re
import argparse

# Opening JSON file
f = open('messages_filtered.json')
parser = argparse.ArgumentParser(description='Process start and end messages.')
parser.add_argument('--startmsg', help='Specify the start message.', default=0)
parser.add_argument('--endmsg', help='Specify the end message.', default=30000)
args = parser.parse_args()
start_msg = int(args.startmsg)
end_msg = int(args.endmsg)
# returns JSON object as 
# a dictionary
data = json.load(f)

def restore_text(dict):
    result = ""
    for item in dict:
        if item["text"] and item["text"] != " ":
            result +=item["text"]
    return result

def analyse_message(message):
    text = restore_text(message["text_entities"])
    result = 'Entr' in text or "ENTRY" in text or "Buy" in text
    result = result and ("Tp" in text or "TP" in text or "Take profit" in text or "target" in text.lower() or "Take Profits" in text or "targets" in text.lower())
    return result


def findpair(message):
    restored_text = restore_text(message["text_entities"])
    result = False
    if "#BTC/USDT" in restored_text:
        return ["BTC", "USDT"]
    for item in message["text_entities"]: 
        if item["type"] == "plain":
            splitted_text = item["text"].split(' ')
            for word in splitted_text:
                if '/' in word:
                    if word.split('/')[0].isupper() and word.split('/')[1].isupper():
                        return word.split('/')
        elif item["type"] == "hashtag":
            if "BTC" in item["text"].upper():
                coin = re.sub("(\#|BTC)", "", item["text"].upper())
                return [coin,"BTC"]
            elif  "USDT" in item["text"].upper():
                coin = re.sub("(\#|USDT)", "", item["text"].upper())
                return [coin,"USDT"]
    if not result:
        if '//' in restored_text in restored_text:
           pattern = r'^(\w+//\s?\w+)'
           matches = re.findall(pattern, restored_text)
           return matches.pop().split("//")
        elif '/' in restored_text and "#" in restored_text:
           pattern = r'#(\w+/\s?\w+)'
           matches = re.findall(pattern, restored_text)
           return matches.pop().split("/")
        elif '/' in restored_text and "$" in restored_text:
           pattern = r'\$(\w+/\s?\w+)'
           matches = re.findall(pattern, restored_text)
           return matches.pop().split("\s")
        elif "#" in restored_text:
           pattern = r'#(\w+\s\w+)'
           matches = re.findall(pattern, restored_text)
           return matches.pop().split("\s")
        else:
            return [re.sub("(\#|USDT)", "", restored_text.split(" ")[0]), "USDT"]
    return False


def find_entrypoint(message):
    result = False
    text = restore_text(message["text_entities"])
    for item in text.splitlines():
        if "Entr" in item or "Buy" in item or "ENTRY" in item:
            if ": " in item:
                entry_text = item.split(": ")[1]
            elif ":" in item:
                entry_text = item.split(":")[1]
            elif " - " in item:
                entry_text = item.split(" - ")[1]         
            elif " " in item:
                entry_text = ', '.join(item.split(" ")[1:])
            else:
                entry_text = re.sub("[^0-9\-\.]", "", item)
            if "-" in entry_text:
                entry_values = entry_text.split("-")
            elif "," in item:
                entry_values = entry_text.split(",")
            elif " " in entry_text:
                entry_values = entry_text.split(" ")
            else:
                entry_values = [entry_text]
            try:                    
                result = [float(re.sub("[^0-9\.]", "", x)) for x in entry_values if re.sub("[^0-9\.]", "", x)]
            except ValueError:
                print("error floating", entry_values)
            except IndexError:
                print("index error", text)
            return result
        
        
def find_take_profit(message):
    result = False
    text = restore_text(message["text_entities"])
    for item in text.splitlines():
        if "profit" in item.lower() or "targets" in item.lower():
            if ": " in item:
                entry_text = item.split(": ")[1]
            elif ":" in item:
                entry_text = item.split(":")[1]
            elif " - " in item:
                entry_text = item.split(" - ")[1]         
            elif " " in item:
                entry_text = ', '.join(item.split(" ")[1:])
            else:
                entry_text = re.sub("[^0-9\-\.]", "", item)
            if "-" in entry_text:
                entry_values = entry_text.split("-")
            elif "," in item:
                entry_values = entry_text.split(",")
            elif " " in entry_text:
                entry_values = entry_text.split(" ")
            else:
                entry_values = [entry_text]
            try:                    
                result = [float(re.sub("[^0-9\.]", "", x)) for x in entry_values if re.sub("[^0-9\.]", "", x)]
            except ValueError:
                print("error floating", entry_values)
            except IndexError:
                print("index error", text)
            return result

def find_stop(message):
    result = False
    text = restore_text(message["text_entities"])
    for item in text.splitlines():
        if "stoploss" in item.lower() or "SL" in item or "loss" in item.lower() or "stop" in item.lower():
            if ": " in item:
                entry_text = item.split(": ")[1]
            elif ":" in item:
                entry_text = item.split(":")[1]
            elif " - " in item:
                entry_text = item.split(" - ")[1]         
            elif " " in item:
                entry_text = ', '.join(item.split(" ")[1:])
            else:
                entry_text = re.sub("[^0-9\-\.]", "", item)
            if "-" in entry_text:
                entry_values = entry_text.split("-")
            elif "," in item:
                entry_values = entry_text.split(",")
            elif " " in entry_text:
                entry_values = entry_text.split(" ")
            else:
                entry_values = [entry_text]
            try:                    
                result = [float(re.sub("[^0-9\.]", "", x)) for x in entry_values if re.sub("[^0-9\.]", "", x)]
            except ValueError:
                print("error floating", entry_values)
            except IndexError:
                print("index error", text)
            return result


processed_counter = 0 
processed_messages_arr = []
for message in data:
    processed_message = {}
    if message["id"] > start_msg:
        print( "processing message {}".format(message["id"]))
        if analyse_message(message):
            processed_counter += 1
            pair = findpair(message)
            entrypoint = find_entrypoint(message)
            take_profit = find_take_profit(message)
            stoploss = find_stop(message)
            if pair and entrypoint and take_profit:
                processed_message["id"] = message["id"]
                processed_message["ts"] = message["date_unixtime"]
                processed_message["datetime"] = message["date"]
                processed_message["pair"] = pair
                processed_message["entrypoint"] = entrypoint
                processed_message["take_profit"] = take_profit
                processed_message["stoploss"] = stoploss
                processed_messages_arr.append(processed_message)
            else:
                print(pair, entrypoint , take_profit)
        else:
            print("Corrupted, skipping")
    if message["id"] >= end_msg:
        f.close()
        print("11Overal messages {}. Recognized {} . Processed {}".format(len(data), processed_counter, len(processed_messages_arr)))
        exit(1)

 
f.close()
with open('/Users/nbulashev/scripts/signals_analysis/rrr.json', 'w', encoding='utf-8') as ff:
    json.dump(processed_messages_arr, ff, ensure_ascii=False, indent=4)
print("Overal messages {}. Recognized {} . Processed {}".format(len(data), processed_counter, len(processed_messages_arr)))