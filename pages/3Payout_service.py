import os
import json
from datetime import datetime
import requests
from jinja2 import Template
from selenium import webdriver
import streamlit as st
# 페이지 레이아웃 설정
st.set_page_config(page_title="지급대행",initial_sidebar_state="expanded")
st.sidebar.title("지급대행")
#DB정보 호출 및 정제
loginInfoPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","loginInfo.json")
sendFaxPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","sendFax.json")
htmlPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","htmlForm","지급대행.html")
with open(loginInfoPath, 'r', encoding='utf-8') as f:
    teleB = json.load(f)
with open(sendFaxPath,"r",encoding="UTF-8") as j:
    faxInfo = json.load(j)
with open(htmlPath,"r",encoding="UTF-8") as html:
    html = html.read()
teleBot = teleB['8faxbot']
#html to image
def toImage(inputURL,outputIMG):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(850,1200)
    driver.get(f"file://{inputURL}")
    # 스크린샷 저장
    driver.save_screenshot(outputIMG)
    driver.quit()
#formating 작업
def formating(form,accountInfo,antherInfo,send):
    #jinja templete 변경 및 formating
    fax8 = Template(form).render(
        account = accountInfo, #지급대행 모계좌
        otherInfomation = antherInfo, #특이사항
        sendBank = send, #수신 은행
        today = datetime.now().strftime("%Y-%m-%d") #발신 날짜
    )
    return fax8
st.write("### 1.지급대행 모계좌")
accountIndex,account,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
st.write("### 2.기타정보")
otherInfomationIndex,otherInfomation,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="top")
sendbankIndex,sendbank,empty = st.columns(spec=[1,3,1],gap="small",vertical_alignment="center")
#입금 모계좌 정보
accountIndex.write("지급대행 모계좌")
account = account.text_input(label="지급대행",value=None,label_visibility="collapsed")
otherInfomationIndex.write("기타사항 : ")
antherInfo = otherInfomation.text_area(label="기타",value=None,label_visibility="collapsed")
antherInfo = antherInfo.replace("\n","<br>") if antherInfo is not None else ""
sendbankIndex.write("발송은행 : ")
sendbank = sendbank.text_input(label="발송은행",value=None,label_visibility="collapsed")
empty,savebtn = st.columns(spec=[5,1],gap="small",vertical_alignment="center")
if savebtn.button("저장"):
    results = formating(form=html,
                        accountInfo = account, #지급대행 모계좌
                        antherInfo = antherInfo, #특이사항
                        send = sendbank, #수신 은행
                        )
    htmlOutput = f"C:\\Users\\USER\\ve_1\\samplePage\\fax8html\\{sendbank}_{datetime.now().microsecond}.html"
    imgOutput = f"C:\\Users\\USER\\ve_1\\samplePage\\fax8image\\{sendbank}_{datetime.now().microsecond}.png"
    with open(htmlOutput,"w",encoding="UTF-8") as html:
        html.write(results)
    toImage(htmlOutput,imgOutput)
    url = f"https://api.telegram.org/bot{teleBot['token']}/sendPhoto"
    with open(imgOutput,"rb") as image_file:
        requests.post(url, data={"chat_id":teleBot['chatId']}, files={"photo": image_file})
    if sendbank == None:
        pass
    else:
        for i in faxInfo.keys():
            if i in sendbank:
                requests.get(f"https://api.telegram.org/bot{teleBot['token']}/sendMessage?chat_id={teleBot['chatId']}&text={faxInfo[i]}")
            else:
                pass