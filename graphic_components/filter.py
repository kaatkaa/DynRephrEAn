import streamlit as st
import sys
import pandas as pd
import numpy as np
import re
from operator import itemgetter
from typing import Tuple, List, Dict, Any
from wordcloud import STOPWORDS


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class Filter:

    __config: Dict[str, Any]={
        'generalConfig':DataProvider.getDynRephrESconfig()['DynRephAn for Sentiment'],
        'prefix':'no_prefix',
        'column': "",
        'showUnits': True,
        'units': ("Percentage","Number"),
        'unit': 'Percentage',
        'showCategoriesInterface': True,
        'categoriesInterfaceTitle': 'Wordcloud_filterInterface',
        'AnalysisUnit': "",
        'SS rephrase': True,
        'OS rephrase': False,
        'showInOutInterface': True,
        'inOutLst': DataProvider.getInOutColLst(),
        'palette': DataProvider.getEthosColors(),
        'showStopWordsInterface':True,
        'showStopwords':False,
        'useStopwords':True,
        'showPOSInterface':False
    }

    def __RemoveStopWordsFromDf(self, dataF: Any, columns: list[str]) -> Any:
        for stop_phrase in self.__stop_words_set:
            p1 = re.compile(r"\s"+stop_phrase+r"\s", flags=re.IGNORECASE)
            p2 = re.compile(r"^"+stop_phrase+r"\s|\s"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.IGNORECASE)
            for column in columns:
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        self.__outputData = dataF

    def __init__(self, data: Any, config: Dict[str, Any]) -> None:
        self.__cf=Filter.__config
        if len(data) > 0:
            for cfg in config.items():
                self.__cf[cfg[0]] = cfg[1]
            self.__stop_words_set = set()
            if self.__cf['showStopWordsInterface']:
                for word in DataProvider.getCustomStopWords():
                    self.__stop_words_set.add(word)
                for word in list(STOPWORDS):
                    self.__stop_words_set.add(word)
            self.__keyCtr = 0
            self.__d = data
            self.__outputData = data.copy(deep=True)
            self.__outDict = dict()
            self.__filterInterface()
        else:
            self.__outDict = dict()

    def getData(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        return self.__outDict, self.__cf

    def __filterInterface(self) -> Tuple[Any, list[str]]:
        def _OS():
            self.__cf['OS rephrase'] = not self.__cf['OS rephrase']
        def _SS():
            self.__cf['SS rephrase'] = not self.__cf['SS rephrase']
        column = ""
        col_radio1, col_radio2, col_chckbox1= st.columns(3)

        if self.__cf['showUnits']:
            with col_radio1:
                self.__units()
            
        if self.__cf['showCategoriesInterface']:
            column = self.__categories(col_radio2)
            self.__cf['column'] = column
        else:
            self.__outputData = self.__d

        if self.__cf['AnalysisUnit'] == 'Speaker-Based Analysis':
            with col_chckbox1:
                st.checkbox("SS rephrase",
                    value=self.__cf['SS rephrase'],
                    key=self.__cf['prefix']+"_SS"+str(self.__keyCtr),
                    on_change=_SS)
                self.__keyCtr += 1
                st.checkbox("OS rephrase",
                    value=self.__cf['OS rephrase'],
                    key=self.__cf['prefix']+"_OS"+str(self.__keyCtr),
                    on_change=_OS)
                self.__keyCtr += 1
        
        if self.__cf['showInOutInterface']:
            self.__inOut()

        if self.__cf['showStopWordsInterface']:
            self.__stopWords()

        if self.__cf['showPOSInterface']:
            self.__cf['palette'] = DataProvider.getPoScolors()
            self.__PoSinterface()
        else:
            self.__cf['palette'] = DataProvider.getEthosColors()
            if self.__cf['AnalysisUnit'] == 'Speaker-Based Analysis':
                if self.__cf['SS rephrase']:
                    self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
                    self.__outDict["gruppedSS"] = self.__distributionData(self.__outDict["wholeSS"], column)
                if self.__cf['OS rephrase']:
                    self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
                    self.__outDict["gruppedOS"] = self.__distributionData(self.__outDict["wholeOS"], column)
            else:
                self.__outDict["wholeAll"] = self.__outputData
                self.__outDict["gruppedAll"] = self.__distributionData(self.__outputData, column)

    def __units(self):
        self.__cf['unit'] = st.radio("Choose units",
            self.__cf['units'],                                                
            key=self.__cf['prefix']+"_Units"+str(self.__keyCtr))
        self.__keyCtr += 1
        
    def __categories(self, col) -> str:
        with col:
            display_complexity = st.radio(self.__cf['generalConfig'][self.__cf['categoriesInterfaceTitle']],
                ("4-categories",
                    "6-categories"),                                                 
                key=self.__cf['prefix']+"_Rephrase_4-6cat"+str(self.__keyCtr))
            self.__keyCtr += 1
        if display_complexity == '4-categories':
            dyn_rephrase_options = st.multiselect(self.__cf["generalConfig"]["Wordcloud_filterInterface"], 
                                        sorted(DataProvider.getDynRephDimentions()), 
                                        sorted(DataProvider.getDynRephDimentions())[:],
                                        key = self.__cf['prefix']+"_multi_sel"+str(self.__keyCtr))
            self.__keyCtr += 1
            column = self.__cf['generalConfig']['colName']
            self.__outputData = self.__d.loc[self.__d[column].isin(dyn_rephrase_options)]
            return column
        elif display_complexity == '6-categories':
            dyn_rephrase_options = st.multiselect(self.__cf['generalConfig']["Wordcloud_filterInterface"], 
                                        sorted(DataProvider.getDynRephDimentionsWS()), 
                                        sorted(DataProvider.getDynRephDimentionsWS())[:],
                                        key = self.__cf['prefix']+"_multi_selWS"+str(self.__keyCtr))
            self.__keyCtr += 1
            column = self.__cf['generalConfig']['colNameWS']
            self.__outputData = self.__d.loc[self.__d[column].isin(dyn_rephrase_options)]
            return column
        else:
            st.error("Oprion not implemented in __filterInterface, class: WordCloudOfEmotions")

    def __inOut(self):
        self.__cf['inOutLst'] = st.multiselect("Choose source of data you would like to visualise", 
                                    DataProvider.getInOutColLst(), 
                                    DataProvider.getInOutColLst()[:],
                                    key = self.__cf['prefix']+"_multi_selInOut"+str(self.__keyCtr))
        self.__keyCtr += 1

    def __stopWords(self):
        col1, col2 = st.columns([2,2])
        with col1:
            useStopWords = st.checkbox(label="Enable stop_words",
                                        value=self.__cf['useStopwords'],
                                        key=self.__cf['prefix']+"_StopWordsChck"+str(self.__keyCtr),
                                        )
            self.__keyCtr += 1
        with col2:
            showStopWords = st.checkbox(label="Show stop_words",
                                        value=self.__cf['showStopwords'],
                                        key=self.__cf['prefix']+"_ShowWordsChck"+str(self.__keyCtr)
                                        )
            self.__keyCtr += 1
        if showStopWords:
            st.write(self.__stop_words_set)
        if useStopWords:
            self.__RemoveStopWordsFromDf(self.__outputData, DataProvider.getInOutColLst())
    
    def __PoSinterface(self):
        def dfFromDic(col1Name: str, col2Name: str, dict: Dict[str, Any]):
            lstOfTuples = []
            for item in dict.items():
                lstOfTuples.append(item)
            lstOfTuples = sorted(lstOfTuples,key=itemgetter(0))
            lst1, lst2 = [l[0] for l in lstOfTuples], [l[1] for l in lstOfTuples]
            return pd.DataFrame.from_dict({col1Name:lst1,col2Name:lst2})
        inOutPOS = st.multiselect(self.__cf['generalConfig']['POS_inOut'], 
                                    sorted(DataProvider.getPSPcolumns()), 
                                    sorted(DataProvider.getPSPcolumns())[:],
                                    key = self.__cf['prefix']+"_multiInOutPOS"+str(self.__keyCtr))
        self.__keyCtr += 1
        POS_filter = st.multiselect(self.__cf['generalConfig']['POS_title'], 
                                    sorted(DataProvider.getPSPlst()), 
                                    sorted(DataProvider.getPSPlstDefault())[:],
                                    key = self.__cf['prefix']+"_multiPOS"+str(self.__keyCtr))
        self.__keyCtr += 1
        if self.__cf['AnalysisUnit'] == 'Speaker-Based Analysis':
            self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
            self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
            self.__outDict["gruppedSS"] = dfFromDic(
                "PoS_type",
                self.__cf['unit'],
                self.__posData(data=self.__outDict['wholeSS'],inOutPOS=inOutPOS,POS_filter=POS_filter)
            )
            self.__outDict["gruppedOS"] = dfFromDic(
                 "PoS_type",
                self.__cf['unit'],
                self.__posData(data=self.__outDict['wholeOS'],inOutPOS=inOutPOS,POS_filter=POS_filter)               
            )
        else:
            self.__outDict["wholeAll"] = self.__outputData
            self.__outDict["gruppedAll"] = dfFromDic("PoS_type",self.__cf['unit'],
                self.__posData(data=self.__outDict['wholeAll'],inOutPOS=inOutPOS,POS_filter=POS_filter))

    def __distributionData(self, data, column):
        if self.__cf['unit'] == "Percentage":
            return DataManipulator.getGruppedPercentages(d=data, 
                denominator=len(data),
                groupBy=column,
                col_name="Percentage")
        elif self.__cf['unit'] == "Number":
            return DataManipulator.getGruppedData(d=data,
                groupBy=column,
                col_name="Number")
        else:
            st.error("Wrong option: ",self.__cf['unit']," for __distributionData!")

    def __posData(self, data, inOutPOS, POS_filter):
        if self.__cf['unit'] == "Percentage":
            return DataManipulator.getTagsPercentageFreq(d=data,
                colLst=inOutPOS,
                PSPset=set(POS_filter))
        elif self.__cf['unit'] == "Number":
            return DataManipulator.getTagsFreq(d=data,
                colLst=inOutPOS,
                PSPset=set(POS_filter))
        else:
            st.error("Wrong option: ",self.__cf['unit']," for __posData!")