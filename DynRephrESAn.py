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

__AnConfigId = "DynRephAnCfgId"
__AnConfig = {
    'prefix':'no_prefix_set_',
    # imediatePlot - set to True if plotting single corpora charts 
    # - to False if plotting in comparative analysis charts
    'imediatePlot': True,
    # For tables wit text, how much lines has to be shown from table
    'textInstances': 1,
    # Dimentions of comparative analysis chart:
    '_8x_dims': [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]],
    # The position (0-7) of current chart in subplot for comparative analysis
    'subChartPosition': 0,
    # ax of subplot
    'ax': None,
    # subplot table customalisation paremeters
    'SubTableXscale': .9,
    'SubTableYscale': 6.5,
    'SubTableFontSize': 24,
    # end of subplot Table configuration
    # Variable below enables "Chart" or "Text" component in SuperTextComponent superclass
    'objectToEnable': "Chart",
    #Number or percentage
    'showPercentageNumber': False,
    'unitPercentNumberIndex': 0,
    'unitPercentNumber': 'Percentage',
    'unitsPercentageNumber': ('Percentage','Number'),
    #categories interface
    'showCategoriesInterface': False,
    'categoryIndex': 0,
    'categoriesColumn': '',
    'categoriesLst': DataProvider.getDynRephDimentions(),
    'categoriesLstWS': DataProvider.getDynRephDimentionsWS(),
    # 'fixedCatLst': [],
    'categoriesInterfaceTitle': 'Wordcloud_filterInterface',
    # ADU or speaker
    'ADU_or_Speaker': '',
    'SS rephrase': False,
    'OS rephrase': False,
    'SS + OS rephrase': True,
    # Use Input or Output phrase
    'showInOutInterface': True,
    'InOutTypeIndex': 0,
    # use radiobutton interface to choose between Input output and Locution input and output
    # 'showInOutVsLoc': False,
    # List that remembers selected Input output or locution input and output
    'inOutLstSub': DataProvider.getInOutColLst()[0],
    'inOutLstSub_loc': DataProvider.getInOutColLst()[1],
    'inOutLstSub_PoS': DataProvider.getInOutColLst()[2],
    'inOutLstSub_LPoS': DataProvider.getInOutColLst()[3],
    'inOutLst': DataProvider.getInOutColLst()[0],
    # Color palette for barchar 2 types for Dynamic rephrase and PoS
    'palette': DataProvider.getEthosColors(),
    # use stopwords interface
    'showStopWordsInterface':False,
    'showStopwords':False,
    'useStopwords':False,
    'StopwordsSet': set(),
    'showStopPoSInterface':False,
    'stopPoSSet': set (),
    #Interface of PoS
    'showPOSInterface':False,
    #PoS column names in excel to choose from
    'posColumns': DataProvider.getInOutColLst()[2],
    #PoS categories selected
    'posCategories': DataProvider.getPSPlst(),
    # Shows ngram slider
    'showNgramSlider': False,
    # Keeps ngram slider value
    'ngramSliderValue': 2
}

st.set_page_config(layout="wide")

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

def __MainPage():
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

def __SingleCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()], submenu_prefix: str) -> SingleCorpusMenu:
    return SingleCorpusMenu(dataDic = dataDic, prefix = submenu_prefix)

def __ComparativeCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()]) -> CmpCorpusMenu:
    return CmpCorpusMenu(dataDict=dataDic)

# def __resetData(single_corpus: SingleCorpusMenu, comparative_corpora: CmpCorpusMenu) -> None:
#     single_corpus.cleanSelections()
#     comparative_corpora.clearTabsSelections()
if __AnConfigId not in st.session_state:
    st.session_state['cfgId'] = __AnConfigId
    st.session_state[st.session_state['cfgId']] = __AnConfig
with st.sidebar:
    st.write('<style>div[class="css-1siy2j7 e1fqkh3o3"] > div{background-color: #d2cdcd;}</style>', unsafe_allow_html=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
    dataDic = __load_data(__rephrase_xlsx)
    st.subheader("Analytics type")
    anSubtype = st.radio("", ("DynRephAn for Ethos",
                            "DynRephAn for Sentiment"),
                key="AnType", label_visibility='collapsed')
    st.session_state[st.session_state['cfgId']]['generalConfig'] = DataProvider.getDynRephrESconfig()[anSubtype]
        
    __single_corpora_menu = __SingleCorporaMenuLoader(dataDic=dataDic, submenu_prefix="0_")
    __cmp_corpora_menu = __ComparativeCorporaMenuLoader(dataDic=dataDic)
    st.title("Contents")
    contents_radio = st.radio("Choose: ", ("Main Page", "Single Corpus Analysis", "Comparative Corpora Analysis"),label_visibility='collapsed')

if contents_radio == "Main Page":
    __MainPage()
elif contents_radio == "Single Corpus Analysis":
    __single_corpora_menu.sidebar()
elif contents_radio == "Comparative Corpora Analysis":
    with st.sidebar:
        st.button("Clear All Tabs",key="tabs_clear",on_click=__cmp_corpora_menu.clearTabsSelections)
        st.subheader("Analysis Units")
        ADU_or_Speaker = st.radio("Unit picker",("Text-Based Analysis",),
                    key="CMP_Text-Entity",
                    index=0,
                    label_visibility='hidden')
    __cmp_corpora_menu.display(ADU_or_Speaker)
else:
    st.error("Wrong option of main sidemenu radiobitton.")