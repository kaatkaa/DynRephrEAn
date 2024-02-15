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

    def getChartsDic() -> Dict[str, Any]:
        st.write("This is SuperChartComponent of methodo that should be verlapped.")

class SuperChartComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        self.__data = {}
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                if not key.startswith("whole"):
                    self.dataDisplay(dataDic[key],key)
        else:
            for ctr, key in enumerate(dataDic.keys()):
                self._cf['subChartPosition'] = ctr
                self.__data[key] = self.getChartObj(dataDic[key],key)

    def getChartsDic(self) -> Dict[str, Any]:
        return self.__data

class SuperTextComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        self.__chartDict = {}
        self.__textDict = {}
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                if not key.startswith("grupped"):
                    self.dataDisplay(dataDic[key],key)
        else:
            for key in dataDic.keys():
                self.__chartDict[key] = self.getChartObj(dataDic[key],key)
                self.__textDict[key] = self.getTextObj(dataDic[key],key)

    def getTextObj(self, data: Any, t: str) -> Any:
        st.write("This is SuperChartComponent of methodo that should be verlapped.")

    def getTextDic(self) -> Dict[str, Any]:
        return self.__textDict
    
    def getChartsDic(self) -> Dict[str, Any]:
        return self.__chartDict