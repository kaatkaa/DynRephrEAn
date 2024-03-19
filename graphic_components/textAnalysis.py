import streamlit as st
import sys
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperTextComponent

class Cases2(SuperTextComponent):

    def getTextObj(self, data: Any, t: str) -> Any:
        colorsDict = DataProvider.getUniversalColors()
        def color(row):
            return ['background-color: '+colorsDict[row[self._cf['categoriesColumn']]]] * len(row)
        def make_pretty(styler):
            styler.set_caption(self._cf['ADU_or_Speaker']+" "+t)
            styler.set_table_styles(DataProvider.getTableFormat())
            styler.apply(color, axis=1)
            return styler
        # colorLst = ['background-color: '+str(colorsDict[v]) for v in data[self._cf['categoriesColumn']]]
        data.index += 1
        lst = [self._cf['categoriesColumn']] + self._cf['inOutLst']
        return make_pretty(data[lst].style)

    def dataDisplay(self, df: Any, title: str):
        stylesed = self.getTextObj(df,title)
        #st.dataframe(stylesed, height=800, column_config={self._cf['categoriesColumn']: None})
        st.dataframe(stylesed, height=800)