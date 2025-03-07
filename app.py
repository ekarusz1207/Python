import requests
import pandas as pd
import datetime
from datetime import timedelta
import time

# 어제 날짜로 조회하기 위해서 날짜 설정함
yesterday = datetime.date.today() - timedelta(days=1)

# API KEY
headers = {"x-nxopen-api-key":"test_cfe2f1c46928427ec384090118eb693fc3efc0a18c7f71533c998616161ce8f6042c17b6efaa5f8fd964840c765b3b76"}

# OCID
nickname = "수금용무자본"
ocid_url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={nickname}"
ocid_res = requests.get(ocid_url, headers=headers).json()
ocid = ocid_res["ocid"]


# EQUIPMENT
equipment_url = f"https://open.api.nexon.com/maplestory/v1/character/item-equipment?ocid={ocid}&date={yesterday}"
equipment_res = requests.get(equipment_url, headers=headers).json()
equipment = equipment_res

item_data = []
for item in equipment["item_equipment"]:
    item_data.append([item["item_equipment_slot"], item["item_name"], item["item_total_option"]])
equipment_df = pd.DataFrame(item_data, columns=["slot", "name", "option"])



# 콘솔창에 pip install flask 명령어로 flask 설치

# Flask를 사용해서 데이터를 HTML 테이블로 렌더링하는 작업
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    table_html = equipment_df.to_html(classes='table table-striped', index=False, escape=False)
    return render_template('index.html', table=table_html)

if __name__ == "__main__":
    app.run(debug=True)