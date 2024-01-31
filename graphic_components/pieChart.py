import streamlit as st
import sys
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider

class Piechart2:

    def __drawPie(self, data: Any, t: str):
        displayer = ""
        namesLst = list(data.columns.values)
        if self.__cf['unit'] == "Percentage":
            displayer = 'percent+label'
        elif self.__cf['unit'] == "Number":
            displayer = 'text+label'
        if len(namesLst) == 3:
            fig = px.pie(data, values=self.__cf['unit'], names=namesLst[2], color=namesLst[0],
                        color_discrete_map=self.__cf['palette'],
                        title=self.__cf['AnalysisUnit']+t
            )
        else:
            fig = px.pie(data, values=self.__cf['unit'], names=namesLst[0], color=namesLst[0],
                        color_discrete_map=self.__cf['palette'],
                        title=self.__cf['AnalysisUnit']+t
            )
        fig.update_traces(textposition='inside', 
                    text=data[self.__cf['unit']].map("#{:,}".format),
                    textinfo=displayer)
        st.plotly_chart(fig, config=DataProvider.getSaveConfig())

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.__cf = config
        self.__prefix = config['prefix']
        DataProvider.addSpacelines(1)
        if 'gruppedAll' in dataDic:
                self.__drawPie(dataDic['gruppedAll'],"")
        else:
            if 'gruppedSS' in dataDic:
                self.__drawPie(dataDic['gruppedSS'],": Same Speaker")
            if 'gruppedOS' in dataDic:
                self.__drawPie(dataDic['gruppedOS'],": Other Speaker")               