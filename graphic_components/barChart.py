import streamlit as st
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class Barchart2:
    def __drawBars(self, data: Any, t: str):
        columnLst = list(data.columns.values)
        z = sns.barplot(data = data, x = columnLst[0], y = columnLst[1], 
            palette = self.__cf['palette'])
        if self.__cf['unit'] == "Percentage":
            z.bar_label(z.containers[0], fmt='%d%%')
        elif self.__cf['unit'] == "Number":
            z.bar_label(z.containers[0], fmt='#%d')
        z.grid(b=True, which='major', color='black', linewidth=0.075)
        z.set(title=self.__cf['AnalysisUnit']+t)
        z.set_xlabel(columnLst[0],fontsize=20)
        z.set_ylabel(columnLst[1], fontsize=20)
        z.tick_params(labelsize=20)
        st.pyplot(fig=z.get_figure(), config=DataProvider.getSaveConfig())
        z.containers.pop()
        z.cla()

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.__cf = config
        self.__prefix = config['prefix']
        DataProvider.addSpacelines(1)
        if 'gruppedAll' in dataDic:
            self.__drawBars(dataDic['gruppedAll'],"")
        else:
            if 'gruppedSS' in dataDic:
                #st.write("SS: ",dataDic['gruppedSS'])
                self.__drawBars(dataDic['gruppedSS'],": Same Speaker")
            if 'gruppedOS' in dataDic:
                #st.write("OS: ",dataDic['gruppedOS'])
                self.__drawBars(dataDic['gruppedOS'],": Other Speaker")