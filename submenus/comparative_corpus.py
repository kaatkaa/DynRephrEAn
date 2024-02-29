import streamlit as st
import pandas as pd

import sys
from submenus.single_corpus import SingleCorpusMenu
from config.config_data_colector import DataProvider
from data_display.display_corpora_cmp import ComparativeCorporaSimple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from submenus.three_d_corpus import ThreeDCorpusMenu
from submenus._3D_PSP_corpus import _3D_PSP_corpus

class CmpCorpusMenu:

    def __init__(self, dataDict: pd, anType: str):
        self.__anType = anType
        self.__dataDict = dataDict

        self.__anCf ={
            'prefix':'no_prefix_set_',
            # imediatePlot - set to True if plotting single corpora charts 
            # - to False if plotting in comparative analysis charts
            'imediatePlot': False,
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

    def display(self, units):
        st.markdown("""
            <style>
            .stRadio [role=radiogroup]{
                display: flex;
                justify-content: space-between;
            }
            </style>
        """,unsafe_allow_html=True)
        userMix, _3dMix, _3dPoS = st.tabs([":male-technologist: User selection corpora",":three: D Corporas", ":three: D PoS"])
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
        # with _3dMix:
        #     with st.form("3D corporas"):
        #         submit = st.form_submit_button("Show 3D corpora!")
        #         if submit:
        #             ThreeDCorpusMenu(dataDic=self.__dataDict, prefix="3D_Distribution", anType=self.__anType).draw3D(bothEthosPathos=False)
        # with _3dPoS:
        #     with st.form("3D Parts of Speech"):
        #         submit = st.form_submit_button("Show 3D Parts of Speech!")
        #         if submit:
        #             _3D_PSP_corpus(dataDic=self.__dataDict, prefix="3D_PoS", anType=self.__anType).draw3D()

    def clearTabsSelections(self) -> None:
        for tab in self.__dataLoaders:
            tab.cleanSelections()