# imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from submenus.single_corpus import SingleCorpusMenu
from submenus.comparative_corpus import CmpCorpusMenu
from config.config_data_colector import DataProvider

pd.set_option("max_colwidth", 300)
sns.set_theme(style="whitegrid")
plt.style.use("seaborn-talk")

class DynRephAnMainInterface:
    # ******************* path to file **************************************

    __rephrase_xlsx = r"./data_xlsx/DynRephrSEAn.xlsx"

    # ********************** functions **************************************

    def __style_css(self, file):
        with open(file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    @st.cache_resource
    @staticmethod
    def __load_data(dir_address: str) -> dict[str : pd.DataFrame()]:
        tmpDic = pd.read_excel(dir_address, sheet_name=None)
        # for corpoName in DataProvider.getCorporaSkipLst():
        #     if corpoName in tmpDic:
        #         del tmpDic[corpoName]
        return tmpDic

    # ******************* multi pages functions **************************************

    def __MainPage(self):
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

    def __SingleCorporaMenuLoader(self, dataDic: dict[str:pd.DataFrame()], submenu_prefix: str, anType: str) -> SingleCorpusMenu:
        return SingleCorpusMenu(dataDic = dataDic, prefix = submenu_prefix, anType=anType)

    def __ComparativeCorporaMenuLoader(self, dataDic: dict[str:pd.DataFrame()], anType: str) -> CmpCorpusMenu:
        return CmpCorpusMenu(dataDict=dataDic, anType=anType)

    # def __resetData(single_corpus: SingleCorpusMenu, comparative_corpora: CmpCorpusMenu) -> None:
    #     single_corpus.cleanSelections()
    #     comparative_corpora.clearTabsSelections()

    def __init__(self) -> None:
        #self.__style_css('multi_style.css')
        with st.sidebar:
            st.write('<style>div[class="css-1siy2j7 e1fqkh3o3"] > div{background-color: #d2cdcd;}</style>', unsafe_allow_html=True)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
            dataDic = DynRephAnMainInterface.__load_data(DynRephAnMainInterface.__rephrase_xlsx)
            st.subheader("Analytics type")
            rAnalytics = st.radio("", ("DynRephAn for Ethos",
                                    "DynRephAn for Sentiment"),
                        key="AnType")
            self.__single_corpora_menu = self.__SingleCorporaMenuLoader(dataDic=dataDic, submenu_prefix="0_", anType=rAnalytics)
            self.__cmp_corpora_menu = self.__ComparativeCorporaMenuLoader(dataDic=dataDic, anType=rAnalytics)
            st.title("Contents")
            contents_radio = st.radio("Choose: ", ("Main Page", "Single Corpus Analysis", "Comparative Corpora Analysis"),label_visibility='collapsed')

        if contents_radio == "Main Page":
            self.__MainPage()
        elif contents_radio == "Single Corpus Analysis":
            self.__single_corpora_menu.sidebar()
        elif contents_radio == "Comparative Corpora Analysis":
            with st.sidebar:
                st.button("Clear All Tabs",key="tabs_clear",on_click=self.__cmp_corpora_menu.clearTabsSelections)
                st.subheader("Analysis Units")
                ADU_or_Speaker = st.radio("Unit picker",("Text-Based Analysis",),
                            key="CMP_Text-Entity",
                            index=0,
                            label_visibility='hidden')
            self.__cmp_corpora_menu.display(ADU_or_Speaker)
        else:
            st.error("Wrong option of main sidemenu radiobitton.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    DynRephAnMainInterface()