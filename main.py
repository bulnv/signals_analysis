import json
 
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

# Iterating through the json
# list
for message in data:
    for item in message["text_entities"]: 
        if item["type"] == "plain":
            print(findpair(item["text"]))

 
# Closing file
f.close()