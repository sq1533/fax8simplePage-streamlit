import streamlit as st
import pandas as pd
#이미지 생성
def faxImage(data,filePath="image.png"):
    faxInfomation = pd.DataFrame(data,columns=[""])