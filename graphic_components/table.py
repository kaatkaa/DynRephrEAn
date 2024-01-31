import streamlit as st
import sys
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class Table2:
    def __drawTable(self, df: Any, title: str):
        def make_pretty(styler):
            styler.set_caption(self.__cf['AnalysisUnit']+title)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        df.index += 1
        st.table(make_pretty(df.style))

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.__cf = config
        self.__prefix = config['prefix']
        DataProvider.addSpacelines(1)
        if 'gruppedAll' in dataDic:
            self.__drawTable(dataDic['gruppedAll'],"")
        else:
            if 'gruppedSS' in dataDic:
                self.__drawTable(dataDic['gruppedSS'],": Same Speaker")
            if 'gruppedOS' in dataDic:
                self.__drawTable(dataDic['gruppedOS'],": Other Speaker")