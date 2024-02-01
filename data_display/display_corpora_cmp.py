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
from data_display.display_single_corpus import Piechart
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class ComparativeCorporaSimple:

    def __filterInterface(self, anCfg: dict[str,str],prefix: str):
        col_radio1, = st.columns(1)
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: ",
                ("4-categories",
                    "6-categories"),                                                  
                key="Rephrase_Comp_4-6cat"+prefix)
        if display_complexity == '4-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentions(), 
                                        DataProvider.getDynRephDimentions()[:],
                                        key = "multi_sel1"+prefix)
            selected = anCfg['colName']
        elif display_complexity == '6-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentionsWS(), 
                                        DataProvider.getDynRephDimentionsWS()[:],
                                        key = "multi_sel2"+prefix)
            selected = anCfg['colNameWS']
        return dyn_rephrase_options, selected
    
    def __filterInterfacePoS(self, anCfg: dict[str,str],prefix: str):
        col_radio1, = st.columns(1)
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: ",
                ("4-categories",
                    "6-categories"),                                                  
                key="RephrasePoS_Comp_4-6cat"+prefix)
        if display_complexity == '4-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentions(), 
                                        DataProvider.getDynRephDimentions()[:],
                                        key = "multi_sel1PoS"+prefix)
            selected = anCfg['colName']
        elif display_complexity == '6-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentionsWS(), 
                                        DataProvider.getDynRephDimentionsWS()[:],
                                        key = "multi_sePoS2"+prefix)
            selected = anCfg['colNameWS']

        inOutPOS = st.multiselect("Choose input/output", 
                                    sorted(DataProvider.getPSPcolumns()), 
                                    sorted(DataProvider.getPSPcolumns())[:],
                                    key = prefix+"_multiInOutPOS")
        POS_filter = st.multiselect("Choose parts of speech", 
                                    sorted(DataProvider.getPSPlst()), 
                                    sorted(DataProvider.getPSPlstDefault())[:],
                                    key = "multi_sePoS3"+prefix
                                    )
        return dyn_rephrase_options, selected, inOutPOS, POS_filter

    def __init__(self, data_dic: dict[str,pd.DataFrame()], anCfg: dict[str,str]):
        self.prefixCtr = 1
        module = st.radio("Choose: ", ("Distribution","Parts of speech"),label_visibility='collapsed', key=str(self.prefixCtr)+"CMP_module_")
        self.prefixCtr += 1

        if module == "Distribution":
            self.__options, self.__selected = self.__filterInterface(anCfg=anCfg, prefix=str(self.prefixCtr)+"Main_Filter")
            self.prefixCtr += 1
            self.__units = st.radio("Choose: ", ("Percentage","Number"),label_visibility='collapsed', key=str(self.prefixCtr)+"units_")
            self.prefixCtr += 1
            chart, table, wordcloud, cases = st.tabs([":bar_chart: Barchart",":black_square_button: Table",":cloud: WordClouds",":speech_balloon: Cases",])
            with chart:
                self.bigPlotDisp(data_dic=data_dic)
                self.prefixCtr +=1
            with table:
                self.tableDisp(data_dic=data_dic)
                self.prefixCtr += 1
            with wordcloud:
                st.write("To be implemented.")
            with cases:
                st.write("to be implemented")
        elif module == "Parts of speech":
            self.__options, self.__selected, self.__inOutPoS, self.__PoSselected = self.__filterInterfacePoS(anCfg=anCfg, prefix=str(self.prefixCtr)+"Main_FilterPoS")
            chart, table, = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
            with chart:
                st.write("Charts for PoS are not yet implemented")
            with table:
                st.write("Tables for PoS are not yet implemented.")
        else:
            st.error("Unknown option for comparative analysis.")

    def tableDisp(self, data_dic: dict[str,pd.DataFrame()]):
        
        if len(data_dic) > 1:
            if self.__units == "Number":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[self.__selected].isin(self.__options)]
                        data = DataManipulator.getGruppedData(data, self.__selected, col_name="Number")
                        self.__drawTable(data, pairs[0])
            elif self.__units == "Percentage":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[self.__selected].isin(self.__options)]
                        denominator = len(data)
                        data = DataManipulator.getGruppedPercentages(d=data, denominator=denominator, groupBy=self.__selected, col_name='Percentage')
                        self.__drawTable(data, pairs[0])     
        else:
            st.write("**Add More Data to Compara.**")


    def bigPlotDisp(self, data_dic: dict[str,pd.DataFrame()]):

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

    def __drawTable(self, df: Any, title: str):
        columnLst = list(df.columns.values)
        def make_pretty(styler):
            styler.set_caption(title)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        df.index += 1
        tmpDf = df.copy(deep=True)
        if len(columnLst) == 3:
            tmpDf = tmpDf[[columnLst[2],columnLst[1]]]
        st.table(make_pretty(tmpDf.style))

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