import json
import os
import streamlit as st

class DataProvider:
    __dyn_rephr_file = 'config/dyn_rephr_cfg.json'
    __lst_of_dyn_rephr = ['Amelioration', 'Pejorativization', 'Neutralization','No_Change']
    __lst_of_dyn_rephrWS = ['A_strong','A_weak','P_strong','P_weak','Neutralization','No_Change']
    __color_sentiment = {'Amelioration':'#3FEE0F','A_strong':'#28B900','A_weak':'#7CFF57','Pejorativization':'#FF0000'
                     ,'P_strong':'#BD0000','P_weak':'#FF5656','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_ethos = {'Amelioration':'#3FEE0F','A_strong':'#28B900','A_weak':'#7CFF57','Pejorativization':'#FF0000'
                     ,'P_strong':'#BD0000','P_weak':'#FF5656','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_rephr = {'C': '#7FB3D5','D': '#76D7C4',
            'I':'#02FF70', 'O': '#F4D03F','P':'#C56EE7'}
    __color_rephr_empty = {'Rephrase': '#E9B711','No rephrase': '#706351'}

    __3d_colors = {
        'F2F' : {'Amelioration':'#33FF99','A_strong':'#33FF66','A_weak':'#33FF99','Pejorativization':'#FF6600'
                     ,'P_strong':'#FF0033','P_weak':'#FF0066','Neutralization':'#0000FF','No_Change': '#A8A8A8'},
        'Media': {'Amelioration':'#33CC33','A_strong':'#33CC33','A_weak':'#33CC66','Pejorativization':'#FF3300'
                     ,'P_strong':'#FF6600','P_weak':'#FF6666','Neutralization':'#0000CC','No_Change': '#909090'},
        'SocialMedia': {'Amelioration':'#33CC00','A_strong':'#33CC00','A_weak':'#33FF99','Pejorativization':'#FF0033'
                     ,'P_strong':'#FF3300','P_weak':'#FF3366','Neutralization':'#000099','No_Change': '#686868'},
        'Total': {'Amelioration':'#336600','A_strong':'#336600','A_weak':'#339933','Pejorativization':'#CC0000'
                     ,'P_strong':'#CC0000','P_weak':'#CC0066','Neutralization':'#000066','No_Change': '#404040'}
    }
        
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
            "http", "https", "co", "rt",
            "donald", "trump", "mike", "pence",
            "hillary","hilary", "clinton", "joe", "biden",
            "michael", "bloomberg", "jeb", "bush","nicholas", "ridley",
            "ben", "carson", "lincoln" "chafee",
            "chris", "christie", "ted", "cruz",
            "carly", "fiorina", "obama", "obama",
            "jim", "gilmore",
            "lindsey", "graham"
            "mike", "huckabee",
            "bobby", "jindal",
            "john", "kasich",
            "lawrence", "lessig",
            "martin", "o'malley",
            "george", "pataki",
            "rand", "paul",
            "rick", "perry",
            "marco", "rubio",
            "bernie", "sanders",
            "rick", "santorum",
            "scott", "walker",
            "elizabeth", "warren",
            "jim", "webb","mr"
    ]

    @staticmethod
    def get3D_ColorMatrix():
        return DataProvider.__3d_colors

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