import streamlit as st
import pandas as pd

import sys

from typing import Dict, Any
from submenus.single_corpus import SingleCorpusMenu
from config.config_data_colector import DataProvider
from data_display.display_corpora_cmp import ComparativeCorporaSimple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components._3D_EthosPathos import _3D_EthosPathos
from graphic_components.filterInterface import FilterInterface
from graphic_components._3D_PoS import _3D_PoS

class CmpCorpusMenu:

    def __init__(self, dataDict: pd, anType: str):
        self.__anType = anType
        self.__ADUorSpeaker = ''
        self.__dataDict = dataDict

        self.__anCf = {
            'prefix':'no_prefix_set_',
            # imediatePlot - set to True if plotting single corpora charts 
            # - to False if plotting in comparative analysis charts
            'imediatePlot': False,
            'anType': anType,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'categoriesColumn': '',
            'SS rephrase': False,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False
        }
        self.__anCf['generalConfig'] = DataProvider.getDynRephrESconfig()[anType]

        #Below are tab labels
        self.__tabLabels: list[str] = ["Data("+str(x)+")" for x in range(1,9,1)]
        #Below is loaded SingleCorpusMenu for each tab
        self.__dataLoaders: list[SingleCorpusMenu] = [SingleCorpusMenu(dataDic=dataDict, prefix=str(ctr)+"0_",anType=anType) for ctr in range(1,9,1)]
        self.__tabLabels.append("Comparative Analysis"+self.__anCf['generalConfig']['anName'])
        # In dictionary below all __dataDic keys are stored for Data(1)-(8)
        self.__keyDic = {}
        # In dictionary below all data_frames will be stored for comparison
        self.__dataDic = {}

    def __updateCfg(self, config: Dict[str, Any]):
        for item in config.items():
            self.__anCf[item[0]] = item[1]

    def display(self, units):
        st.markdown("""
            <style>
            .stRadio [role=radiogroup]{
                display: flex;
                justify-content: space-between;
            }
            </style>
        """,unsafe_allow_html=True)
        self.__ADUorSpeaker = units
        userMix, _3dMix = st.tabs([":male-technologist: User selection corpora",":three: D Corporas"])
        st.divider()
        with userMix:
            tabs = st.tabs(tabs=self.__tabLabels)
            for ctr, i in enumerate(tabs):
                if ctr < (len(tabs)-1):
                    with i:
                        st.subheader("**Pick your data set "+str(ctr+1)+".**")
                        self.__dataLoaders[ctr].tab(units)
                        # if __dataDic was previously filled, now new data will be stored in it so it has to be cleared.
                        if str(ctr)+"_" in self.__keyDic:
                            #st.text(self.__keyDic[str(ctr)+'_'])
                            del self.__dataDic[self.__keyDic[str(ctr)+"_"]]
                            del self.__keyDic[str(ctr)+"_"]
                        self.__keyDic[str(ctr)+"_"] = self.__tabLabels[ctr]+" |"+self.__dataLoaders[ctr].getCriteria()
                        self.__dataDic[self.__keyDic[str(ctr)+"_"]] = self.__dataLoaders[ctr].getDF()
                else:
                    with i:
                        st.subheader(self.__tabLabels[ctr])
                        ComparativeCorporaSimple(data_dic=self.__dataDic, config=self.__anCf)
        with _3dMix:
            cfg = {
                'prefix': "3D_EthosPathos",
                'imediatePlot': True,
                'objectToEnable': "Chart",
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'ADU_or_Speaker': units,
                'SS rephrase': True,
                'OS rephrase': False,
                'showInOutInterface': False,
                'showStopWordsInterface':False,
                'showStopwords':False,
                'useStopwords':False,
                'showPOSInterface':False,
                'showNgramSlider': False
            }
            self.__updateCfg(config=cfg)
            self.__anCf = FilterInterface(config=self.__anCf).getConfig()
            _3D_EthosPathos(dataDic=self.__dataDict,config=self.__anCf).plot3D()
        # with _3dPoS:
        #     cfg = {
        #                     'prefix': "3D_PoS",
        #                     'imediatePlot': True,
        #                     'objectToEnable': "Chart",
        #                     'showPercentageNumber': True,
        #                     'showCategoriesInterface': True,
        #                     'ADU_or_Speaker': units,
        #                     'SS rephrase': True,
        #                     'OS rephrase': False,
        #                     'showInOutInterface': False,
        #                     'showStopWordsInterface':False,
        #                     'showStopwords':False,
        #                     'useStopwords':False,
        #                     'showPOSInterface':True,
        #                     'showNgramSlider': False
        #     }
        #     self.__updateCfg(config=cfg)
        #     self.__anCf = FilterInterface(config=self.__anCf).getConfig()
        #     _3D_PoS(dataDic=self.__dataDict,config=self.__anCf).plot3D()

    def clearTabsSelections(self) -> None:
        for tab in self.__dataLoaders:
            tab.cleanSelections()