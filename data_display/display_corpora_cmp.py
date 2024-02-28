import streamlit as st
import io
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

from typing import Dict, Any
sys.path.insert(0,"..")
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2
from graphic_components.wordCoud import WordCloudOfRephrase
from graphic_components.filterInterface import FilterInterface
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from data_manipulation.data_filter import DataFilter

class ComparativeCorporaSimple:

    def __init__(self, data_dic: dict[str,pd.DataFrame()], config: Dict[str,Any]):
        self.prefixCtr = 1
        self.__dataDic = data_dic
        self.__cf = config
        with st.sidebar:
            st.header("Analytics module")
            module = st.radio("Choose module: ", ("Distribution","Wordcloud","n-grams","PoS","3D_Distribution","3D_PoS"),
                            label_visibility='collapsed', key=str(self.prefixCtr)+"CMP_module_")
        self.prefixCtr += 1
        gruppedDataDic = {}
        wholeDataDic = {}

        if module == "Distribution" and len(self.__dataDic) > 0:
            self.__cf = {
                'imediatePlot': False,
                'showPercentageNumber': True,
                'unitPercentNumber': 'Percentage',
                'showCategoriesInterface': True,
                'categoriesColumn': '',
                'ADU_or_Speaker':"",
                'SS rephrase': False,
                'OS rephrase': False,
                'showInOutInterface': True,
                'showStopWordsInterface':True,
                'showStopwords':False,
                'useStopwords':True,
                'showPOSInterface':False
            }
            self.__cf = FilterInterface(config=self.__cf).getConfig()
            for key in self.__dataDic.keys():
                tmpDic = DataFilter(data=self.__dataDic[key],config=self.__cf).getDataDict()
                if len(tmpDic) > 0:
                    gruppedDataDic[key] = tmpDic['gruppedAll']
                    wholeDataDic[key] = tmpDic['wholeAll']
            chart, table, wordcloud, cases = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
            with chart:
                self.__Display(data_dic=gruppedDataDic, classType=Barchart2)
                self.prefixCtr +=1
            with table:
                self.__cf['SubTableXscale'] = .9
                self.__cf['SubTableYscale'] = 6.5
                self.__cf['SubTableFontSize'] = 24
                self.__Display(data_dic=gruppedDataDic, classType=Table2)
                self.prefixCtr += 1
            with wordcloud:
                self.__cf['objectToEnable'] = "Chart"
                self.__Display(data_dic=wholeDataDic, classType=WordCloudOfRephrase)
                self.prefixCtr += 1
            with cases:
                self.__cf['objectToEnable'] = "Text"
                self.__cf['SubTableXscale'] = .9
                self.__cf['SubTableYscale'] = 2
                self.__cf['SubTableFontSize'] = 18
                self.__Display(data_dic=wholeDataDic, classType=WordCloudOfRephrase)
                self.prefixCtr += 1
        elif module == "Parts of speech":
            self.__cf['showStopWordsInterface'] = False
            self.__cf['showInOutInterface'] = False
            self.__cf['showPOSInterface'] = True
            self.__cf = FilterInterface(config=self.__cf).getConfig()
            for key in self.__dataDic.keys():
                tmpDic = DataFilter(data=self.__dataDic[key],config=self.__cf).getDataDict()
                if len(tmpDic) > 0:
                    gruppedDataDic[key] = tmpDic['gruppedAll']
                    wholeDataDic[key] = tmpDic['wholeAll']
            chart, table, = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
            with chart:
                self.__Display(data_dic=gruppedDataDic, classType=Barchart2)
                self.prefixCtr +=1
            with table:
                self.__cf['SubTableXscale'] = .9
                self.__cf['SubTableYscale'] = 2
                self.__cf['SubTableFontSize'] = 18
                self.__Display(data_dic=gruppedDataDic, classType=Table2)
                self.prefixCtr += 1
        else:
            st.error("Unknown option for comparative analysis.")

    def __Display(self, data_dic: dict[str,pd.DataFrame()], classType: Any):
        if len(data_dic) > 1:
            a = classType
            fig, ax = plt.subplots(4, 2, figsize=(10,45), sharex=True)
            fig.subplots_adjust(left=-1, bottom=0.1, right=1.2, top=0.9, wspace=0.2, hspace=0.2)
            sns.set(font_scale=2)
            self.__cf['ax'] = ax
            [ k for k in a(dataDic=data_dic,config=self.__cf).getChartsDic().keys()]
            st.pyplot(fig=fig, config=DataProvider.getSaveConfig())
            fn = 'comparative_analysis.png'
            img = io.BytesIO()
            fig.savefig(img,fig=fig, format='png',height=1080, width=800,bbox_inches="tight")
            btn = st.download_button(
                label="Download as image",
                data=img,
                file_name=fn,
                mime="image/png"
            )
        else:
            st.write("**Add More Data to Compara.**")

    def __Distribution(self, data: pd.DataFrame, config: Dict[str, Any]):
        self.__cf = {
            'imediatePlot': False,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'categoriesColumn': '',
            'ADU_or_Speaker':"",
            'SS rephrase': False,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False
        }
        self.__cf = FilterInterface(config=self.__cf).getConfig()
        for key in self.__dataDic.keys():
            tmpDic = DataFilter(data=self.__dataDic[key],config=self.__cf).getDataDict()
            if len(tmpDic) > 0:
                gruppedDataDic[key] = tmpDic['gruppedAll']
                wholeDataDic[key] = tmpDic['wholeAll']
        chart, table, wordcloud, cases = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
        with chart:
            self.__Display(data_dic=gruppedDataDic, classType=Barchart2)
            self.prefixCtr +=1
        with table:
            self.__cf['SubTableXscale'] = .9
            self.__cf['SubTableYscale'] = 6.5
            self.__cf['SubTableFontSize'] = 24
            self.__Display(data_dic=gruppedDataDic, classType=Table2)
            self.prefixCtr += 1

# Save to file first or an image file has already existed.
# fn = 'scatter.png'
# plt.savefig(fn)
# with open(fn, "rb") as img:
#     btn = st.download_button(
#         label="Download image",
#         data=img,
#         file_name=fn,
#         mime="image/png"
#     )
