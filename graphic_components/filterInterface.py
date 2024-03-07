import streamlit as st
import sys
from typing import Tuple, List, Dict, Any
from wordcloud import STOPWORDS


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class FilterInterface:

    __config: Dict[str, Any]={
        'generalConfig':DataProvider.getDynRephrESconfig()['DynRephAn for Sentiment'],
        'prefix':'no_prefix_set_',
        # imediatePlot - set to True if plotting single corpora charts 
        # - to False if plotting in comparative analysis charts
        'imediatePlot': True,
        # For tables wit text, how much lines has to be shown from table
        'textInstances': 1,
        # Dimentions of comparative analysis chart:
        '_8x_dims': [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]],
        # The position (0-7) of current chart in subplot for comparative analysis
        'subChartPosition': 0,
        # ax of subplot
        'ax': None,
        # subplot table customalisation paremeters
        'SubTableXscale': .9,
        'SubTableYscale': 6.5,
        'SubTableFontSize': 24,
        # end of subplot Table configuration
        # Variable below enables "Chart" or "Text" component in SuperTextComponent superclass
        'objectToEnable': "Chart",
        #Number or percentage
        'showPercentageNumber': False,
        'unitPercentNumber': 'Percentage',
        'unitsPercentageNumber': ('Percentage','Number'),
        #categories interface
        'showCategoriesInterface': False,
        'categoriesColumn': '',
        'categoriesLst': DataProvider.getDynRephDimentions(),
        'fixedCatLst': [],
        'categoriesInterfaceTitle': 'Wordcloud_filterInterface',
        # ADU or speaker
        'ADU_or_Speaker': '',
        'SS rephrase': False,
        'OS rephrase': False,
        # Use Input or Output phrase
        'showInOutInterface': True,
        # use radiobutton interface to choose between Input output and Locution input and output
        'showInOutVsLoc': False,
        # List that remembers selected Input output or locution input and output
        'inOutLst': DataProvider.getInOutColLst(),
        # Color palette for barchar 2 types for Dynamic rephrase and PoS
        'palette': DataProvider.getEthosColors(),
        # use stopwords interface
        'showStopWordsInterface':False,
        'showStopwords':False,
        'useStopwords':False,
        'StopwordsSet': set(),
        #Interface of PoS
        'showPOSInterface':False,
        #PoS column names in excel to choose from
        'posColumns': DataProvider.getPSPcolumns1(),
        #PoS categories selected
        'posCategories': DataProvider.getPSPlst(),
        # Shows ngram slider
        'showNgramSlider': False,
        # Keeps ngram slider value
        'ngramSliderValue': 2
    }

    def __init__(self, config: Dict[str, Any]) -> None:
        self.__cf=FilterInterface.__config
        self.__keyCtr = 0
        for cfg in config.items():
            self.__cf[cfg[0]] = cfg[1]
        self.__stop_words_set = set()
        for word in DataProvider.getCustomStopWords():
            self.__stop_words_set.add(word)
        for word in list(STOPWORDS):
            self.__stop_words_set.add(word)
        self.__cf['StopwordsSet'] = self.__stop_words_set
        self.__filterInterface()

    def getConfig(self) -> Dict[str, Any]:
        return self.__cf

    def __filterInterface(self) -> Tuple[Any, list[str]]:

        col_radio1, col_radio2, col_chckbox1= st.columns(3)

        if self.__cf['showPercentageNumber']:
            with col_radio1:
                self.__units()
            
        if self.__cf['showCategoriesInterface']:
            self.__categories(col_radio2)

        if self.__cf['ADU_or_Speaker'] == 'Speaker-Based Analysis':
            with col_chckbox1:
                self.__cf['SS rephrase'] = st.checkbox("SS rephrase",
                    value=self.__cf['SS rephrase'],
                    key=self.__cf['prefix']+"_SS"+str(self.__keyCtr))
                self.__keyCtr += 1
                self.__cf['OS rephrase'] = st.checkbox("OS rephrase",
                    value=self.__cf['OS rephrase'],
                    key=self.__cf['prefix']+"_OS"+str(self.__keyCtr))
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

        if self.__cf['showNgramSlider']:
            self.__NgramSlider()


    def __units(self):
        self.__cf['unitPercentNumber'] = st.radio("Choose units",
            self.__cf['unitsPercentageNumber'],                                                
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
            sortDict = {key: i for i, key in enumerate(DataProvider.getDynRephDimentions())}
            self.__cf['categoriesLst'] = st.multiselect(self.__cf["generalConfig"]["Wordcloud_filterInterface"], 
                                        sorted(DataProvider.getDynRephDimentions()), 
                                        sorted(DataProvider.getDynRephDimentions())[:],
                                        key = self.__cf['prefix']+"_multi_sel"+str(self.__keyCtr))
            self.__keyCtr += 1
            self.__cf['fixedCatLst'] = sorted(self.__cf['categoriesLst'], key=lambda d: sortDict[d])
            self.__cf['categoriesColumn'] = self.__cf['generalConfig']['colName']
        elif display_complexity == '6-categories':
            sortDict = {key: i for i, key in enumerate(DataProvider.getDynRephDimentionsWS())}
            self.__cf['categoriesLst'] = st.multiselect(self.__cf['generalConfig']["Wordcloud_filterInterface"], 
                                        sorted(DataProvider.getDynRephDimentionsWS()), 
                                        sorted(DataProvider.getDynRephDimentionsWS())[:],
                                        key = self.__cf['prefix']+"_multi_selWS"+str(self.__keyCtr))
            self.__keyCtr += 1
            self.__cf['fixedCatLst'] = sorted(self.__cf['categoriesLst'], key=lambda d: sortDict[d])
            self.__cf['categoriesColumn'] = self.__cf['generalConfig']['colNameWS']
        else:
            st.error("Oprion not implemented in __filterInterface, class: WordCloudOfEmotions")

    def __inOut(self):
        col_radio1, col_radio2= st.columns(2)
        with col_radio1:
            if self.__cf['showInOutVsLoc']:
                phrasesType = st.radio(self.__cf['generalConfig']['InOutType'],
                                ("Input_Output",
                                    "Locution_Input_Output"),                                                 
                                key=self.__cf['prefix']+"_inOutType"+str(self.__keyCtr))
                self.__keyCtr += 1
            else:
                phrasesType = "Input_Output"
        with col_radio2:
            if phrasesType == "Input_Output":
                self.__cf['inOutLst'] = st.multiselect("Choose source of data you would like to visualise", 
                                            DataProvider.getInOutColLst(), 
                                            DataProvider.getInOutColLst()[:],
                                            key = self.__cf['prefix']+"_multi_selInOut"+str(self.__keyCtr))
                self.__keyCtr += 1
            elif phrasesType == "Locution_Input_Output":
                self.__cf['inOutLst'] = st.multiselect("Choose source of data you would like to visualise", 
                                            DataProvider.getLocInOut(), 
                                            DataProvider.getLocInOut()[:],
                                            key = self.__cf['prefix']+"_multi_selLocInOut"+str(self.__keyCtr))
                self.__keyCtr += 1
            else:
                st.error("Unknown option: ",phrasesType," in __inOut method.")

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
        self.__cf['useStopwords'] = useStopWords
    
    def __PoSinterface(self):
        col1, col2 = st.columns(2)
        with col1:
            colType = st.radio(self.__cf['generalConfig'][self.__cf['categoriesInterfaceTitle']],
                ("input & output",
                    "Locution input & Locution output"),                                                 
                key=self.__cf['prefix']+"_Rephrase_4-6cat"+str(self.__keyCtr))
        with col2:
            if colType == "input & output":
                self.__cf['posColumns'] = st.multiselect(self.__cf['generalConfig']['POS_inOut'], 
                                            sorted(DataProvider.getPSPcolumns1()),
                                            sorted(DataProvider.getPSPcolumns1())[:],
                                            key = self.__cf['prefix']+"_multiInOutPOS"+str(self.__keyCtr))
                self.__keyCtr += 1
            elif colType == "Locution input & Locution output":
                self.__cf['posColumns'] = st.multiselect(self.__cf['generalConfig']['POS_inOut'], 
                                            sorted(DataProvider.getPSPcolumns2()), 
                                            sorted(DataProvider.getPSPcolumns2())[:],
                                            key = self.__cf['prefix']+"_multiInOutPOS"+str(self.__keyCtr))
                self.__keyCtr += 1
            else:
                st.error("Wrong option in __PoSinterface: colType==",colType)             
        self.__cf['posCategories'] = st.multiselect(self.__cf['generalConfig']['POS_title'],
                                    sorted(DataProvider.getPSPlst()), 
                                    sorted(DataProvider.getPSPlstDefault())[:],
                                    key = self.__cf['prefix']+"_multiPOS"+str(self.__keyCtr))
        self.__keyCtr += 1

    def __NgramSlider(self):
        self.__cf['ngramSliderValue'] = st.slider("Choose n-gram type: (1-4)",1,value=2, max_value=4, key="nType"+self.__cf['prefix'])