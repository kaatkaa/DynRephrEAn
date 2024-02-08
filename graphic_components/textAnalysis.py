import streamlit as st
import sys
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperTextComponent

class Cases2(SuperTextComponent):
    def dataDisplay(self, df: Any, title: str):
        def make_pretty(styler):
            styler.set_caption(self.cf['ADU_or_Speaker']+title)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        df.index += 1
        st.table(make_pretty(df[self.cf['inOutLst']].style))