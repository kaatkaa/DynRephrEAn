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
        module = st.radio("Choose: ", ("Distribution","Parts of speech"),label_visibility='collapsed', key=str(self.prefixCtr)+"CMP_module_")
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
            chart, table, wordcloud, cases = st.tabs([":bar_chart: Barchart",":black_square_button: Table",":cloud: WordClouds",":speech_balloon: Top20Words",])
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


    def __Old(self, data_dic: dict[str,pd.DataFrame()]):

        fig, ax = plt.subplots(4, 2, figsize=(10,45), sharex=True)
        fig.subplots_adjust(left=-1, bottom=0.1, right=1.2, top=0.9, wspace=0.2, hspace=0.2)
        sns.set(font_scale=2)
        four_dim = [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]]
        if len(data_dic) > 1:
            if self.__units == "Number":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[self.__selected].isin(self.__options)]
                        axTmp = ax[four_dim[ctr][0],four_dim[ctr][1]]
                        x = sns.countplot(data = data.sort_values(by = [self.__selected]), y = self.__selected, ax=axTmp,
                            palette = DataProvider.getEthosColors())
                        x.bar_label(x.containers[0], fmt='#%d')
                        x.grid(b=True, which='major', color='black', linewidth=0.075)
                        x.set(title=pairs[0])
                        x.set_xlabel("Number",fontsize=20)
                        x.set_ylabel("", fontsize=20)
                        x.tick_params(labelsize=15)
            elif self.__units == "Percentage":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[self.__selected].isin(self.__options)]
                        denominator = len(data)
                        data = DataManipulator.getGruppedPercentages(d=data, denominator=denominator, groupBy=self.__selected, col_name='Percentage')
                        axTmp = ax[four_dim[ctr][0],four_dim[ctr][1]]
                        # # Create an array with the colors you want to use
                        # colors = []
                        # for name, val in sorted(DataProvider.getEthosColors().items(), key=lambda x:x[1], reverse=True):
                        #     if name in options:
                        #         colors.append(val)
                        # # Set your custom color palette
                        # customPalette = sns.set_palette(sns.color_palette(colors))
                        # z = axTmp.pie(data.sort_values(by = [selected])['Percentage'], labels=options, colors=customPalette, autopct='%d%%')
                        z = sns.barplot(data = data, y = self.__selected, x = 'Percentage', ax=ax[four_dim[ctr][0],four_dim[ctr][1]], 
                            palette = DataProvider.getEthosColors())
                        z.bar_label(z.containers[0], fmt='%d%%')
                        z.grid(b=True, which='major', color='black', linewidth=0.075)
                        z.set(title=pairs[0])
                        z.set_xlabel("Percentage",fontsize=20)
                        z.set_ylabel("", fontsize=20)
                        z.tick_params(labelsize=20)       
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
