# imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly
import plotly.graph_objects as go
import wordcloud
import os
import json

from submenus.single_corpus import SingleCorpusMenu
from submenus.comparative_corpus import CmpCorpusMenu
from submenus.three_d_corpus import ThreeDCorpusMenu
from submenus._3D_PSP_corpus import _3D_PSP_corpus
from config.config_data_colector import DataProvider

from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import streamlit.components.v1 as components

pd.set_option("max_colwidth", 300)
sns.set_theme(style="whitegrid")
plt.style.use("seaborn-talk")
 
# ******************* path to file **************************************

rephrase_xlsx = r"./data_xlsx/DynRephrSEAn.xlsx"

# ********************** functions **************************************

def style_css(file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#style_css('multi_style.css')

@st.cache_data
def load_data(dir_address: str) -> dict[str : pd.DataFrame()]:
    tmpDic = pd.read_excel(dir_address, sheet_name=None)
    # for corpoName in DataProvider.getCorporaSkipLst():
    #     if corpoName in tmpDic:
    #         del tmpDic[corpoName]
    return tmpDic

# ******************* multi pages functions **************************************

def MainPage():
    st.title("Dynamics of Rephrase Analytics")
    DataProvider.addSpacelines(2)

    st.write("#### DynRephAn")
    with st.expander("Read abstract"):
        DataProvider.addSpacelines(1)
        st.write("Some more information...")

    with st.container():
        DataProvider.addSpacelines(3)

        st.write("**[The New Ethos Lab](https://newethos.org/)**")
        st.write(" ************************** ")

    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;font-size=18px;}</style>', unsafe_allow_html=True)

@st.cache_resource
def SingleCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()], submenu_prefix: str, anType: str) -> SingleCorpusMenu:
    return SingleCorpusMenu(dataDic = dataDic, prefix = submenu_prefix, anType=anType)

@st.cache_resource
def ComparativeCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()], anType: str) -> CmpCorpusMenu:
    return CmpCorpusMenu(dataDict=dataDic, anType=anType)

# @st.cache_data
# def ThreeDCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()],submenu_prefix: str, anType: str) -> ThreeDCorpusMenu:
#     return ThreeDCorpusMenu(dataDic=dataDic, prefix=submenu_prefix, anType=anType)

# @st.cache_data
# def _3D_PSPCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()],submenu_prefix: str, anType: str) -> _3D_PSP_corpus:
#     return _3D_PSP_corpus(dataDic=dataDic, prefix=submenu_prefix, anType=anType)

def resetData(single_corpus: SingleCorpusMenu, comparative_corpora: CmpCorpusMenu) -> None:
    single_corpus.cleanSelections()
    comparative_corpora.clearTabsSelections()

#  *************************** sidebar  *********************************

with st.sidebar:
    st.write('<style>div[class="css-1siy2j7 e1fqkh3o3"] > div{background-color: #d2cdcd;}</style>', unsafe_allow_html=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
    dataDic = load_data(rephrase_xlsx)
    st.subheader("Analytics type")
    single_corpora_menu = None
    cmp_corpora_menu = None
    rAnalytics = st.radio("", ("DynRephAn for Ethos",
                            "DynRephAn for Sentiment"),
                key="AnType")
    single_corpora_menu = SingleCorporaMenuLoader(dataDic=dataDic, submenu_prefix="0_", anType=rAnalytics)
    cmp_corpora_menu = ComparativeCorporaMenuLoader(dataDic=dataDic, anType=rAnalytics)
    # threeD_corpora_EthOrSent = ThreeDCorporaMenuLoader(dataDic=dataDic, submenu_prefix="3D_1", anType=rAnalytics)
    # threeD_corpora_EthAndSent = ThreeDCorporaMenuLoader(dataDic=dataDic, submenu_prefix="3D_2", anType=rAnalytics)
    # pSP = _3D_PSPCorporaMenuLoader(dataDic=dataDic, submenu_prefix="3D_3", anType=rAnalytics)
    st.title("Contents")
    contents_radio = st.radio("Choose: ", ("Main Page", "Single Corpus Analysis", "Comparative Corpora Analysis"),label_visibility='collapsed')

if contents_radio == "Main Page":
    MainPage()
elif contents_radio == "Single Corpus Analysis":
    single_corpora_menu.sidebar()
elif contents_radio == "Comparative Corpora Analysis":
    with st.sidebar:
        st.button("Clear All Tabs",key="tabs_clear",on_click=cmp_corpora_menu.clearTabsSelections)
        st.subheader("Analysis Units")
        units_choice = st.radio("", ("ADU-Based Analysis",
                                        "Speaker-Based Analysis"
                                        ), key="Cmp_units",
                                        on_change=resetData,
                                        args=(single_corpora_menu, cmp_corpora_menu))
    cmp_corpora_menu.display(units_choice)
# elif contents_radio == "3D Charts":
#     with st.sidebar:
#         _3D_Choice = st.radio("Choose 3D diagram", ("Ethos or Sentiment","Ethos and Sentiment", "3D_PartsOfSpeech"))
#     if _3D_Choice == "Ethos or Sentiment":
#         threeD_corpora_EthOrSent.draw3D(bothEthosPathos=False)
#     elif _3D_Choice == "Ethos and Sentiment":
#         threeD_corpora_EthAndSent.draw3D(bothEthosPathos=True)
#     elif _3D_Choice == "3D_PartsOfSpeech":
#         pSP.draw3D()
#     else:
#         st.warning("This option of 3D chart: '",_3D_Choice,"' is not implemented.")
else:
    st.error("Wrong option of main sidemenu radiobitton.")