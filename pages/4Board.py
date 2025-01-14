import os
import json
from datetime import datetime
import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(page_title="자유게시판",initial_sidebar_state="expanded")
st.sidebar.title("자유게시판")

#게시판 DB path 호출
boardPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","board.json")

#글 생성
def boardW(write:str):
    with open(boardPath, 'r', encoding='utf-8') as j:
        readBoards = json.load(j)
    number = str(datetime.now().microsecond)
    readBoards[number] = {"title":write,"comments":[]}
    with open(boardPath, 'w', encoding='utf-8') as j:
        json.dump(readBoards, j, ensure_ascii=False, indent=4)
    st.rerun()

#댓글쓰기
def commentW(num:str,comm:str):
    with open(boardPath, 'r', encoding='utf-8') as j:
        readBoards = json.load(j)
    readBoards[num]["comments"].append(comm)
    with open(boardPath, 'w', encoding='utf-8') as j:
        json.dump(readBoards, j, ensure_ascii=False, indent=4)
    st.rerun()

#댓글삭제
def commentD(num:str,commnum:str):
    with open(boardPath, 'r', encoding='utf-8') as j:
        readBoards = json.load(j)
    readBoards[num]["comments"].pop(commnum)
    with open(boardPath, 'w', encoding='utf-8') as j:
        json.dump(readBoards, j, ensure_ascii=False, indent=4)
    st.rerun()

#글 삭제
def boardD(num:str):
    with open(boardPath, 'r', encoding='utf-8') as j:
        readBoards = json.load(j)
    del readBoards[num]
    with open(boardPath, 'w', encoding='utf-8') as j:
        json.dump(readBoards, j, ensure_ascii=False, indent=4)
    st.rerun()

#글 작성
@st.dialog(title="게시글 쓰기",width="large")
def board():
    writes = st.text_input(label="게시글 쓰기",value=None,label_visibility="collapsed")
    if st.button(label="개시"):
        boardW(write=writes)

#본문
with open(boardPath, 'r', encoding='utf-8') as j:
    readBoards = json.load(j)
rerunB1,empty,boardB1 = st.columns([3,3,1],vertical_alignment="top")
if rerunB1.button(label="새로고침l"):
    st.rerun()
if boardB1.button(label="글쓰기l"):
    board()

n = 0 #카테고리 no.

for i in list(readBoards.keys()):
    with st.expander(label=readBoards[i]["title"]):
        for j in range(0,len(readBoards[i]['comments'])):
            comment_,comdel = st.columns([4,1],vertical_alignment="top")
            comment_.write(readBoards[i]['comments'][j])
            comdelB = comdel.button(label=f"{j}댓글 삭제")
            if comdelB:
                commentD(i,j)
            else:
                pass
        #댓글 작성 후 초기화를 위한 세션
        if f"{i}text" not in st.session_state:
            st.session_state[f"{i}text"] = ''
        comment = st.text_input(label=f"{i}댓글",key=f"{i}text",label_visibility="collapsed")
        comments = f":gray[[{datetime.now().strftime('%m.%d. %H:%M')}]] {comment}"
        empty,delB = st.columns([5,1],vertical_alignment="top")
        btn = delB.button(label=f"{n}글삭제")
        if comment:
            if comment == '':
                st.error(body="입력값 없음")
            else:
                del st.session_state[f"{i}text"]
                commentW(i,comments)
        else:
            pass
        if btn:
            boardD(i)
        else:
            pass
    n = n+1

rerunB2,empty,boardB2 = st.columns([3,3,1],vertical_alignment="top")
if rerunB2.button(label="새로고침I"):
    st.rerun()
if boardB2.button(label="글쓰기I"):
    board()