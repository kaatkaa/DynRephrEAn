import streamlit as st
import pandas as pd
from typing import Tuple, List, Dict, Any

import sys
sys.path.insert(0,"..")
from graphic_components.filterInterface import FilterInterface
from data_manipulation.data_filter import DataFilter
from graphic_components.wordCoud import WordCloudOfRephrase
from graphic_components.pieChart import Piechart2
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2
from graphic_components.textAnalysis import Cases2
from graphic_components.ngrams import Ngrams
from graphic_components.pos import PoS
from config.config_data_colector import DataProvider
from submenus.tweaker import st_tweaker

class SingleCorpusMenu:

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="0_", anType: str="DynRephAn for Sentiment") -> None:
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
        #Prefix to distinguish between different data sets
        self.__prefix = prefix
        #loading config file for ethos and sentiment
        tmp = DataProvider.getDynRephrESconfig()
        #config file with messages and column names for Ethos and Sentiment
        self.__anCfg = {}
        self.__anCfg = tmp[anType]

        self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = pd.DataFrame()

        if self.__checkSessionState():
            self.__update_corpora_checkbox
        else:
            # ADU or Speaker
            st.session_state[self.__prefix + 'speakerOrAdu'] = ""
            # Speaker type: "SS rephrase" or "OS rephrase", default is ""
            st.session_state[self.__prefix + 'speakerType'] = ""
        print("Reloaded!!!")

    def __checkSessionState(self) -> bool:
        for key in self.__dataDic:
            if self.__prefix + key not in st.session_state:
                return False
        if self.__prefix + 'speakerOrAdu' not in st.session_state:
            return False
        if self.__prefix + 'speakerType' not in st.session_state:
            return False
        return True

    def cleanSelections(self):
        for key in self.__dataDic:
            st.session_state[self.__prefix + key] = False
        st.session_state[self.__prefix + "US2016reddit"] = False
        st.session_state[self.__prefix + "US2016tv"] = False
        self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df.copy(deep=True)

    def __update_corpora_checkbox(self):
        dfLst = []
        for key in self.__dataDic:
            if st.session_state[self.__prefix + key]:
                dfLst.append(self.__dataDic[key])
        if len(dfLst) > 1:
            self.__rephrase_df = pd.concat(dfLst)          
        elif len(dfLst) == 1:
            self.__rephrase_df = dfLst[0]
        else:
            self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df.copy(deep=True)

    def __update_block(self, name: str):
        for key in self.__dataDic:
            if key.find(name) != -1:
                print("Block:", self.__prefix + name," Updates: ",self.__prefix + key)
                st.session_state[self.__prefix + key] = st.session_state[self.__prefix + name]
                self.__update_corpora_checkbox()

    def __corporaPickerChckBox(self):
        tv = False
        reddit = False
        for ctr, key in enumerate(self.__dataDic):
            if key.find("US2016reddit") != -1:
                if not reddit:
                    reddit = True
                    st.checkbox("US2016reddit", \
                        key = self.__prefix + "US2016reddit",
                        help = self.__prefix + "US2016reddit",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "US2016reddit"},
                        disabled=False
                    )           
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "Reddit" + str(ctr)
                )
            elif key.find("US2016tv") != -1:
                if not tv:
                    tv = True
                    st.checkbox("US2016tv", \
                        key = self.__prefix + "US2016tv",
                        help = self.__prefix + "US2016tv",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "US2016tv"},
                        disabled=False
                    )                     
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "US2016tv" + str(ctr) 
                )                
            else:
                st.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False
                )
        self.__update_corpora_checkbox()
        st.markdown("""
        <style>
        #Reddit0,#Reddit1,#Reddit2,#US2016tv3,#US2016tv4,#US2016tv5 {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
            

    def sidebar(self):
        
        with st.sidebar:
            st.subheader("Choose Corpora: ")           
            st.button("Clean selection",key=self.__prefix+"clear_corpo_button",on_click=self.cleanSelections)
            self.__corporaPickerChckBox()
            st.write("****************************")
            st.subheader("Analysis Units")
            ADU_or_Speaker = st.radio("", ("ADU-Based Analysis",
                                            "Speaker-Based Analysis"
                                            ), key=self.__prefix+"units")
            self.__anCfg['ADU_or_Speaker'] = ADU_or_Speaker
            #if units == "ADU-Based Analysis":
            st.write("****************************")
            st.subheader("Analitics module")
            module_choice = st.radio("An. Module", \
                                        ("Distribution","Wordcloud","n-grams","PoS"), \
                                        key=self.__prefix+"post", label_visibility="hidden"
                                    )
        if module_choice == "n-grams":
            __filterWordCloud = {
                'prefix':'Ngrams_',
                'generalConfig': self.__anCfg,
                'ADU_or_Speaker': ADU_or_Speaker,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'SS rephrase': True,
                'OS rephrase': False,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopwords':False,
                'useStopwords':True,
                'showPOSInterface':False,
                'showNgramSlider': False
            }
            config = FilterInterface(config=__filterWordCloud).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=config).getDataDict()
            Ngrams(dataDic=dataDict,config=config)
        elif module_choice == "Wordcloud":
            #WordCloudOfEmotions(self.__rephrase_df,analysisType="Wordcloud",unit=ADU_or_Speaker, configDic=self.__anCfg, prefix="WordCloud")
            __filterWordCloud = {
                'prefix':'WordCloud_',
                'generalConfig': self.__anCfg,
                'ADU_or_Speaker': ADU_or_Speaker,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'SS rephrase': True,
                'OS rephrase': False,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopwords':False,
                'useStopwords':True,
                'showPOSInterface':False,
                'showNgramSlider': False
            }
            config = FilterInterface(config=__filterWordCloud).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=config).getDataDict()
            WordCloudOfRephrase(dataDic=dataDict,config=config)
        elif module_choice == "Distribution":
            #Piechart(self.__rephrase_df,unit=units_choice, configDic=self.__anCfg, prefix="PieChart", table=False)
            self.container(s="_sub", units_choice=ADU_or_Speaker)
        elif module_choice == "PoS":
            __filterPoS = {
                'prefix':'PoS_',
                'generalConfig': self.__anCfg,
                'ADU_or_Speaker': ADU_or_Speaker,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'SS rephrase': True,
                'OS rephrase': False,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopwords':False,
                'useStopwords':True,
                'showPOSInterface':False,
                'showNgramSlider': False
            }
            PoS(df=self.__rephrase_df,config=__filterPoS)
        else:
            raise NotImplementedError("Unsupported option of Analytical module in single_corpus.py .")
        
    def container(self, s: str="",units_choice: str=""):
        filterCfg = {
            'prefix':'distributions_',
            'generalConfig': self.__anCfg,
            'ADU_or_Speaker': units_choice,
            'imediatePlot': True,
            'showPercentageNumber': True,
            'showCategoriesInterface': True,
            'SS rephrase': True,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showInOutVsLoc': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False,
            'showNgramSlider': False
        }
        config = FilterInterface(config=filterCfg).getConfig()
        dataDic = DataFilter(data=self.__rephrase_df,config=config).getDataDict()
        pieTab, barTab, tableTab, casesTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table",":speech_balloon: Cases"])
        with pieTab:
            #Distribution of ethos/sentiment dynamics in rephrase
            #Piechart(self.__rephrase_df,unit=units_choice, configDic=self.__anCfg, prefix="PieChart"+s, table=False)
            Piechart2(dataDic=dataDic,config=config)
        with barTab:
            Barchart2(dataDic=dataDic, config=config)
        with tableTab:
            #To be formatted
            #st.header(self.getCriteria())
            #Piechart(self.__rephrase_df,unit=units_choice, configDic=self.__anCfg,prefix="Table"+s, table=True)
            Table2(dataDic=dataDic, config=config)
        with casesTab:
            #WordCloudOfEmotions(self.__rephrase_df,analysisType="Cases",unit=units_choice, configDic=self.__anCfg, prefix="Cases"+s,x="simple")
            Cases2(dataDic=dataDic, config=config)
        
    #Returns criteria to which data is selected
    def getCriteria(self) -> str:
        if len(self.__dataDic) > 0:
            newLst = []
            if st.session_state[self.__prefix + 'speakerOrAdu'] == "ADU-Based Analysis":
                newLst = ['ADU based']
            elif st.session_state[self.__prefix + 'speakerOrAdu'] == "Speaker-Based Analysis":
                if self.__prefix + 'speakerType' in st.session_state:
                    newLst = ['Speaker '+st.session_state[self.__prefix + 'speakerType']]
                else:
                    newLst = ['error']
            ctr = 1
            for key in self.__dataDic:
                if st.session_state[self.__prefix + key]:
                    ctr += 1
                    newLst.append(key)
                    if ctr == 2:
                        newLst.append("\n")
                        ctr = 0
            self.criteria = "|".join(newLst)
        else:
            self.criteria = ""
        return self.criteria

    def tab(self, units):
        st.session_state[self.__prefix + 'speakerOrAdu'] = units
        st.subheader("Choose Corpora: ")
        self.__corporaPickerChckBox()
        if len(self.__rephrase_old) > 0:
            if st.session_state[self.__prefix + 'speakerOrAdu'] == "ADU-Based Analysis":
                st.write("ADU units selected.")
                self.__rephrase_df = self.__rephrase_old.copy(deep=True)
                st.session_state[self.__prefix + 'speakerType'] = ""
            elif st.session_state[self.__prefix + 'speakerOrAdu'] == "Speaker-Based Analysis":
                speaker = st.radio("Choose Speaker Unit Type: ",
                    ("SS rephrase",
                    "OS rephrase"),
                    key=self.__prefix+"Rephrase_Cmp_Speaker")
                if speaker == "SS rephrase":
                    self.__rephrase_df = self.__rephrase_old.copy(deep=True)
                    self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] == self.__rephrase_df['speaker_output']]
                elif speaker == "OS rephrase":
                    self.__rephrase_df = self.__rephrase_old.copy(deep=True)
                    self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] != self.__rephrase_df['speaker_output']]
                st.session_state[self.__prefix + 'speakerType'] = speaker
        else:
            st.write("Choose corpora above.")

    #Returns data for diagrams
    def getDF(self) -> pd.DataFrame():
        return self.__rephrase_df