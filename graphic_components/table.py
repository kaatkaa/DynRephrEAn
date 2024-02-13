import streamlit as st
import sys
import io
import pandas as pd
import numpy as np
import dataframe_image as dfi
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Table2(SuperChartComponent):
    def getChartObj(self, df: Any, t: str):
        columnLst = list(df.columns.values)
        def make_pretty(styler):
            styler.set_caption(self._cf['ADU_or_Speaker']+" "+t)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        df.index += 1
        tmpDf = df.copy(deep=True)
        if len(columnLst) == 3:
            tmpDf = tmpDf[[columnLst[2],columnLst[1]]]
        return make_pretty(tmpDf.style)

    def dataDisplay(self, data: Any, t: str) -> Any:
        tbl = self.getChartObj(data, t)
        st.table(tbl)
        fn = "PNG/"+self._cf['ADU_or_Speaker']+" "+t+".png"
        dfi.export(tbl,filename=fn,dpi=200)
        with open(fn, "rb") as img:
            btn = st.download_button(
                label="Download as PNG",
                data=img,
                file_name=fn,
                mime="image/png"
            )
