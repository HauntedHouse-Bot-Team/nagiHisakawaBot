import json
with open("json/bot_id.json","r")as f:
    user = json.load(f)
for i in user.keys():
    user[i]["playlist"]=[]
with open("json/bot_id.json","w")as f:
    json.dump(user, f, indent=3)
