import streamlit as st
from jinja2 import Template
import pandas as pd

htmlForm = "C:\\Users\\USER\\ve_1\\samplePage\\htmlForm\\{servise}.html"
#선불 및 비선불 선택
option1,option2 = st.tabs(["선불","비선불"])
with option1:
    #선불가맹점 서비스
    servise = st.radio(label="서비스",options=["간편결제(내통장결제 포함)","VAN가상계좌","PG가상계좌","010PAY"])
    #간편,내통장
    if servise == "간편결제(내통장결제 포함)":
        st.write("1.재이전된 계좌 정보 입력")
        mid = st.selectbox(label="MID",options=["smile_r","M2060628"],index=None,placeholder="선택")
        section_1_bankIndex,section_1_bank,section_1_acountIndex,section_1_acount = st.columns(spec=[1,1,1,3],vertical_alignment="center")
        section_1_nameIndex,section_1_name,empty = st.columns(spec=[1,2,3],vertical_alignment="center")
        if mid == None:
            section_1_bankIndex.write("은행 : ")
            section_1_bank.text_input(label="재이전계좌 은행",value=None,label_visibility="collapsed")
            section_1_acountIndex.write("계좌 번호 : ")
            section_1_acount.number_input(label="재이전계좌 번호",value=None,step=1,label_visibility="collapsed")
            section_1_nameIndex.write("명의인 : ")
            section_1_name.text_input(label="재이전계좌 명의인",value=None,label_visibility="collapsed")
        else:
            section_1_bankIndex.write("은행: ")
            section_1_bank.write(mid)
            section_1_acountIndex.write("계좌 번호: ")
            section_1_acount.write(mid)
            section_1_nameIndex.write("명의인 : ")
            section_1_name.write(mid)
        st.write("2.입금 모계좌")
        section_2_bankIndex,section_2_bank,section_2_acountIndex,section_2_acount = st.columns(spec=[1,1,1,3],vertical_alignment="center")
        section_2_bankIndex.write("은행 : ")
        section_2_bank.text_input(label="입금계좌 은행",value=None,label_visibility="collapsed")
        section_2_acountIndex.write("계좌 번호 : ")
        section_2_acount.number_input(label="입금계좌 번호",value=None,step=1,label_visibility="collapsed")
        st.write("3.출금(정산) 모계좌")
        section_3_bankIndex,section_3_bank,section_3_acountIndex,section_3_acount = st.columns(spec=[1,1,1,3],vertical_alignment="center")
        section_3_bankIndex.write("은행 : ")
        section_3_bank.write(mid)
        section_3_acountIndex.write("계좌 번호 : ")
        section_3_acount.write(mid)
        st.write("4.피해정보")
        section_2_timeIndex,section_2_day,section_2_time,empty,empty = st.columns(spec=[1,1,1,1,1],vertical_alignment="center")
        section_1_timeIndex,section_1_day,section_1_time,empty,empty = st.columns(spec=[1,1,1,1,1],vertical_alignment="center")
        section_1_costIndex,section_1_cost,empty,empty = st.columns(spec=[1,2,1,1],vertical_alignment="center")
        section_2_timeIndex.write("입금 시간 : ")
        section_2_day.date_input(label="입금 날짜",label_visibility="collapsed")
        section_2_time.text_input(label="입금 시간",value=None,label_visibility="collapsed")
        section_1_timeIndex.write("정산 시간 : ")
        section_1_day.date_input(label="정산 날짜",label_visibility="collapsed")
        section_1_time.text_input(label="정산 시간",value=None,label_visibility="collapsed")
        section_1_costIndex.write("피해금 : ")
        section_1_cost.number_input(label="피해금",value=None,step=1,label_visibility="collapsed")
    #html_form 불러오기
    with open(htmlForm.format(servise="선불"),"r",encoding="UTF-8") as html:
        html = html.read()
    #jinja templete 변경 및 formating
    fax = Template(html).render(
        section_1_bank = "", #재이전 모계좌 은행
        section_1_acount = "", #재이전 모계좌 번호
        section_1_name = "", #재이전 가맹점
        section_1_time = "", #정산 시간
        section_1_cost = "", #피해금
        section_2_bank = "", #입금 은행
        section_2_acount = "", #입금 계좌
        section_2_time = "", #입금 시간
        section_3_bank = "", #정산 계좌 은행
        section_3_acount = "", #정산 계좌 번호
        trNum = "", #거래번호
        orNum = "", #주문번호
        otherInfomation = "", #특이사항
        sendBank = "", #수신 은행
        today = "" #발신 날짜
    )