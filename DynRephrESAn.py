# imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from submenus.single_corpus import SingleCorpusMenu
from submenus.comparative_corpus import CmpCorpusMenu
from config.config_data_colector import DataProvider
from PIL import Image
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
st.set_page_config(layout="wide")

# st.markdown(
#         f"""
# <style>
#     .reportview-container .main{{
#         max-width: 800px;
#         min-width: 400px;
#         padding-top: 2rem;
#         padding-right: 2rem;
#         padding-left: 2rem;
#         padding-bottom: 2rem;
#     }}
# </style>
# """,
#         unsafe_allow_html=True,
#     )

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
    st.write("DynRephAn_Extended_2")
    with st.expander("Read abstract"):
        DataProvider.addSpacelines(1)
        st.write("""
            Dynamics of Rephrase Analytics is the other foundational tool in Rhetoric Analytics, 
            as it allows us to analyse the transformations of the use of rhetorical devices as a result of rephrasing information, 
            i.e. to analyse them as they change when speakers rephrase what they say. 
            The special role of DynRephAn consists in treating an argument relation of rephrase as a process of how a debate is evolving, 
            how rhetorical devices are changed and manipulated by speakers. 
            This means that we are able to inspect not only results of rhetorical or linguistic use of language, 
            e.g., by comparing the frequencies of using logos vs ethos, 
            but we are also able to trace how speakers were strategically influencing the character of the discussion, 
            e.g., by shifting from using pure logos to using logos loaded with ethos."""
        )

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
        annotationUnits = st.radio("Unit picker",("Text-based","Entity-based"),
                    key="CMP_Text-Entity",
                    index=0)
        if annotationUnits == "Text-based":
            ADU_or_Speaker = st.radio("Next choose: ", ("ADU-Based Analysis",)
                , key="CMP_textUnits")
        elif annotationUnits == "Entity-based":
            ADU_or_Speaker = st.radio("Next choose: ", ("Speaker-Based Analysis",)
                , key="CMP_entityUnits")
    cmp_corpora_menu.display(ADU_or_Speaker)
else:
    st.error("Wrong option of main sidemenu radiobitton.")