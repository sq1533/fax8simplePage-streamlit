import streamlit as st
from jinja2 import Template
import json
import requests
import pandas as pd
from datetime import datetime
from selenium import webdriver
# 페이지 레이아웃 설정
st.set_page_config(page_title="선불",initial_sidebar_state="expanded")
st.sidebar.title("선불")
#DB정보 호출 및 정제
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json', 'r', encoding='utf-8') as f:
    teleB = json.load(f)
with open("C:\\Users\\USER\\ve_1\\DB\\acountInfo.json","r",encoding="UTF-8") as j:
    ACOUNT = json.load(j)
with open("C:\\Users\\USER\\ve_1\\samplePage\\htmlForm\\선불.html","r",encoding="UTF-8") as html:
    html = html.read()
teleBot = teleB['ezmailbot']
MID = ACOUNT["가맹점"]
sec_2 = ACOUNT["입금모계좌"]
sec_3 = ACOUNT["정산"]
#html to image
def toImage(inputURL,outputIMG):
    driver = webdriver.Chrome()
    driver.set_window_size(850,1200)
    driver.get(f"file://{inputURL}")
    # 스크린샷 저장
    driver.save_screenshot(outputIMG)
    driver.quit()
#formating 작업
def formating(form,sec_1_bank,sec_1_acount,sec_1_name,sec_1_time,sec_1_cost,sec_2_bank,sec_2_acount,sec_2_time,sec_3_bank,sec_3_acount,tradeNo,orderNo,antherInfo,send):
    #jinja templete 변경 및 formating
    fax8 = Template(form).render(
        section_1_bank = sec_1_bank, #재이전 모계좌 은행
        section_1_acount = sec_1_acount, #재이전 모계좌 번호
        section_1_name = sec_1_name, #재이전 가맹점
        section_1_time = sec_1_time, #정산 시간
        section_1_cost = sec_1_cost, #피해금
        section_2_bank = sec_2_bank, #입금 은행
        section_2_acount = sec_2_acount, #입금 계좌
        section_2_time = sec_2_time, #입금 시간
        section_3_bank = sec_3_bank, #정산 계좌 은행
        section_3_acount = sec_3_acount, #정산 계좌 번호
        trNum = tradeNo, #거래번호
        orNum = orderNo, #주문번호
        otherInfomation = antherInfo, #특이사항
        sendBank = send, #수신 은행
        today = datetime.now().strftime("%Y-%m-%d") #발신 날짜
    )
    return fax8

#선불가맹점 서비스
servise = st.selectbox(label="서비스",options=["간편결제","VAN가상계좌","PG가상계좌","010PAY"])
midList = MID[servise]
st.write("### 1.재이전된 계좌 정보 입력")
mid = st.selectbox(label="MID",options=list(midList.keys()),index=None,placeholder="선택",label_visibility="collapsed")
section_1_bankIndex,section_1_bank,section_1_acountIndex,section_1_acount = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
section_1_nameIndex,section_1_name,empty = st.columns(spec=[1,2,3],gap="small",vertical_alignment="center")
st.write("### 2.입금 모계좌")
inputAcount = st.selectbox(label="입금모계좌",options=list(sec_2.keys()),index=None,placeholder="선택",label_visibility="collapsed")
section_2_bankIndex,section_2_bank,section_2_acountIndex,section_2_acount = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
st.write("### 3.피해정보")
section_2_timeIndex,section_2_day,section_2_time,empty,empty = st.columns(spec=[1,1,1,1,1],gap="small",vertical_alignment="center")
section_1_timeIndex,section_1_day,section_1_time,empty,empty = st.columns(spec=[1,1,1,1,1],gap="small",vertical_alignment="center")
section_1_costIndex,section_1_cost,empty,empty = st.columns(spec=[1,2,1,1],gap="small",vertical_alignment="center")
st.write("### 4.기타정보")
trNumIndex,trNum,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
orNumIndex,orNum,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
otherInfomationIndex,otherInfomation,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="top")
sendbankIndex,sendbank,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
#가맹점 계좌정보
if mid == None:
    section_1_bankIndex.write("은행 : ")
    bank1 = section_1_bank.text_input(label="재이전계좌 은행",value=None,label_visibility="collapsed")
    section_1_acountIndex.write("계좌 번호 : ")
    acount1 = section_1_acount.number_input(label="재이전계좌 번호",value=None,step=1,label_visibility="collapsed")
    section_1_nameIndex.write("명의인 : ")
    name1 = section_1_name.text_input(label="재이전계좌 명의인",value=None,label_visibility="collapsed")
else:
    section_1_bankIndex.write("은행: ")
    bank1 = midList[mid]["은행"]
    section_1_bank.write(midList[mid]["은행"])
    section_1_acountIndex.write("계좌 번호: ")
    acount1 = midList[mid]["계좌"]
    section_1_acount.write(midList[mid]["계좌"])
    section_1_nameIndex.write("명의인 : ")
    name1 = midList[mid]["예금주"]
    section_1_name.write(midList[mid]["예금주"])
#입금 모계좌 정보
if inputAcount == None:
    section_2_bankIndex.write("은행 : ")
    bank2 = section_2_bank.text_input(label="입금계좌 은행",value=None,label_visibility="collapsed")
    section_2_acountIndex.write("계좌 번호 : ")
    acount2 = section_2_acount.number_input(label="입금계좌 번호",value=None,step=1,label_visibility="collapsed")
else:
    section_2_bankIndex.write("은행 : ")
    bank2 = sec_2[inputAcount]["은행"]
    section_2_bank.write(sec_2[inputAcount]["은행"])
    section_2_acountIndex.write("계좌 번호 : ")
    acount2 = sec_2[inputAcount]["계좌"]
    section_2_acount.write(sec_2[inputAcount]["계좌"])
bank3 = sec_3[servise]["은행"]
acount3 = sec_3[servise]["계좌"]
section_2_timeIndex.write("입금 시간 : ")
day2 = section_2_day.date_input(label="입금 날짜",label_visibility="collapsed")
time2 = section_2_time.text_input(label="입금 시간",value=None,label_visibility="collapsed")
section_1_timeIndex.write("정산 시간 : ")
day1 = section_1_day.date_input(label="정산 날짜",label_visibility="collapsed")
time1 = section_1_time.text_input(label="정산 시간",value=None,label_visibility="collapsed")
section_1_costIndex.write("피해금 : ")
cost1 = section_1_cost.number_input(label="피해금",value=None,step=1,label_visibility="collapsed")
trNumIndex.write("거래번호 : ")
tradeNo = trNum.text_input(label="거래번호",value=None,label_visibility="collapsed")
orNumIndex.write("주문번호 : ")
orderNo = orNum.text_input(label="주문번호",value=None,label_visibility="collapsed")
otherInfomationIndex.write("기타사항 : ")
antherInfo = otherInfomation.text_area(label="주문번호",value="-",label_visibility="collapsed")
sendbankIndex.write("발송은행 : ")
sendbank = sendbank.text_input(label="발송은행",value=None,label_visibility="collapsed")
empty,savebtn = st.columns(spec=[5,1],gap="small",vertical_alignment="center")
if savebtn.button("저장"):
    results = formating(form=html,
                        sec_1_bank=bank1,
                        sec_1_acount=acount1,
                        sec_1_name=name1,
                        sec_1_time=f"{day1}<br>{time1}",
                        sec_1_cost=cost1,
                        sec_2_bank=bank2,
                        sec_2_acount=acount2,
                        sec_2_time=f"{day2}<br>{time2}",
                        sec_3_bank=bank3,
                        sec_3_acount=acount3,
                        tradeNo=tradeNo,
                        orderNo=orderNo,
                        antherInfo=antherInfo.replace("  \n","<br>"),
                        send=sendbank
                        )
    htmlOutput = f"C:\\Users\\USER\\ve_1\\samplePage\\fax8html\\{sendbank}_{cost1}_{datetime.now().microsecond}.html"
    imgOutput = f"C:\\Users\\USER\\ve_1\\samplePage\\fax8image\\{sendbank}_{cost1}_{datetime.now().microsecond}.png"
    with open(htmlOutput,"w",encoding="UTF-8") as html:
        html.write(results)
    toImage(htmlOutput,imgOutput)
    url = f"https://api.telegram.org/bot{teleBot['token']}/sendPhoto"
    with open(imgOutput,"rb") as image_file:
        requests.post(url, data={"chat_id":teleBot['chatId']}, files={"photo": image_file})
    if str(day2) == datetime.now().strftime("%Y-%m-%d"):
        read = pd.read_json("C:\\Users\\USER\\ve_1\\DB\\6reMind.json",orient='records',dtype={"inputBank":str,"sendBank":str,"cost":str})
        new = pd.DataFrame(data={"inputBank":bank2,"sendBank":sendbank,"cost":str(cost1)},index=[0])
        pd.concat([read,new],ignore_index=True).to_json("C:\\Users\\USER\\ve_1\\DB\\6reMind.json",orient='records',force_ascii=False,indent=4)
    else:pass