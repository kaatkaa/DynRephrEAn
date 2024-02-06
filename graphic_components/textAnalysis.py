import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.api.types import CategoricalDtype
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperTextComponent

class Cases2(SuperTextComponent):
    def dataDisplay(self, df: Any, title: str):
        def make_pretty(styler):
            styler.set_caption(self.cf['AnalysisUnit']+title)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        if len(self.cf['inOutLst']) == 2:
            df.index += 1
            st.table(make_pretty(df[self.cf['inOutLst']].style))
        elif len(self.cf['inOutLst']) == 1:
            tmp = []
            tmp.append(self.cf['inOutLst'][0])
            tmp.append("locution_"+self.cf['inOutLst'][0])
            df.index += 1
            st.table(make_pretty(df[tmp].style))