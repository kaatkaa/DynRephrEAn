import streamlit as st
import io
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from config.config_data_manipulator import DataManipulator

class ComparativeCorporaSimple:

    def __filterInterface(self, anCfg: dict[str,str]):
        col_radio1, = st.columns(1)
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: ",
                ("4-categories",
                    "6-categories"),                                                  
                key="Rephrase_Comp_4-6cat")
        if display_complexity == '4-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentions(), 
                                        DataProvider.getDynRephDimentions()[:],
                                        key = "multi_sel1")
            selected = anCfg['colName']
        elif display_complexity == '6-categories':
            dyn_rephrase_options = st.multiselect(anCfg["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentionsWS(), 
                                        DataProvider.getDynRephDimentionsWS()[:],
                                        key = "multi_sel2")
            selected = anCfg['colNameWS']
        return dyn_rephrase_options, selected
    

    def __init__(self, data_dic: dict[str,pd.DataFrame()], anCfg: dict[str,str]):
        options, selected = self.__filterInterface(anCfg=anCfg)
        units = st.radio("Choose: ", ("Percentage","Number"),label_visibility='collapsed')
        fig, ax = plt.subplots(4, 2, figsize=(10,45), sharex=True)
        fig.subplots_adjust(left=-1, bottom=0.1, right=1.2, top=0.9, wspace=0.2, hspace=0.2)
        sns.set(font_scale=2)
        four_dim = [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]]
        if len(data_dic) > 1:
            if units == "Number":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[selected].isin(options)]
                        axTmp = ax[four_dim[ctr][0],four_dim[ctr][1]]
                        x = sns.countplot(data = data.sort_values(by = [selected]), y = selected, ax=axTmp,
                            palette = DataProvider.getEthosColors())
                        x.bar_label(x.containers[0], fmt='#%d')
                        x.grid(b=True, which='major', color='black', linewidth=0.075)
                        x.set(title=pairs[0])
                        x.set_xlabel("Number",fontsize=20)
                        x.set_ylabel("", fontsize=20)
                        x.tick_params(labelsize=15)
            elif units == "Percentage":
                for ctr, pairs in enumerate(data_dic.items()):
                    data = pairs[1]
                    if len(data) > 0:
                        data = data.loc[data[selected].isin(options)]
                        denominator = len(data)
                        data = DataManipulator.extractBarPlotPercentageData(d=data, denominator=denominator, groupBy=selected, col_name='Percentage')
                        z = sns.barplot(data = data, y = selected, x = 'Percentage', ax=ax[four_dim[ctr][0],four_dim[ctr][1]], 
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