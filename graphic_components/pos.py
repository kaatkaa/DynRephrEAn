import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.api.types import CategoricalDtype
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_filter import DataFilter
from graphic_components.filterInterface import FilterInterface
from graphic_components.pieChart import Piechart2
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2

class PoS:

    __filterCfg = {
        'prefix':'PoS_',
        'showPercentageNumber': True,
        'showCategoriesInterface': True,
        'showInOutInterface': False,
        'SS rephrase': True,
        'OS rephrase': False,
        'showStopWordsInterface':False,
        'showPOSInterface':True
    }

    def __plot(self, dfDic: Dict[str, Any]):

        pieTab, barTab, tableTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table"])
        with pieTab:
            st.subheader(self.__cf['generalConfig']['POS_piechart'])
            Piechart2(dataDic=dfDic,config=self.__cf)
        with barTab:
            st.subheader(self.__cf['generalConfig']['POS_barchart'])
            Barchart2(dataDic=dfDic,config=self.__cf)
        with tableTab:
            st.subheader(self.__cf['generalConfig']['POS_table'])
            Table2(dataDic=dfDic,config=self.__cf)

    def __init__(self, df: Any, config: Dict[str, str or Dict]) -> None:
        config = PoS.__filterCfg
        for key in config:
            config[key] = config[key]
        config = FilterInterface(config=config).getConfig()
        dataDic = DataFilter(df, config=config).getDataDict()
        self.__cf = config
        DataProvider.addSpacelines(1)
        self.__plot(dfDic=dataDic)