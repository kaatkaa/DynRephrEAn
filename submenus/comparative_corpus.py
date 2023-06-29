import streamlit as st
import pandas as pd

import sys
from submenus.single_corpus import SingleCorpusMenu
from data_display.display_corpora_cmp import ComparativeCorporaSimple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class CmpCorpusMenu:

    def __init__(self, data: pd):
        #Below are tab labels
        self.__tabLabels: list[str] = ["Data("+str(x)+")" for x in range(1,5,1)]
        #Below is loaded SingleCorpusMenu for each tab
        self.__dataLoaders: list[SingleCorpusMenu] = [SingleCorpusMenu(data=data,tickerDic=DataProvider.getLeadersTicker(),prefix=str(ctr)+"_") for ctr in range(1,5,1)]
        self.__tabLabels.append("Comparative Analysis")
        # In dictionary below all __dataDic keys are stored for Data(1)-(4)
        self.__keyDic = {}
        # In dictionary below all data_frames will be stored for comparison
        self.__dataDic = {}

    def display(self):
        # Intialization of tabs
        tabs = st.tabs(tabs=self.__tabLabels)
        for ctr, i in enumerate(tabs):
            if ctr < (len(tabs)-1):
                with i:
                    st.subheader("**Pick your data set "+str(ctr+1)+".**")
                    self.__dataLoaders[ctr].tab()
                    # if __dataDic was previously filled, now new data will be stored in it so it has to be cleared.
                    if str(ctr)+"_" in self.__keyDic:
                        print('self.__keyDic['+str(ctr)+'_] = ' +self.__keyDic[str(ctr)+"_"])
                        del self.__dataDic[self.__keyDic[str(ctr)+"_"]]
                    self.__keyDic[str(ctr)+"_"] = self.__tabLabels[ctr]+" |"+self.__dataLoaders[ctr].getCriteria()
                    self.__dataDic[self.__keyDic[str(ctr)+"_"]] = self.__dataLoaders[ctr].getDF()
            else:
                with i:
                    st.subheader(self.__tabLabels[ctr])
                    ComparativeCorporaSimple(self.__dataDic)