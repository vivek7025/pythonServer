import json

import requests

BASE ="http://172.20.10.2:5000/"
BASE2 ="https://reminder-dfe59-default-rtdb.asia-southeast1.firebasedatabase.app/"

data = [{"likes": 78, "name": "balebale","views": 10000},
        {"likes": 10000, "name": "hhdg","views": 95000},
        {"likes": 25, "name": "heropandi","views": 35200}]

# response = requests.get(BASE + "bot/How are you")
# print(response.json())

jsValue = {
        "intent" : "call",
        "slot1" : "Vijay"
}
# jsObject = json.loads(jsValue)
response2 = requests.post(BASE2,json=jsValue)
print(response2.json())


# for i in range(len(data)):
#     response = requests.put(BASE +"video/" + str(i), data[i])
#     print(response.json())
#
# input()
# response = requests.delete(BASE + "video/0")
# print(response)
# input()
# response = requests.get(BASE +"video/2")
# print(response.json())

# response = requests.get(BASE +"helloworld/vivek")
# print(response.json())