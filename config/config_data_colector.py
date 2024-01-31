import json
import os
import streamlit as st

class DataProvider:
    __tableFormat = [
        {"selector": "", "props": [("border", "1px solid grey")]},
        {"selector": "tbody td", "props": [("border", "1px solid grey")]},
        {"selector": "th", "props": [("border", "2px solid black")]}
    ]

    __dyn_rephr_file = 'config/dyn_rephr_cfg.json'
    __lst_of_dyn_rephr = ['Amelioration', 'Pejorativization', 'Neutralization','No_Change']
    __lst_of_dyn_rephrWS = ['A_strong','A_weak','P_strong','P_weak','Neutralization','No_Change']
    __lst_of_dyn_in_out = ['input','output']
    __rephPSP_columns = ['inputPSP','outputPSP']
    __color_sentiment = {'Amelioration':'#3FEE0F','A_strong':'#28B900','A_weak':'#7CFF57','Pejorativization':'#FF0000'                     
                     ,'P_strong':'#BD0000','P_weak':'#FF5656','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_ethos = {'Amelioration':'#3FEE0F','A_strong':'#28B900','A_weak':'#7CFF57','Pejorativization':'#FF0000'
                     ,'P_strong':'#BD0000','P_weak':'#FF5656','Neutralization':'#2EBDFF','No_Change': '#414040'}
    __color_rephr = {'C': '#7FB3D5','D': '#76D7C4',
            'I':'#02FF70', 'O': '#F4D03F','P':'#C56EE7'}
    __color_rephr_empty = {'Rephrase': '#E9B711','No rephrase': '#706351'}

    __color_PoS ={
        "PROPN": '#B3B3B3',"AUX": '#47CCD3',"VERB": '#FF0000',"PRON": '#0008FF',"NOUN": '#51FF00',
        "CCONJ": '#dcb559',"ADP": '#f5bc6b',"DET": '#f5aa60',"PART": '#f39659',"ADJ": '#FF00FB',
        "NUM": '#ec6e55',"PUNCT": '#e65857',"ADV": '#D0FF00',"INTJ": '#501D5B',"SYM": '#2D157B',
        "SCONJ": '#2E3390',"SPACE": '#213766',"X": '#2A565C'
    }

    __3d_colors = {
        'F2F' : {'Amelioration':'#33FF99','A_strong':'#33FF66','A_weak':'#33FF99','Pejorativization':'#FF6600'
                     ,'P_strong':'#FF0033','P_weak':'#FF0066','Neutralization':'#0000FF','No_Change': '#A8A8A8',
                     "PROPN": '#488f31',"AUX": '#60994b',"VERB": '#76a263',"PRON": '#8bab7c',"NOUN": '#b3bdad',
                     "CCONJ": '#c6c6c6',"ADP": '#ceb2b2',"DET": '#d39d9d',"PART": '#d68889',"ADJ": '#d77276',
                     "NUM": '#d65a63',"PUNCT": '#de425b',"ADV": '#C442DE',"INTJ": '#883DDE',"SYM": '#633DDE',
                     "SCONJ": '#3D45DE',"SPACE": '#285FD5',"X": '#2EC6DD'},
        'Media': {'Amelioration':'#33CC33','A_strong':'#33CC33','A_weak':'#33CC66','Pejorativization':'#FF3300'
                     ,'P_strong':'#FF6600','P_weak':'#FF6666','Neutralization':'#0000CC','No_Change': '#909090',
                     "PROPN": '#488f31',"AUX": '#6f963d',"VERB": '#8e9e4f',"PRON": '#a7a564',"NOUN": '#bbae7c',
                     "CCONJ": '#cbb896',"ADP": '#d5c4b1',"DET": '#d6b397',"PART": '#d8a180',"ADJ": '#db8e6f',
                     "NUM": '#dd7862',"PUNCT": '#de5f5c',"ADV": '#875292',"INTJ": '#6D4576',"SYM": '#5841A4',
                     "SCONJ": '#6066DA',"SPACE": '#537CD4',"X": '#2EC6DD'                     
                     },
        'SocialMedia': {'Amelioration':'#33CC00','A_strong':'#33CC00','A_weak':'#33FF99','Pejorativization':'#FF0033'
                     ,'P_strong':'#FF3300','P_weak':'#FF3366','Neutralization':'#000099','No_Change': '#686868',
                     "PROPN": '#488f31',"AUX": '#6c9736',"VERB": '#8a9f3f',"PRON": '#a6a74b',"NOUN": '#c0ae5b',
                     "CCONJ": '#d7b66d',"ADP": '#edbf82',"DET": '#ecad72',"PART": '#eb9a66',"ADJ": '#ea865d',
                     "NUM": '#e87159',"PUNCT": '#e45b58',"ADV": '#de425b',"INTJ": '#6A2779',"SYM": '#361899',
                     "SCONJ": '#4047D5',"SPACE": '#4373D8',"X": '#22A1B5'                     
                     },
        'Total': {'Amelioration':'#336600','A_strong':'#336600','A_weak':'#339933','Pejorativization':'#CC0000'
                     ,'P_strong':'#CC0000','P_weak':'#CC0066','Neutralization':'#000066','No_Change': '#404040',
                     "PROPN": '#488f31',"AUX": '#6a9832',"VERB": '#89a036',"PRON": '#a6a73e',"NOUN": '#c1ae4a',
                     "CCONJ": '#dcb559',"ADP": '#f5bc6b',"DET": '#f5aa60',"PART": '#f39659',"ADJ": '#f18255',
                     "NUM": '#ec6e55',"PUNCT": '#e65857',"ADV": '#de425b',"INTJ": '#501D5B',"SYM": '#2D157B',
                     "SCONJ": '#2E3390',"SPACE": '#213766',"X": '#2A565C'                     
                     }
    }

    __3d_PSP = ["PROPN","AUX","VERB","PRON","NOUN","CCONJ","ADP","DET","PART","ADJ","NUM","PUNCT","ADV","INTJ","SYM","SCONJ","SPACE","X"]
    __3D_PSPdefalut = ["PROPN","AUX","VERB","PRON","NOUN","CCONJ","NUM"]
        
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
    def getTableFormat():
        return DataProvider.__tableFormat

    @staticmethod
    def getInOutColLst():
        return DataProvider.__lst_of_dyn_in_out

    @staticmethod
    def getPSPcolumns():
        return DataProvider.__rephPSP_columns

    @staticmethod
    def getPSPlst():
        return DataProvider.__3d_PSP

    @staticmethod
    def getPSPlstDefault():
        return DataProvider.__3D_PSPdefalut

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
    def getPoScolors():
        return DataProvider.__color_PoS

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