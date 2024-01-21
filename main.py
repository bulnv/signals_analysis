import json
import re

# Opening JSON file
f = open('messages_filtered.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)


def findpair(text):
    splitted_text = text.split(' ')
    for word in splitted_text:
        if '/' in word:
            if word.split('/')[0].isupper() and word.split('/')[1].isupper():
                return word.split('/')
            

def find_entrypoint(text):
    result = "x"
    if "Entry" in text:
        for item in text.split("\n"):
            if "Entry" in item or "Buy" in item:
                if ":" in item:
                    entry_text = item.split(": ")[1]
                elif " - " in item:
                    entry_text = item.split(" - ")[1]
                else:
                    entry_text = re.sub("[^0-9\-]", "", item).split('-')
                try:                    
                    result = [float(re.sub("[^0-9]", "", x)) for x in entry_text]
                except ValueError:
                    print(text)
                return result
# Iterating through the json
# list
for message in data:
    for item in message["text_entities"]: 
        if item["type"] == "plain":
            print(findpair(item["text"]))
            print(find_entrypoint((item["text"])))

 
# Closing file
f.close()