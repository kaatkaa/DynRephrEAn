import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")

class dataHandlerDisplayInterface:

    def dataDisplay(self, data: Any, t: str) -> None:
        st.write("This is SuperChartComponent of methodo that should be verlapped.")

    def getChartObj(self, data: Any, t: str) -> Any:
        st.write("This is SuperChartComponent of methodo that should be verlapped.")

class SuperChartComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                if not key.startswith("whole"):
                    self.dataDisplay(dataDic[key],key)
        else:
            pass

class SuperTextComponent(dataHandlerDisplayInterface):

    def getTextObj(self, data: Any, t: str) -> Any:
        st.write("This is SuperChartComponent of methodo that should be verlapped.")

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                if not key.startswith("grupped"):
                    self.dataDisplay(dataDic[key],key)
        else:
            pass