import streamlit as st
import sys
import pandas as pd
import numpy as np
from io import BytesIO
import dataframe_image as dfi
from typing import Tuple, List, Dict, Any
from pandas.plotting import table

sys.path.insert(0,"..")
from graphic_components.superComponent import SuperPoSTextComponent
from config.config_data_colector import DataProvider

class FalseTable(SuperPoSTextComponent):
    
    def dataDisplay(self, two: Tuple[Dict[str, int], Dict[str, int or float]], t: str) -> None:
        posDict = two[0]
        tagDict = two[1]

        def showAdvTable(key = ''):
            if key in tagDict:
                with st.container():
                    st.table(data=tagDict[key])

        with st.container():
            st.header("Analysis: "+t)
            col1, col2, col3 = st.columns(3)
            st.markdown("""
                <style>
                .font-custom {
                    font-size:22px !important;
                }
                </style>
                """, unsafe_allow_html=True)
            with col1:
                st.subheader("Row number")
                for n in range(1,len(posDict)+1):
                    st.markdown('<p class="font-custom">{s}</p>'.format(s=str(n)),unsafe_allow_html=True)
                    DataProvider.addSpacelines(1)
            with col2:
                st.subheader("Tag")
                for tg in posDict.keys():
                    st.button(label=tg, on_click=showAdvTable, kwargs={'key':tg})
                    DataProvider.addSpacelines(1)
            with col3:
                st.subheader("Frequency")
                for tg in posDict.values():
                    st.markdown('<p class="font-custom">{s}</p>'.format(s=str(tg)),unsafe_allow_html=True)
                    DataProvider.addSpacelines(1)
