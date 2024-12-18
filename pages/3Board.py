import os
import json
from datetime import datetime
import streamlit as st
# 페이지 레이아웃 설정
st.set_page_config(page_title="자유게시판",initial_sidebar_state="expanded")
st.sidebar.title("자유게시판")
#게시판 DB 호출
boardPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","DB","board.json")
picturePath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","picture")
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
n = 0
for i in list(readBoards.keys()):
    with st.expander(label=readBoards[i]["title"]):
        for j in range(0,len(readBoards[i]['comments'])):
            st.write(readBoards[i]['comments'][j])
        comments = st.text_input(label=f"{i}댓글",value=None,label_visibility="collapsed")
        empty,inputB,commB,delB = st.columns([5,1,1,1],vertical_alignment="top")
        inputPicture = st.file_uploader(label=f"{n}",type=['jpg','png','tif'],accept_multiple_files=False,label_visibility="collapsed")
        file_path = os.path.join(picturePath,f"{i}.png")
        if os.path.exists(file_path):
            st.image(image=file_path,caption=None,width=600,clamp=False,channels="RGB",output_format="auto",use_container_width=False)
            if st.button(label=f"{n}이미지제거"):
                os.remove(file_path)
                st.rerun()
        else:
            pass
        if inputPicture == None:
            pass
        else:
            with open(file_path, "wb") as f:
                f.write(inputPicture.getbuffer())
            st.rerun()
        if commB.button(label=f"{n}댓글"):
            commentW(i,comments)
        if delB.button(label=f"{n}삭제"):
            boardD(i)
    n = n+1
rerunB,empty,boardB = st.columns([3,3,1],vertical_alignment="top")
if boardB.button(label="글쓰기"):
    board()
if rerunB.button(label="새로고침"):
    st.rerun()