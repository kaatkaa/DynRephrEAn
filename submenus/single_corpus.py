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
from graphic_components.ngrams_PoS import NgramsPoS
from config.config_data_colector import DataProvider
from submenus.tweaker import st_tweaker
from st_ant_tree import st_ant_tree
from streamlit_modal import Modal

class SingleCorpusMenu:

    __debug = True

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="0_") -> None:
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
        #Prefix to distinguish between different data sets
        self.__prefix = prefix

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
        st.session_state[self.__prefix + "ElectionsSM"] = False
        st.session_state[self.__prefix + "ElectionsTV"] = False
        self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df.copy(deep=True)

    def __update_corpora_checkbox(self):
        dfLst = []
        for key in self.__dataDic:
            if st.session_state[self.__prefix + key]:
                dfLst.append(self.__dataDic[key])
        if len(dfLst) > 1:
            self.__rephrase_df = pd.concat(dfLst,ignore_index=True)          
        elif len(dfLst) == 1:
            self.__rephrase_df = dfLst[0]
        else:
            self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df.copy(deep=True)

    def __update_block(self, name: str):
        for key in self.__dataDic:
            if key.find(name) != -1:
                #print("Block:", self.__prefix + name," Updates: ",self.__prefix + key)
                st.session_state[self.__prefix + key] = st.session_state[self.__prefix + name]
                self.__update_corpora_checkbox()

    def __corporaPickerChckBox(self):
        tv = False
        reddit = False
        for ctr, key in enumerate(self.__dataDic):
            if key.find("ElectionsSM") != -1:
                if not reddit:
                    reddit = True
                    st.checkbox("ElectionsSM", \
                        key = self.__prefix + "ElectionsSM",
                        help = self.__prefix + "ElectionsSM",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "ElectionsSM"},
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
            elif key.find("ElectionsTV") != -1:
                if not tv:
                    tv = True
                    st.checkbox("ElectionsTV", \
                        key = self.__prefix + "ElectionsTV",
                        help = self.__prefix + "ElectionsTV",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "ElectionsTV"},
                        disabled=False
                    )                     
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "ElectionsTV" + str(ctr) 
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
        #Reddit0,#Reddit1,#Reddit2,#ElectionsTV3,#ElectionsTV4,#ElectionsTV5 {
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
            ADU_or_Speaker = st.radio("Unit picker",("Text-Based Analysis",),
                     key=self.__prefix+"Text-Based",
                     index=0,
                     label_visibility='hidden')
            st.session_state[st.session_state['cfgId']]['ADU_or_Speaker'] = ADU_or_Speaker
            st.write("****************************")
            st.subheader("Statictical module")
            module_choice = st.radio("An. Module", \
                                        ("Distribution","Wordcloud","n-grams","PoS","n-grams_PoS"), \
                                        key=self.__prefix+"post", label_visibility="hidden"
                                    )
        st.markdown("""
        <style>
        #TextUnits #EntityUnits {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
        config = {}
        # if SingleCorpusMenu.__debug:
        #     open_modal = False
        #     open_modal = st.button(key="N-grams_debug..", label='N-grams_debug')
        #     modal = Modal(key="N-gram_debug", title="showPOSInterface check")
        if module_choice == "n-grams":
            __n_gramsCfg = {
                'prefix':'Ngrams_',
                'imediatePlot': True,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopPoSInterface': False,
                'showPOSInterface':False,
                'showNgramSlider': False,
            }
            DataProvider.updateGlobalConfig(config=__n_gramsCfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            Ngrams(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
        elif module_choice == "n-grams_PoS":
            __n_gramsPoS_Cfg = {
                'prefix':'NgramsPoS_',
                'imediatePlot': True,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':False,
                'showPOSInterface':False,
                'showStopPoSInterface': True,
                'showNgramSlider': True,
            }
            DataProvider.updateGlobalConfig(config=__n_gramsPoS_Cfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            NgramsPoS(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
        elif module_choice == "Wordcloud":
            __CloudCfg = {
                'prefix':'WordCloud_',
                'imediatePlot': True,
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopPoSInterface': False,
                'showPOSInterface':False,
                'showNgramSlider': False,
            }
            DataProvider.updateGlobalConfig(config=__CloudCfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            WordCloudOfRephrase(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
        elif module_choice == "Distribution":
            __DistribCfg = {
                'prefix':'distributions_',
                'imediatePlot': True,
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':True,
                'showStopPoSInterface': False,
                'showPOSInterface':False,
                'showNgramSlider': False,
                'n-gramType': ''
            }
            DataProvider.updateGlobalConfig(config=__DistribCfg)
            if SingleCorpusMenu.__debug:
                st.button(key="Session_state..", label='Session_state')
                modal = Modal(key="session_st", title="showPOSInterface check")
                if modal.is_open():
                    with modal.container():
                        st.write(st.session_state[st.session_state['cfgId']])
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            pieTab, barTab, tableTab, casesTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table",":speech_balloon: Cases"])
            with pieTab:
                Piechart2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
            with barTab:
                Barchart2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with tableTab:
                Table2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with casesTab:
                Cases2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
        elif module_choice == "PoS":
            __PoSCfg = {
                'prefix':'PoS_',
                'imediatePlot': True,
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'showInOutInterface': True,
                'showInOutVsLoc': True,
                'showStopWordsInterface':False,
                'showStopPoSInterface': False,
                'showPOSInterface':True,
                'showNgramSlider': False,
                'showStopPoSInterface':False,
            }
            DataProvider.updateGlobalConfig(config=__PoSCfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__rephrase_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            pieTab, barTab, tableTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table"])
            with pieTab:
                st.subheader(st.session_state[st.session_state['cfgId']]['generalConfig']['POS_piechart'])
                Piechart2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
            with barTab:
                st.subheader(st.session_state[st.session_state['cfgId']]['generalConfig']['POS_barchart'])
                Barchart2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
            with tableTab:
                st.subheader(st.session_state[st.session_state['cfgId']]['generalConfig']['POS_table'])
                Table2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
        else:
            raise NotImplementedError("Unsupported option of Analytical module in single_corpus.py .")
        
    #Returns criteria to which data is selected
    def getCriteria(self) -> str:
        if len(self.__dataDic) > 0:
            newLst = []
            # if st.session_state[self.__prefix + 'speakerOrAdu'] == "Text-Based Analysis":
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
            speaker = st.radio("Choose Speaker Unit Type: ",
                ("SS + OS rephrase",
                "SS rephrase",
                "OS rephrase"),
                key=self.__prefix+"Rephrase_Cmp_Speaker")
            if speaker == "SS + OS rephrase":
                self.__rephrase_df = self.__rephrase_old.copy(deep=True)
            elif speaker == "SS rephrase":
                self.__rephrase_df = self.__rephrase_old.copy(deep=True)
                self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] == self.__rephrase_df['speaker_output']]
            elif speaker == "OS rephrase":
                self.__rephrase_df = self.__rephrase_old.copy(deep=True)
                self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] != self.__rephrase_df['speaker_output']]
            st.session_state[self.__prefix + 'speakerType'] = speaker

    #Returns data for diagrams
    def getDF(self) -> pd.DataFrame():
        return self.__rephrase_df