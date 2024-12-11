import requests
import json
import os
import pandas as pd
import time
from datetime import datetime
loginPath = os.path.join(os.path.dirname(__file__),"DB","1loginInfo.json")
restDayPath = os.path.join(os.path.dirname(__file__),"DB","restDay.json")
reMindPath = os.path.join(os.path.dirname(__file__),"DB","reMind.json")
with open(loginPath, 'r', encoding='utf-8') as f:
    login_info = json.load(f)
bot_info = pd.Series(login_info['nFaxbot'])
bot_HC = pd.Series(login_info['nFaxbot_hc'])
def reMind() -> None:
    restDay = pd.read_json(restDayPath,orient="index")
    today = datetime.today()
    toMonth = restDay.loc[today.month].dropna().tolist()
    #공휴일 리마인드 발송 제외
    if today.day not in toMonth:
        if datetime.now().strftime("%H:%M") == "09:00":
            read = pd.read_json(reMindPath,orient='records',dtype={"inputBank":str,"sendBank":str,"cost":str})
            if len(read.index.tolist()) == 1:pass
            else:
                for i in range(1,len(read.index.tolist())):
                    sendText = f"입금 은행 : {read["inputBank"][i]}\n발송한 은행 : {read["sendBank"][i]}\n피해금액 : {read["cost"][i]}"
                    requests.get(f"https://api.telegram.org/bot{bot_info['token']}/sendMessage?chat_id={bot_info['chatId']}&text={sendText}")
                    time.sleep(1)
                #발송 후 데이터 리셋
                pd.DataFrame(data={"inputBank":"test","sendBank":"test","cost":"test"},index=[0]).to_json(reMindPath,orient='records',force_ascii=False,indent=4)
                requests.get(f"https://api.telegram.org/bot{bot_HC['token']}/sendMessage?chat_id={bot_HC['chatId']}&text=리마인드 전송 및 리셋")
                time.sleep(60)
        else:
            time.sleep(30)
            pass
    else:
        time.sleep(36000)
        pass
if __name__ == "__main__":
    while True:reMind()