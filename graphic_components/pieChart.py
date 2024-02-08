import streamlit as st
import sys
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Piechart2(SuperChartComponent):

    def dataDisplay(self, data: Any, t: str):
        displayer = ""
        namesLst = list(data.columns.values)
        if self.cf['unitPercentNumber'] == "Percentage":
            displayer = 'percent+label'
        elif self.cf['unitPercentNumber'] == "Number":
            displayer = 'text+label'
        if len(namesLst) == 3:
            fig = px.pie(data, values=self.cf['unitPercentNumber'], names=namesLst[2], color=namesLst[0],
                        color_discrete_map=self.cf['palette'],
                        title=self.cf['ADU_or_Speaker']+" "+t
            )
        else:
            fig = px.pie(data, values=self.cf['unitPercentNumber'], names=namesLst[0], color=namesLst[0],
                        color_discrete_map=self.cf['palette'],
                        title=self.cf['ADU_or_Speaker']+" "+t
            )
        fig.update_traces(textposition='inside', 
                    text=data[self.cf['unitPercentNumber']].map("#{:,}".format),
                    textinfo=displayer)
        st.plotly_chart(fig, config=DataProvider.getSaveConfig())            