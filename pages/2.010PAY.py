import streamlit as st
from jinja2 import Template
import json
import os
import requests
from datetime import datetime
from selenium import webdriver
# 페이지 레이아웃 설정
st.set_page_config(page_title="010PAY",initial_sidebar_state="expanded")
st.sidebar.title("010PAY")
#DB정보 호출 및 정제
loginInfoPath = os.path.join(os.path.dirname(__file__),"DB","1loginInfo.json")
acountInfoPath = os.path.join(os.path.dirname(__file__),"DB","acountInfo.json")
sendFaxPath = os.path.join(os.path.dirname(__file__),"DB","sendFax.json")
htmlPath = os.path.join(os.path.dirname(__file__),"htmlForm","010PAY.html")
with open(loginInfoPath, 'r', encoding='utf-8') as f:
    teleB = json.load(f)
with open(acountInfoPath,"r",encoding="UTF-8") as j:
    ACOUNT = json.load(j)
with open(sendFaxPath,"r",encoding="UTF-8") as j:
    faxInfo = json.load(j)
with open(htmlPath,"r",encoding="UTF-8") as html:
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
def formating(form,sec_1_bank,sec_1_acount,sec_1_name,sec_1_time,sec_1_cost,sec_2_bank,sec_2_acount,sec_2_time,sec_2_cost,sec_3_bank,sec_3_acount,sec_3_time,AboutBuy,UsedCost,ReturnCost,InCost,antherInfo,send):
    #jinja templete 변경 및 formating
    fax8 = Template(form).render(
        section_1_bank = sec_1_bank, #환불계좌 은행
        section_1_acount = sec_1_acount, #환불계좌 번호
        section_1_name = sec_1_name, #환불계좌 명의인
        section_1_time = sec_1_time, #환불 시간
        section_1_cost = sec_1_cost, #환불금
        section_2_bank = sec_2_bank, #입금 은행
        section_2_acount = sec_2_acount, #입금 계좌
        section_2_time = sec_2_time, #입금 시간
        section_2_cost = sec_2_cost, #피해금
        section_3_bank = sec_3_bank, #정산 계좌 은행
        section_3_acount = sec_3_acount, #정산 계좌 번호
        section_3_time = sec_3_time, #정산 시간
        aboutBuy = AboutBuy, #실제사용처
        usedCost = UsedCost, #이용 금액
        returnCost = ReturnCost, #환불 금액
        inCost = InCost, #선불충전금 잔액
        otherInfomation = antherInfo, #특이사항
        sendBank = send, #수신 은행
        today = datetime.now().strftime("%Y-%m-%d") #발신 날짜
    )
    return fax8
st.write("### 입금 모계좌")
inputAcount = st.selectbox(label="입금모계좌",options=list(sec_2.keys()),index=None,placeholder="선택",label_visibility="collapsed")
section_2_bankIndex,section_2_bank,section_2_acountIndex,section_2_acount = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
section_2_timeIndex,section_2_day,section_2_time,empty = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
section_2_costIndex,section_2_cost,empty = st.columns(spec=[1,2,3],gap="small",vertical_alignment="center")
pay010 = st.radio(label="잔금처리방법",options=["선불충전금 보유","기프티몰 결제","고객계좌 환불"],label_visibility="collapsed")
if pay010 == "선불충전금 보유":
    bank1 = "-"
    acount1 = "-"
    name1 = "-"
    cost1 = "-"
    day1 = "-"
    time1 = "-"
    bank3 = "-"
    acount3 = "-"
    day3 = "-"
    time3 = "-"
elif pay010 == "기프티몰 결제":
    bank1 = "-"
    acount1 = "-"
    name1 = "-"
    cost1 = "-"
    day1 = "-"
    time1 = "-"
    section_3_timeIndex,section_3_day,section_3_time,empty = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
    #정산 모계좌 정보
    bank3 = sec_3["010PAY"]["은행"]
    acount3 = sec_3["010PAY"]["계좌"]
    section_3_timeIndex.write("정산 시간 : ")
    day3 = section_3_day.date_input(label="정산 날짜",label_visibility="collapsed")
    time3 = section_3_time.text_input(label="정산 시간",value=None,label_visibility="collapsed")
else:
    st.write("### 환불 계좌 정보")
    section_1_bankIndex,section_1_bank,section_1_acountIndex,section_1_acount = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
    section_1_nameIndex,section_1_name,empty = st.columns(spec=[1,2,3],gap="small",vertical_alignment="center")
    section_1_timeIndex,section_1_day,section_1_time,empty = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
    section_3_timeIndex,section_3_day,section_3_time,empty = st.columns(spec=[1,1,1,3],gap="small",vertical_alignment="center")
    section_1_costIndex,section_1_cost,empty = st.columns(spec=[1,2,3],gap="small",vertical_alignment="center")
    #환불 계좌정보
    section_1_bankIndex.write("은행 : ")
    bank1 = section_1_bank.text_input(label="재이전계좌 은행",value=None,label_visibility="collapsed")
    section_1_acountIndex.write("계좌 번호 : ")
    acount1 = section_1_acount.number_input(label="재이전계좌 번호",value=None,step=1,label_visibility="collapsed")
    section_1_nameIndex.write("명의인 : ")
    name1 = section_1_name.text_input(label="재이전계좌 명의인",value=None,label_visibility="collapsed")
    section_1_timeIndex.write("환불 시간 : ")
    day1 = section_1_day.date_input(label="환불 날짜",label_visibility="collapsed")
    time1 = section_1_time.text_input(label="환불 시간",value=None,label_visibility="collapsed")
    section_1_costIndex.write("환불금액 : ")
    cost1 = section_1_cost.number_input(label="환불금액",value=None,step=1,label_visibility="collapsed")
    #정산 모계좌 정보
    bank3 = sec_3["010PAY"]["은행"]
    acount3 = sec_3["010PAY"]["계좌"]
    section_3_timeIndex.write("정산 시간 : ")
    day3 = section_3_day.date_input(label="정산 날짜",label_visibility="collapsed")
    time3 = section_3_time.text_input(label="정산 시간",value=None,label_visibility="collapsed")
st.write("### 기타정보")
aboutBuyIndex,aboutBuy,empty = st.columns(spec=[1,2,2],gap="small",vertical_alignment="center")
usedCostIndex,usedCost,empty = st.columns(spec=[1,2,2],gap="small",vertical_alignment="center")
returnCostIndex,returnCost,empty = st.columns(spec=[1,2,2],gap="small",vertical_alignment="center")
inCostIndex,inCost,empty = st.columns(spec=[1,2,2],gap="small",vertical_alignment="center")
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
section_2_costIndex.write("피해금 : ")
cost2 = section_2_cost.number_input(label="피해금",value=None,step=1,label_visibility="collapsed")
section_2_timeIndex.write("입금 시간 : ")
day2 = section_2_day.date_input(label="입금 날짜",label_visibility="collapsed")
time2 = section_2_time.text_input(label="입금 시간",value=None,label_visibility="collapsed")
#기타정보
aboutBuyIndex.write("실제사용처 : ")
aboutBuy = aboutBuy.text_input(label="실제사용처",value=None,label_visibility="collapsed")
usedCostIndex.write("이용 금액 : ")
usedCost = usedCost.number_input(label="이용금",value=None,step=1,label_visibility="collapsed")
returnCostIndex.write("환불(출금) 금액 : ")
returnCost = returnCost.number_input(label="환불금",value=None,step=1,label_visibility="collapsed")
inCostIndex.write("선불충전금 잔액 : ")
inCost = inCost.number_input(label="잔액",value=None,step=1,label_visibility="collapsed")
otherInfomationIndex.write("기타사항 : ")
antherInfo = otherInfomation.text_area(label="기타",value=None,label_visibility="collapsed")
antherInfo = antherInfo.replace("\n","<br>") if antherInfo is not None else ""
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
                        sec_2_cost=cost2,
                        sec_3_bank=bank3,
                        sec_3_acount=acount3,
                        sec_3_time=f"{day3}<br>{time3}",
                        AboutBuy=aboutBuy,
                        UsedCost=usedCost,
                        ReturnCost=returnCost,
                        InCost=inCost,
                        antherInfo=antherInfo,
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
    for i in faxInfo.keys():
        if i in sendbank:
            requests.get(f"https://api.telegram.org/bot{teleBot['token']}/sendMessage?chat_id={teleBot['chatId']}&text={faxInfo[i]}")
    else:pass