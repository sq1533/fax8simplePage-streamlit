import streamlit as st
from jinja2 import Template
import json
import requests
from datetime import datetime
from selenium import webdriver
#DB정보 호출 및 정제
with open('C:\\Users\\USER\\ve_1\\DB\\3loginInfo.json', 'r', encoding='utf-8') as f:
    teleB = json.load(f)
with open("C:\\Users\\USER\\ve_1\\DB\\acountInfo.json","r",encoding="UTF-8") as j:
    ACOUNT = json.load(j)
with open("C:\\Users\\USER\\ve_1\\samplePage\\htmlForm\\비선불.html","r",encoding="UTF-8") as html:
    html = html.read()
teleBot = teleB['ezmailbot']
sec_2 = ACOUNT["입금모계좌"]
#html to image
def toImage(inputURL,outputIMG):
    driver = webdriver.Chrome()
    driver.set_window_size(850,1200)
    driver.get(f"file://{inputURL}")
    # 스크린샷 저장
    driver.save_screenshot(outputIMG)
    driver.quit()
#formating 작업
def formating(form,sec_1_cost,sec_2_bank,sec_2_acount,sec_2_time,antherInfo,send):
    #jinja templete 변경 및 formating
    fax8 = Template(form).render(
        section_1_cost = sec_1_cost, #피해금
        section_2_bank = sec_2_bank, #입금 은행
        section_2_acount = sec_2_acount, #입금 계좌
        section_2_time = sec_2_time, #입금 시간
        otherInfomation = antherInfo, #특이사항
        sendBank = send, #수신 은행
        today = datetime.now().strftime("%Y-%m-%d") #발신 날짜
    )
    return fax8
st.write("### 1.입금 모계좌")
inputAcount = st.selectbox(label="입금모계좌",options=list(sec_2.keys()),index=None,placeholder="선택",label_visibility="collapsed")
section_2_bankIndex,section_2_bank,section_2_acountIndex,section_2_acount = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
st.write("### 2.피해정보")
section_2_timeIndex,section_2_day,section_2_time,empty,empty = st.columns(spec=[1,1,1,1,1],gap="small",vertical_alignment="center")
section_1_costIndex,section_1_cost,empty,empty = st.columns(spec=[1,2,1,1],gap="small",vertical_alignment="center")
st.write("### 3.기타정보")
otherInfomationIndex,otherInfomation,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="top")
sendbankIndex,sendbank,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
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
section_2_timeIndex.write("입금 시간 : ")
day2 = section_2_day.date_input(label="입금 날짜",label_visibility="collapsed")
time2 = section_2_time.text_input(label="입금 시간",value=None,label_visibility="collapsed")
section_1_costIndex.write("피해금 : ")
cost1 = section_1_cost.number_input(label="피해금",value=None,step=1,label_visibility="collapsed")
otherInfomationIndex.write("기타사항 : ")
antherInfo = otherInfomation.text_area(label="주문번호",value="-",label_visibility="collapsed")
sendbankIndex.write("발송은행 : ")
sendbank = sendbank.text_input(label="발송은행",value=None,label_visibility="collapsed")
empty,savebtn = st.columns(spec=[5,1],gap="small",vertical_alignment="center")
if savebtn.button("저장"):
    results = formating(form=html,
                        sec_1_cost=cost1,
                        sec_2_bank=bank2,
                        sec_2_acount=acount2,
                        sec_2_time=f"{day2}<br>{time2}",
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