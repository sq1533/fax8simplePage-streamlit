import os
import json
import streamlit as st
# 페이지 레이아웃 설정
st.set_page_config(page_title="자유게시판",initial_sidebar_state="expanded")
st.sidebar.title("자유게시판")
#게시판 DB 호출
boardPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","board.json")
#글 생성
def boardW(write:str):
    with open(boardPath, 'r', encoding='utf-8') as j:
        readBoards = json.load(j)
    number = str(len(readBoards)+1)
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
for i in range(2,len(readBoards)+1):
    with st.expander(label=readBoards[str(i)]["title"]):
        st.write(f"{str(i-1)}.{readBoards[str(i)]['title']}")
        for j in range(0,len(readBoards[str(i)]['comments'])):
            st.write(readBoards[str(i)]['comments'][j])
        comments = st.text_input(label=f"{str(i-1)}댓글",value=None,label_visibility="collapsed")
        empty,commB,delB = st.columns([6,1,1],vertical_alignment="top")
        if commB.button(label=f"{str(i-1)}댓글"):
            commentW(str(i),comments)
        if delB.button(label=f"{str(i-1)}삭제"):
            boardD(str(i))
empty,boardB = st.columns([7,1],vertical_alignment="top")
if boardB.button(label="글쓰기"):
    board()