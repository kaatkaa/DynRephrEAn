import json
import os
import streamlit as st

class DataProvider:
    __dyn_rephr_file = 'config/dyn_rephr_cfg.json'
    __lst_of_dyn_rephr = ['Meliorization', 'Pejorativization', 'Neutralization','No_Change']
    __lst_of_dyn_rephrWS = ['M_strong','M_weak','P_strong','P_weak','Neutralization','No_Change']
    __color_sentiment = {'Meliorization':'#3FEE0F','M_strong':'#7CFF57','M_weak':'#28B900','Pejorativization':'#FF0000'
                     ,'P_strong':'#FF5656','P_weak':'#BD0000','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_ethos = {'Meliorization':'#3FEE0F','M_strong':'#7CFF57','M_weak':'#28B900','Pejorativization':'#FF0000'
                     ,'P_strong':'#FF5656','P_weak':'#BD0000','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_rephr = {'C': '#7FB3D5','D': '#76D7C4',
            'I':'#02FF70', 'O': '#F4D03F','P':'#C56EE7'}
    __color_rephr_empty = {'Rephrase': '#E9B711','No rephrase': '#706351'}
        
    __sav_image = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'presentation_image',
            'height': 1080,
            'width': 1180,
            'scale':6 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    __custom_stop_words = [
            "http", "https", "co", "RT",
            "Donald", "Trump", "Mike", "Pence",
            "Hillary","Hilary", "Clinton", "Joe", "Biden",
            "Michael", "Bloomberg", "Jeb", "Bush","Nicholas", "Ridley",
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
            "Jim", "Webb","Mr"
    ]

    @staticmethod
    def getDynRephrESconfig():
        try:
            DataProvider.__config_dic
        except AttributeError:
            with open(DataProvider.__dyn_rephr_file) as json_file:
                DataProvider.__config_dic = json.load(json_file)
        return DataProvider.__config_dic

    @staticmethod
    def getDynRephDimentions():
        return DataProvider.__lst_of_dyn_rephr

    @staticmethod
    def getDynRephDimentionsWS():
        return DataProvider.__lst_of_dyn_rephrWS

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
    def getCustomStopWords() -> list[str]:
        return DataProvider.__custom_stop_words
    
    @staticmethod
    def getSaveConfig() -> dict[str, any]:
        return DataProvider.__sav_image