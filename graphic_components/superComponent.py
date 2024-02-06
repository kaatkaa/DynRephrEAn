import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")

class SuperChartComponent:

    def dataDisplay(self, data: pd, title: str) -> None:
        st.write("This is SuperChartComponent of non overlapped method.")

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.cf = config
        for key in dataDic.keys():
            if not key.startswith("whole"):
                self.dataDisplay(dataDic[key],key)

class SuperTextComponent:

    def dataDisplay(self, data: pd, title: str) -> None:
        st.write("This is SuperTextComponent of non overlapped method.")

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self.cf = config
        for key in dataDic.keys():
            if not key.startswith("grupped"):
                self.dataDisplay(dataDic[key],key)