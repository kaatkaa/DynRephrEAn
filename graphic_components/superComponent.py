import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")

class dataHandlerDisplayInterface:

    def dataDisplay(self, data: Any, t: str) -> None:
        st.write("This is SuperChartComponent of overlapped method.")

    def getChartObj(self, data: Any, t: str) -> Any:
        st.write("This should return chart obj.")

class SuperChartComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.cf = config
        for key in dataDic.keys():
            if not key.startswith("whole"):
                self.dataDisplay(dataDic[key],key)

class SuperTextComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.cf = config
        for key in dataDic.keys():
            if not key.startswith("grupped"):
                self.dataDisplay(dataDic[key],key)