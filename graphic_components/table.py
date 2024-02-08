import streamlit as st
import sys
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Table2(SuperChartComponent):
    def dataDisplay(self, df: Any, t: str):
        columnLst = list(df.columns.values)
        def make_pretty(styler):
            styler.set_caption(self.cf['ADU_or_Speaker']+" "+t)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        df.index += 1
        tmpDf = df.copy(deep=True)
        if len(columnLst) == 3:
            tmpDf = tmpDf[[columnLst[2],columnLst[1]]]
        st.table(make_pretty(tmpDf.style))