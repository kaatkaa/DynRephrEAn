import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.data as pdata
from typing import Dict
#from data_display.barchart3d import barchart3d
from wordcloud import STOPWORDS
from pandas.api.types import CategoricalDtype
from typing import Tuple
from nltk.util import ngrams
from nltk import FreqDist
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from data_display.display_data_in_3d import ThreeD_Charts

class ThreeDCorpusMenu:

    def __RemoveStopWordsFromDf(self, dataF: pd.DataFrame(), columns: list[str]) -> pd.DataFrame:
        for stop_phrase in self.__stop_words_set:
            p1 = re.compile(r"\s"+stop_phrase+r"\s", flags=re.IGNORECASE)
            p2 = re.compile(r"^"+stop_phrase+r"\s|\s"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.IGNORECASE)
            for column in columns:
                #dataF[column].str.lower()
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        return dataF
    
    def __onFilterChange(self, lst: list[str], colName = "") -> None:
        if colName == self.__anCfg['colName']:
            if str(self.__prefix + 'filterLst') in st.session_state:
                st.session_state[str(self.__prefix + 'filterLst')] = lst
                self.__filterLst = lst
            else:
                st.error("Sesion state not set for function: ",self.__onFilterChange.__name__)
        elif colName == self.__anCfg['colNameWS']:
            if str(self.__prefix + 'filterLstSW') in st.session_state:
                st.session_state[str(self.__prefix + 'filterLstSW')] = lst
                self.__filterLstSW = lst
            else:
                st.error("Sesion state SW not set for function: __onFilterChange")
        else:
            st.error("Wrong column option in __onFilterChange.")

    def __filterAPNNch(self) -> Tuple[any, list[str]]:
        col_radio1, = st.columns(1)
        def get_new_values_list(key: str="", colName: str=""):
            self.__onFilterChange(st.session_state[key],colName=colName)
        def set_show_stopwords(key: str):
            self.__showStopWords = st.session_state[key]
            if self.__showStopWords:
                st.title("Stop words: ")
                st.write(self.__stop_words_set)
        def set_use_stopwords(key: str):
            self.__useStopWords = st.session_state[key]
        col1, col2 = st.columns([2,2])
        with col1:
            st.checkbox(label="Enable stop_words",
                value=self.__useStopWords,
                on_change=set_use_stopwords,
                kwargs={'key': str(self.__prefix)+"StopWordsChck"},
                key=str(self.__prefix)+"StopWordsChck")
        with col2:
            st.checkbox(label="Show stop_words",
                value=self.__showStopWords,
                on_change=set_show_stopwords,
                kwargs={'key': str(self.__prefix)+"ShowWordsChck"},
                key=str(self.__prefix)+"ShowWordsChck")
        dyn_rephrase_options = []
        colName = ""
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: WordCloudOfEmotions",
                ("4-categories",
                    "6-categories"),                                                 
                key="Rephrase_Piechart_ADU_4-6cat")
        if display_complexity == '4-categories':
            colName = self.__anCfg['colName']
            dyn_rephrase_options = st.multiselect(self.__anCfg["Wordcloud_filterInterface"], 
                                        default=list(self.__filterLst),
                                        options=list(DataProvider.getDynRephDimentions()),
                                        on_change=get_new_values_list,
                                        kwargs={'key': str(self.__prefix)+"1multi_sel",'colName':colName},
                                        key = str(self.__prefix)+"1multi_sel")
        elif display_complexity == '6-categories':
            colName = self.__anCfg['colNameWS']
            dyn_rephrase_options = st.multiselect(self.__anCfg["Wordcloud_filterInterface"], 
                                        default=list(self.__filterLstSW),
                                        on_change=get_new_values_list,
                                        kwargs={'key': str(self.__prefix)+"2multi_sel",'colName':colName},
                                        options=list(DataProvider.getDynRephDimentionsWS()),
                                        key = str(self.__prefix)+"2multi_sel")
        else:
            st.warning("Option not implemented in __filterInterface, class: WordCloudOfEmotions")
        return dyn_rephrase_options, colName

    def __loader(self, mySet: set[str]):
        tmp = pd.DataFrame()
        for ddf in self.__dataDic.items():
            if ddf[0] in mySet:
                tmp = pd.concat([ddf[1], tmp])
        tmp.reset_index(inplace=True)
        return tmp

    def __prepCorpora_and_DynRephType(self) -> Dict[str, Dict[str, int]]:
        corpus3Ddic = {
             'Total': {'US2016redditD1','US2016redditR1','US2016redditG1','US2016tvD1','US2016tvR1','US2016tvG1','Hansard'},
             'SocialMedia': {'US2016redditD1','US2016redditR1','US2016redditG1'},
             'Media': {'US2016tvD1','US2016tvR1','US2016tvG1'},
             'F2F': {'Hansard'}
        }
        filterLst, dataColumn = self.__filterAPNNch()
        dic3D = {}
        for item in corpus3Ddic.items():
            tmpDf = DataManipulator.getGruppedData(self.__loader(item[1]),dataColumn,"Frequency")
            tmpDf = tmpDf.set_index(dataColumn)
            tmpDict = tmpDf.to_dict('index')
            dic3D[item[0]] = dict()
            #st.write(tmpDict)
            for dyn in filterLst:
                #st.write(tmpDict)
                if dyn in tmpDict:
                    dic3D[item[0]][dyn] = tmpDict[dyn]
                else:
                    dic3D[item[0]][dyn] = {'Frequency': 0}
        return dic3D

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="3D_", anType: str="DynRephAn for Ethos") -> None:
            self.__prefix = prefix
            self.__stop_words_set = set()
            self.__showStopWords = False
            self.__useStopWords = True
            for word in DataProvider.getCustomStopWords():
                self.__stop_words_set.add(word)
            for word in list(STOPWORDS):
                self.__stop_words_set.add(word)
            if str(self.__prefix + 'filterLst') in st.session_state:
                self.__filterLst = st.session_state[str(self.__prefix + 'filterLst')]
            else:
                self.__filterLst = DataProvider.getDynRephDimentions()
                st.session_state[self.__prefix + 'filterLst'] = self.__filterLst
            if str(self.__prefix + 'filterLstSW') in st.session_state: 
                self.__filterLstSW = st.session_state[str(self.__prefix + 'filterLstSW')]
            else:
                self.__filterLstSW = DataProvider.getDynRephDimentionsWS()
                st.session_state[str(self.__prefix + 'filterLstSW')] = self.__filterLst
            if str(self.__prefix)+"ShowWordsChck" in st.session_state:
                self.__showStopWords = st.session_state(str(self.__prefix)+"ShowWordsChck")
            else:
                st.session_state[str(self.__prefix)+"ShowWordsChck"] = self.__showStopWords
            if str(self.__prefix)+"StopWordsChck" in st.session_state:
                self.__useStopWords = st.session_state[str(self.__prefix)+"StopWordsChck"]
            else:
                st.session_state[str(self.__prefix)+"StopWordsChck"] = self.__useStopWords
            self.__plotData1 = None
            #dictionary containing all possible data with corpora indexed by name
            self.__dataDic = dataDic
            #Prefix to distinguish between different data sets
            #loading config file for ethos and sentiment
            tmp = DataProvider.getDynRephrESconfig()
            #config file with messages and column names for Ethos and Sentiment
            self.__anCfg = tmp[anType]

    def __RemoveStopWordsFromDf(self, dataF: pd.DataFrame(), columns: list[str]) -> pd.DataFrame:
        for stop_phrase in self.__stop_words_set:
            p1 = re.compile(r"\s"+stop_phrase+r"\s", flags=re.IGNORECASE)
            p2 = re.compile(r"^"+stop_phrase+r"\s|\s"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.IGNORECASE)
            for column in columns:
                #dataF[column].str.lower()
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        return dataF
    
    def draw3D(self):
        self.__plotData1 = self.__prepCorpora_and_DynRephType()
        #print("*******************************")
        ploter = ThreeD_Charts()
        ploter.CorporaVsDynRephrasePlot(self.__plotData1,
                                        "Corpora VS DynamicRephType distribution",
                                        "Color Scale"
                                        )
        #st.write(self.__plotData1)
        #print("*******************************")
