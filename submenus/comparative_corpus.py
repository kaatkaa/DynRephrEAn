import streamlit as st
import pandas as pd

import sys
from submenus.single_corpus import SingleCorpusMenu
from config.config_data_colector import DataProvider
from data_display.display_corpora_cmp import ComparativeCorporaSimple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class CmpCorpusMenu:

    def __init__(self, dataDict: pd, anType: str):
        self.__anCf = DataProvider.getDynRephrESconfig()[anType]
        #Below are tab labels
        self.__tabLabels: list[str] = ["Data("+str(x)+")" for x in range(1,9,1)]
        #Below is loaded SingleCorpusMenu for each tab
        self.__dataLoaders: list[SingleCorpusMenu] = [SingleCorpusMenu(dataDic=dataDict, prefix=str(ctr)+"0_",anType=anType) for ctr in range(1,9,1)]
        self.__tabLabels.append("Comparative Analysis"+self.__anCf['anName'])
        # In dictionary below all __dataDic keys are stored for Data(1)-(8)
        self.__keyDic = {}
        # In dictionary below all data_frames will be stored for comparison
        self.__dataDic = {}

    def display(self, units):
        # Intialization of tabs
        tabs = st.tabs(tabs=self.__tabLabels)
        for ctr, i in enumerate(tabs):
            if ctr < (len(tabs)-1):
                with i:
                    st.subheader("**Pick your data set "+str(ctr+1)+".**")
                    self.__dataLoaders[ctr].tab(units)
                    # if __dataDic was previously filled, now new data will be stored in it so it has to be cleared.
                    if str(ctr)+"_" in self.__keyDic:
                        #print('self.__keyDic['+str(ctr)+'_] = ' +self.__keyDic[str(ctr)+"_"])
                        del self.__dataDic[self.__keyDic[str(ctr)+"_"]]
                    self.__keyDic[str(ctr)+"_"] = self.__tabLabels[ctr]+" |"+self.__dataLoaders[ctr].getCriteria()
                    self.__dataDic[self.__keyDic[str(ctr)+"_"]] = self.__dataLoaders[ctr].getDF()
            else:
                with i:
                    st.subheader(self.__tabLabels[ctr])
                    ComparativeCorporaSimple(self.__dataDic, self.__anCf)

    def clearTabsSelections(self) -> None:
        for tab in self.__dataLoaders:
            tab.cleanSelections()