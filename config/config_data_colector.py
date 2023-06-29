import json
import os
import pandas as pd
import streamlit as st

class DataProvider:
    __leftmenu_cf_dir = 'left_menu'
    __corporaSkipLst = ['Statistics']
    __rephr_sortDic = {'P':0,'I':1,'C':2,'D':3,'O':4}
    __rephr_dims = ['P','I','C','D','O']
    __color_sentiment = {'positive':'#3FEE0F','negative':'#FF0000','neutral':'#2EBDFF','No_Change': '#414040'}
    __color_ethos = {'Meliorization':'#3FEE0F','Pejorativization':'#FF0000','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_rephr = {'C': '#7FB3D5','D': '#76D7C4',
            'I':'#02FF70', 'O': '#F4D03F','P':'#C56EE7'}
    __color_rephr_empty = {'Rephrase': '#E9B711','No rephrase': '#706351'}

    __custom_stop_words = [
            "http", "https", "co", "RT",
            "Donald", "Trump", "Mike", "Pence",
            "Hillary","Hilary", "Clinton", "Joe", "Biden",
            "Michael", "Bloomberg", "Jeb", "Bush",
            "Ben", "Carson", "Lincoln" "Chafee",
            "Chris", "Christie", "Ted", "Cruz",
            "Carly", "Fiorina", "Obama", "OBAMA",
            "Jim", "Gilmore","Sanders'",
            "Lindsey", "Graham"
            "Mike", "Huckabee",
            "Bobby", "Jindal",
            "John", "Kasich",
            "Lawrence", "Lessig",
            "Martin", "O'Malley",
            "George", "Pataki",
            "Rand", "Paul",
            "Rick", "Perry",
            "Marco", "Rubio",
            "Bernie", "Sanders",
            "Rick", "Santorum",
            "Scott", "Walker",
            "Elizabeth", "Warren",
            "Jim", "Webb",
    ]

    @staticmethod
    def getRephraseDimentions():
        return DataProvider.__rephr_dims

    @staticmethod
    def getRephraseColors():
        return DataProvider.__color_rephr

    @staticmethod
    def getRephraseAndEmptycolors():
        return DataProvider.__color_rephr_empty
    
    @staticmethod
    def getSentimentColors():
        return DataProvider.__color_sentiment
    
    @staticmethod
    def getEthosColors():
        return DataProvider.__color_ethos

    @staticmethod
    def addSpacelines(number=2):
        for i in range(number):
            st.write("\n")

    @staticmethod
    def getCorporaSkipLst() -> list[str]:
        return DataProvider.__corporaSkipLst
    
    @staticmethod
    def getSortingDic() -> dict[str:int]:
        return DataProvider.__rephr_sortDic
    
    @staticmethod
    def getCustomStopWords() -> list[str]:
        return DataProvider.__custom_stop_words