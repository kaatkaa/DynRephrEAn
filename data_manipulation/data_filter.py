import streamlit as st
import sys
import pandas as pd
import re
from operator import itemgetter
from typing import Tuple, List, Dict, Any


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class DataFilter:

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
        'StopwordsSet': set(),
        'showPOSInterface':False,
        'posColumns': DataProvider.getPSPcolumns1(),
        'posCategories': DataProvider.getPSPlst()
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
        self.__cf=DataFilter.__config
        self.__stop_words_set = self.__cf['StopwordsSet']
        if len(data) > 0:
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
        
    def __filterInterface(self) -> Tuple[Any, list[str]]:
            
        if self.__cf['showCategoriesInterface'] and len(self.__outputData) > 0:
            self.__outputData = self.__outputData.loc[self.__outputData[self.__cf['categoriesColumn']].isin(self.__cf['categoriesLst'])]
        else:
            self.__outputData = self.__d

        if self.__cf['showStopWordsInterface'] and self.__cf['useStopwords'] and len(self.__outputData) > 0:
            self.__RemoveStopWordsFromDf(self.__outputData, self.__cf['inOutLst'])

        if self.__cf['showPOSInterface'] and len(self.__outputData) > 0:
            self.__cf['palette'] = DataProvider.getPoScolors()
            self.__PoSinterface()
        else:
            if self.__cf['imediatePlot']:
                self.__cf['palette'] = DataProvider.getEthosColors()
                if self.__cf['ADU_or_Speaker'] == 'Speaker-Based Analysis':
                    #st.write("Same speaker rephrase: "+str(self.__cf['SS rephrase'])+" Other speaker rephrase: "+str(self.__cf['OS rephrase']))
                    if self.__cf['SS rephrase']:
                        self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
                        self.__outDict["gruppedSS"] = self.__distributionData(self.__outDict["wholeSS"], self.__cf['categoriesColumn'])
                    if self.__cf['OS rephrase']:
                        self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
                        self.__outDict["gruppedOS"] = self.__distributionData(self.__outDict["wholeOS"], self.__cf['categoriesColumn'])
                else:
                    self.__outDict["wholeAll"] = self.__outputData
                    self.__outDict["gruppedAll"] = self.__distributionData(self.__outputData, self.__cf['categoriesColumn']) 
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
            if self.__cf['ADU_or_Speaker'] == 'Speaker-Based Analysis':
                if self.__cf['SS rephrase']:
                    self.__outDict["wholeSS"]=self.__outputData[self.__outputData['speaker_input']==self.__outputData['speaker_output']]
                    self.__outDict["gruppedSS"] = dfFromDic(
                        "PoS_type",
                        self.__cf['unitPercentNumber'],
                        self.__posData(data=self.__outDict['wholeSS'],inOutPOS=self.__cf['posColumns'],POS_filter=self.__cf['posCategories'])
                    )
                if self.__cf['OS rephrase']:
                    self.__outDict["wholeOS"]=self.__outputData[self.__outputData['speaker_input']!=self.__outputData['speaker_output']]
                    self.__outDict["gruppedOS"] = dfFromDic(
                        "PoS_type",
                        self.__cf['unitPercentNumber'],
                        self.__posData(data=self.__outDict['wholeOS'],inOutPOS=self.__cf['posColumns'],POS_filter=self.__cf['posCategories'])               
                    )
            else:
                self.__outDict["wholeAll"] = self.__outputData
                self.__outDict["gruppedAll"] = dfFromDic("PoS_type",self.__cf['unitPercentNumber'],
                    self.__posData(data=self.__outputData,inOutPOS=self.__cf['posColumns'],POS_filter=self.__cf['posCategories']))
        else:
            self.__outDict["wholeAll"] = self.__outputData
            self.__outDict["gruppedAll"] = dfFromDic("PoS_type",self.__cf['unitPercentNumber'],
                self.__posData(data=self.__outputData,inOutPOS=self.__cf['posColumns'],POS_filter=self.__cf['posCategories']))

    def __distributionData(self, data, column):
        if self.__cf['unitPercentNumber'] == "Percentage":
            #print("############",data,"Column: ",column)
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
            return DataManipulator.getTagsPercentageFreq(d=data,
                colLst=inOutPOS,
                PSPset=set(POS_filter))
        elif self.__cf['unitPercentNumber'] == "Number":
            return DataManipulator.getTagsFreq(d=data,
                colLst=inOutPOS,
                PSPset=set(POS_filter))
        else:
            st.error("Wrong option: "+self.__cf['unitPercentNumber']+" for __posData!")