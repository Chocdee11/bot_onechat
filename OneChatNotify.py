import requests
import pymssql
import json

## Connection Database
server = "............."
user = "............."
password = "............."
database = "............."

conn = pymssql.connect(server, user, password,database)
cursor = conn.cursor()

## Query สำหรับเช็คข้อมูลที่ต้องการ
query = """
select distinct
	'API_CussatEHPv2_EVAUsageV2AllRating_UAT' as table_name,
	updateat_etl,
	case
		when datediff(HOUR,getdate(),cast(updateat_etl as datetime)) between -1 and 1 then 'success'
		else 'fail'
	End as status_update,
	count(*) as row_count
from [dbo].[API_CussatEHPv2_EVAUsageV2AllRating_UAT]
group by updateat_etl
"""
cursor.execute(query)
rows = cursor.fetchall()

conn.close()

## Token ที่ได้รับใน Token Service
token = "Token Service หยิบมาแค่ Message หลัง Bearer"
url = "https://chat-api.one.th/message/api/v1/push_message"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

## loop เพื่อรับข้อมูลที่ต้องการ
for row in rows:
    table = row[0]
    updateat_etl = row[1]
    status = row[2]
    count_row = str(row[3])
    # Add more column names as needed

## Message ที่ต้องการให้แสดงผลใน Notify
message = (
    f"Job_name : CussatEHPv2_UAT\n"
    f"Database : EHP_UAT\n"
    f"Table : API_CussatEHPv2_EVAUsageV2AllRating_UAT\n"
    f"updateat_etl : {updateat_etl}\n"
    f"status : {status}\n"
    f"row_count : {count_row}\n"
)

## กำหนดตาม Document 
parameter = {
    "to" : "One ID จาก One platform",
    "bot_id" : "Bot ID",
    "type" : "text", # รูปแบบของ Message ที่ส่งค่า
    "message" : f'{message}',
    "custom_notification" : "เปิดอ่านข้อความใหม่จากทางเรา" # message ที่จะขึ้นหน้ากล่องข้อความ
  }

response = requests.post(url, headers=headers, data= json.dumps(parameter))
print(f"Status: {response.status_code}, Response: {response.text}") 
