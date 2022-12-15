import requests
import json


def push(user_id, app_id, notification_text):
    print(notification_text)
    print("\n-----\n")
    url = 'https://london.bybrisk.com/notification/send/push'
    
    payload = {'user_id': user_id,'app_id': app_id,'push_notification': {"story":notification_text}}
    print(json.dumps(payload))
    print("\n-----\n")
    headers = {'content-type': 'application/json'}

    r = requests.post(url, auth=('shashank','prakash'), data=json.dumps(payload), headers=headers)
    print(r)
