import requests
import json

token = "token = "Token Service หยิบมาแค่ Message หลัง Bearer""
url = "https://chat-api.one.th/manage/api/v1/getlistroom"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

parameter = {
	"bot_id":"bot_id"
}
response = requests.post(url, headers=headers, data= json.dumps(parameter))
print(f"Status: {response.status_code}, Response: {response.text}") 
