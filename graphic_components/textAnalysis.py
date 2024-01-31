import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.api.types import CategoricalDtype
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class Cases2:
    def __showTable(self, df: Any, title: str):
        def make_pretty(styler):
            styler.set_caption(self.__cf['AnalysisUnit']+title)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        if len(self.__cf['inOutLst']) == 2:
            df.index += 1
            st.table(make_pretty(df[self.__cf['inOutLst']].style))
        elif len(self.__cf['inOutLst']) == 1:
            tmp = []
            tmp.append(self.__cf['inOutLst'][0])
            tmp.append("locution_"+self.__cf['inOutLst'][0])
            df.index += 1
            st.table(make_pretty(df[tmp].style))

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.__cf = config
        self.__prefix = config['prefix']
        st.subheader(self.__cf['generalConfig']['Distribution_top'])
        DataProvider.addSpacelines(1)
        if 'wholeAll' in dataDic:
            self.__showTable(dataDic['wholeAll'],"")
        else: 
            if 'wholeSS' in dataDic:
                self.__showTable(dataDic['wholeSS'],": Same Speaker")
            elif 'wholeOS' in dataDic:
                self.__showTable(dataDic['wholeOS'],": Other Speaker")