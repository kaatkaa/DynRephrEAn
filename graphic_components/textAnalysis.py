import streamlit as st
import sys
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperTextComponent

class Cases2(SuperTextComponent):

    def getTextObj(self, data: Any, t: str) -> Any:
        def make_pretty(styler):
            styler.set_caption(self._cf['ADU_or_Speaker']+" "+t)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        data.index += 1
        return make_pretty(data[self._cf['inOutLst']].style)

    def dataDisplay(self, df: Any, title: str):
        stylesed = self.getTextObj(df,title)
        st.table(stylesed)