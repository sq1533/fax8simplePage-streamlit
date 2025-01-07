import os
import json
import pandas as pd
import requests
import time
from datetime import datetime, timedelta

#데이터 호출
loginPath = os.path.join(os.path.dirname(__file__),"..","loginInfo.json")
restDayPath = os.path.join(os.path.dirname(__file__),"..","restDay.json")
reMindPath = os.path.join(os.path.dirname(__file__),"DB","reMind.json")
with open(loginPath, 'r', encoding='utf-8') as f:
    login_info = json.load(f)
with open(restDayPath,"r") as f:
    restday = json.load(f)
bot_info = pd.Series(login_info['nFaxbot'])
bot_HC = pd.Series(login_info['nFaxbot_hc'])

#리마인드
def reMind() -> None:
    today = datetime.now()
    next_day = today + timedelta(days=1)
    #공휴일 리마인드 발송 제외
    if (today.weekday() == 5) or (today.weekday() == 6) or (today.strftime('%d') in restday[today.strftime('%m')]):
        if today.strftime("%H:%M") == "09:00":
            read = pd.read_json(restday,orient='records',dtype={"sendDay":str,"inputBank":str,"sendBank":str,"cost":str,"comments":str})
            if len(read.index.tolist()) == 1:
                pass
            else:
                for i in read["sendDay"].tolist():
                    if i == today.strftime("%m-%d"):
                        pass
                    else:
                        ID = read[read["sendDay"].isin(i)].index
                        sendText = f"발송날짜 : {read["sendDay"][ID]}\n입금 은행 : {read["inputBank"][ID]}\n발송한 은행 : {read["sendBank"][i]}\n피해금액 : {read["cost"][i]}\n{read["comments"][i]}"
                        requests.get(f"https://api.telegram.org/bot{bot_info['token']}/sendMessage?chat_id={bot_info['chatId']}&text={sendText}")
                        time.sleep(1)
                #발송 후 데이터 리셋
                pd.DataFrame(data={"sendDay":next_day.strftime("%m-%d"),"inputBank":"test","sendBank":"test","cost":"test","comments":"test"},index=[0]).to_json(reMindPath,orient='records',force_ascii=False,indent=4)
                requests.get(f"https://api.telegram.org/bot{bot_HC['token']}/sendMessage?chat_id={bot_HC['chatId']}&text=리마인드 전송 및 리셋")
                time.sleep(60)
        else:
            time.sleep(30)
            pass
    else:
        time.sleep(36000)
        pass
if __name__ == "__main__":
    while True:
        reMind()