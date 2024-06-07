import streamlit as st
import sys
import pandas as pd
import re
import ast
from operator import itemgetter
from typing import Tuple, List, Dict, Any, Set
from streamlit_modal import Modal


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class DataFilter:

    __debug = False

    __config: Dict[str, Any]={
        'generalConfig':DataProvider.getDynRephrESconfig()['DynRephAn for Sentiment'],
        'prefix':'no_prefix_set_',
        # imediatePlot - set to True if plotting single corpora charts 
        # - to False if plotting in comparative analysis charts
        'imediatePlot': True,
        'showPercentageNumber': False,
        'unitPercentNumber': 'Percentage',
        'unitsPercentageNumber': ('Percentage','Number'),
        'showCategoriesInterface': False,
        'categoriesColumn': '',
        'categoriesLst': DataProvider.getDynRephDimentions(),
        'categoriesInterfaceTitle': 'Wordcloud_filterInterface',
        'ADU_or_Speaker': '',
        'SS rephrase': False,
        'OS rephrase': False,
        'showInOutInterface': True,
        'inOutLst': DataProvider.getInOutColLst(),
        'palette': DataProvider.getEthosColors(),
        'showStopWordsInterface':False,
        'showStopwords':False,
        'useStopwords':False,
        'stopPoSSet': set (),
        'usePoSSet': False,
        'StopwordsSet': set(),
        'showPOSInterface':False,
        # 'posColumns': DataProvider.getPSPcolumns1(),
        'posCategories': DataProvider.getPoSlst(),
        'showNgramSlider': False,
        'ngramSliderValue': 2
    }

    def __RemoveStopWordsFromDf(self, dataF: Any, columns: List[str], stopwords_set: Set[str]) -> None:
        for stop_phrase in stopwords_set:
            p1 = re.compile(r"\s+"+stop_phrase+r"\s+", flags=re.I|re.S)
            p2 = re.compile(r"^"+stop_phrase+r"\s+|\s+"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.I|re.S)
            for column in columns:
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        self.__outputData = dataF

    def __RemoveStopPoSFromDf(self, dataF: Any, columns: List[str], stopPoS_set: Set[str]) -> None:
        for column in columns:
            modColumn = []
            for line in dataF[column].tolist():
                line = ast.literal_eval(line)
                modLine = []
                for pos in line:
                    if pos not in stopPoS_set:
                        modLine.append(pos)
                modColumn.append(modLine)
            dataF[column] = modColumn
        self.__outputData = dataF

    def __init__(self, data: Any, config: Dict[str, Any]) -> None:
        self.__cf=DataFilter.__config
        self.__stop_words_set = self.__cf['StopwordsSet']
        self.__ngramLst = []
        self.__PoS_Dict = {}
        if DataFilter.__debug:
            open_modal = False
            open_modal = st.button(key="debug config button", label='debuf_fData')
            modal = Modal(key="Debugger_fData", title="Check config selected settings")
        if len(data) > 0:
            if DataFilter.__debug and open_modal:
                with modal.container():
                    st.markdown("config['showPOSInterface'] = "+str(config['showPOSInterface']))
                    open_modal = st.button(key="modal_debug_closer", label='Close debug info')
            for cfg in config.items():
                self.__cf[cfg[0]] = cfg[1]
            self.__d = data
            self.__outputData = data.copy(deep=True)
            self.__outDict = dict()
            self.__filterInterface()
        else:
            self.__outputData = data
            self.__outDict = data

    def getDataDict(self) -> Dict[str, Any]:
        return self.__outDict
    
    def getNgramLst(self) -> List[Tuple[str, int]]:
        return self.__ngramLst
    
    def getPoS_Dict(self) -> Dict[str, Any]:
        return self.__PoS_Dict
        
    def __filterInterface(self) -> Tuple[Any, list[str]]:
            
        if self.__cf['showCategoriesInterface'] and len(self.__outputData) > 0:
            if self.__cf['categoryIndex'] == 0:
                self.__outputData = self.__outputData.loc[self.__outputData[self.__cf['categoriesColumn']].isin(self.__cf['categoriesLst'])]
            elif self.__cf['categoryIndex'] == 1:
                self.__outputData = self.__outputData.loc[self.__outputData[self.__cf['categoriesColumn']].isin(self.__cf['categoriesLstWS'])]
        else:
            self.__outputData = self.__d

        if self.__cf['showStopWordsInterface'] and self.__cf['useStopwords'] and len(self.__outputData) > 0:
            self.__RemoveStopWordsFromDf(self.__outputData, self.__cf['inOutLst'], self.__stop_words_set)

        if self.__cf['showStopPoSInterface']:
            self.__RemoveStopPoSFromDf(self.__outputData, self.__cf['inOutLst'], self.__cf['stopPoSSet'])

        if DataFilter.__debug:
            open_modal = False
            open_modal = st.button(key="modal_button", label='button')
            modal = Modal(key="Modal_test", title="showPOSInterface enabled.")
            if open_modal:
                with modal.container():
                    st.markdown("self.__cf['showPOSInterface'] = "+str(self.__cf['showPOSInterface']))
                    open_modal = st.button(key="modal_close_button", label='Close modal')

        if self.__cf['showPOSInterface'] and len(self.__outputData) > 0:
            self.__cf['palette'] = DataProvider.getPoScolors()
            self.__PoSinterface()
        else:
            if self.__cf['imediatePlot']:
                self.__cf['palette'] = DataProvider.getEthosColors()
                if self.__cf['ADU_or_Speaker'] == 'Text-Based Analysis':
                    #st.write("Same speaker rephrase: "+str(self.__cf['SS rephrase'])+" Other speaker rephrase: "+str(self.__cf['OS rephrase']))
                    if self.__cf['SS + OS rephrase']:
                        self.__outDict["whole SS + OS"] = self.__outputData
                        self.__outDict["grupped SS + OS"] = self.__distributionData(self.__outputData, self.__cf['categoriesColumn']) 
                    if self.__cf['SS rephrase']:
                        self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
                        self.__outDict["gruppedSS"] = self.__distributionData(self.__outDict["wholeSS"], self.__cf['categoriesColumn'])
                    if self.__cf['OS rephrase']:
                        self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
                        self.__outDict["gruppedOS"] = self.__distributionData(self.__outDict["wholeOS"], self.__cf['categoriesColumn'])
            else:
                self.__outDict["wholeAll"] = self.__outputData
                self.__outDict["gruppedAll"] = self.__distributionData(self.__outputData, self.__cf['categoriesColumn']) 
                
    def __PoSinterface(self):
        def dfFromDic(col1Name: str, col2Name: str, dict: Dict[str, Any]):
            lstOfTuples = []
            for item in dict.items():
                lstOfTuples.append(item)
            lstOfTuples = sorted(lstOfTuples,key=itemgetter(0))
            cnv = DataProvider.getPoStagsConverter()
            lst1, lst2, lst3 = [l[0] for l in lstOfTuples], [l[1] for l in lstOfTuples], [cnv[l[0]] for l in lstOfTuples]
            return pd.DataFrame.from_dict({col1Name:lst1,col2Name:lst2,"PoS full name":lst3})
        if self.__cf['imediatePlot']:
            # if self.__cf['ADU_or_Speaker'] == 'Text-Based Analysis':
            if self.__cf['SS + OS rephrase']:
                self.__outDict["whole SS + OS"]=self.__outputData
                self.__PoS_Dict["SS + OS"] = self.__posData(data=self.__outDict['whole SS + OS'],inOutPOS=self.__cf['inOutLst'],POS_filter=self.__cf['posCategories'])
                self.__outDict["grupped SS + OS"] = dfFromDic(
                    "PoS_type",
                    self.__cf['unitPercentNumber'],
                    self.__PoS_Dict["SS + OS"][0]
                )
            if self.__cf['SS rephrase']:
                self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
                self.__PoS_Dict["SS"] = self.__posData(data=self.__outDict['wholeSS'],inOutPOS=self.__cf['inOutLst'],POS_filter=self.__cf['posCategories'])
                self.__outDict["gruppedSS"] = dfFromDic(
                    "PoS_type",
                    self.__cf['unitPercentNumber'],
                    self.__PoS_Dict["SS"][0]
                )
            if self.__cf['OS rephrase']:
                self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
                self.__PoS_Dict["OS"] = self.__posData(data=self.__outDict['wholeOS'],inOutPOS=self.__cf['inOutLst'],POS_filter=self.__cf['posCategories'])
                self.__outDict["gruppedOS"] = dfFromDic(
                    "PoS_type",
                    self.__cf['unitPercentNumber'],
                    self.__PoS_Dict["OS"][0]               
                )
            # else:
            #     self.__outDict["wholeAll"] = self.__outputData
            #     self.__outDict["gruppedAll"] = dfFromDic("PoS_type",self.__cf['unitPercentNumber'],
            #         self.__posData(data=self.__outputData,inOutPOS=self.__cf['posColumns'],POS_filter=self.__cf['posCategories']))
        else:
            self.__outDict["wholeAll"] = self.__outputData
            self.__PoS_Dict["CMP"] = self.__posData(data=self.__outDict['wholeAll'],inOutPOS=self.__cf['inOutLst'],POS_filter=self.__cf['posCategories'])
            self.__outDict["gruppedAll"] = dfFromDic("PoS_type",self.__cf['unitPercentNumber'],
                self.__PoS_Dict["CMP"][0]
                )

    def __distributionData(self, data, column):
        if self.__cf['unitPercentNumber'] == "Percentage":
            return DataManipulator.getGruppedPercentages(d=data, 
                denominator=len(data),
                groupBy=column,
                col_name="Percentage")
        elif self.__cf['unitPercentNumber'] == "Number":
            return DataManipulator.getGruppedData(d=data,
                groupBy=column,
                col_name="Number")
        else:
            st.error("Wrong option: "+self.__cf['unitPercentNumber']+" for __distributionData!")

    def __posData(self, data, inOutPOS, POS_filter):
        if self.__cf['unitPercentNumber'] == "Percentage":
            return DataManipulator.getSpacyPoSTagsFreq(data,
                inOutPOS,
                set(POS_filter),self.__cf['posTagType'],percentage=True)
        elif self.__cf['unitPercentNumber'] == "Number":
            return DataManipulator.getSpacyPoSTagsFreq(data,
                inOutPOS,
                set(POS_filter),self.__cf['posTagType'],percentage=False)
        else:
            st.error("Wrong option: "+self.__cf['unitPercentNumber']+" for __posData!")