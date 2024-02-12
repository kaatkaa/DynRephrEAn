import streamlit as st
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Barchart2(SuperChartComponent):
    def getChartObj(self, data: Any, t: str) -> sns.barplot():
        columnLst = list(data.columns.values)
        z = sns.barplot(data = data, x = columnLst[0], y = columnLst[1], 
            palette = self.cf['palette'])
        if self.cf['unitPercentNumber'] == "Percentage":
            z.bar_label(z.containers[0], fmt='%d%%')
        elif self.cf['unitPercentNumber'] == "Number":
            z.bar_label(z.containers[0], fmt='#%d')
        z.grid(b=True, which='major', color='black', linewidth=0.075)
        z.set(title=self.cf['ADU_or_Speaker']+" "+t)
        z.set_xlabel(columnLst[0],fontsize=20)
        z.set_ylabel(columnLst[1], fontsize=20)
        z.tick_params(labelsize=20)
        return z

    def dataDisplay(self, data: Any, t: str) -> Any:
        fig = self.getChartObj(data, t)
        st.pyplot(fig=fig.get_figure(), config=DataProvider.getSaveConfig())
        fig.containers.pop()
        fig.cla()