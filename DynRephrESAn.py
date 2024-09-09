# imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from submenus.single_corpus import SingleCorpusMenu
from submenus.comparative_corpus import CmpCorpusMenu
from config.config_data_colector import DataProvider
from typing import Dict, Set, List, Tuple

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
    # 'posColumns': DataProvider.getInOutColLst()[2],
    #PoS categories selected
    'posCategories': DataProvider.getPoSlst(),
    'posTmpCategories': DataProvider.getPoSlstDefault(),
    #Select spaCy's tagger for different results
    'posTagType': '',
    #Limit the results between 1-100 to score
    'posLimittingSliderValue': 30,
    #Choose specipic PoS tag to display results with it
    'posSpecialContentName': "",
    'posSpecialContent': {},
    #Shows ngram slider
    'showNgramSlider': False,
    # Keeps ngram slider value
    'ngramSliderValue': 2
}

st.set_page_config(layout="wide")

# ******************* path to file **************************************

__rephrase_xlsx = r"./data_xlsx/DynRephrSEAnSortedNoConnId.xlsx"

# ********************** functions **************************************

def __style_css(self, file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def __load_data(dir_address: str) -> dict[str : pd.DataFrame()]:
    tmpDic = pd.read_excel(dir_address, sheet_name=None)
    # for corpoName in DataProvider.getCorporaSkipLst():
    #     if corpoName in tmpDic:
    #         del tmpDic[corpoName]
    return tmpDic

dataDic = __load_data(__rephrase_xlsx)

# ******************* multi pages functions **************************************

def __MainPage():
    st.title("Dynamics of Rephrase Analytics")
    DataProvider.addSpacelines(2)
    st.write("DynRephAn_ver_2.0")

    with st.expander("Read abstract"):
        DataProvider.addSpacelines(1)
        st.write("""
            The app DynRephAn was analysis 10 corpora: US2016redditD1, US2016redditR1, US2016redditG1
            (Reddit presidential debates during 2016 elections), US2016tvR1, US2016tvD1, US2016tvG1 (Televi-
            sion debates between candidates in 2016), Hansart (UK parliament debates), PolarIs1 - COVID19 vaccines debate 
            , PolarIs4 - a climate change discussion and lastly: ToyCorpus prepared for testing purposes. For now the data is
            provided through the *.xls file, but in the future it will be loaded directly from postgres database. The
            application shows dynamics of the rephrase in ethos (annotated manually except PolarIs 1) and sentiment (annotated
            automatically). The Ethos as well as Sentiment are both assigned to rephrased (input) and reprasing
            part (output) of rephrase and are classified into 3 categories: positive (ethotic support or positive
            emotions in sentiment), negative (ethotic attack on someone or negative emotions in sentiment) and
            neutral (no ethos or no emotions). 
            This analytic shows the dynamic nature of rephrase by taking into consideration both the rephrasing and rephrased part of rephrase. 
            For example if rephrase statement  
            is rephrased from:  
            \n- :green[neutral or negative (statement) to → positive : it would be called **Amelioration**],
            \n\n There are also other combinations:  
            \n- :red[positive or negative → neutral is called **Neutralization**],
            \n- :blue[positive or neutral → negative is called **Pejorativization**],
            \n- neutral or positive, or negative → to the same as on the left is called **No_Change**.
        """
        )

    with st.expander("Corpora statistics"):
        def make_pretty(styler):
            styler.set_caption("Data used in DynRephAn technology")
            styler.set_table_styles(DataProvider.getTableStatsFormat())
            return styler
        # tmpData = dataDic.items()
        tmpData = list()
        for x in dataDic.items():
            tmpData.append((x[0], x[1].drop_duplicates(),))
        names = [n[0] for n in tmpData]
        names1 = names + ["Total"]
        aduLen = [len(set(l[1]["id_input"].tolist()) | set(l[1]["id_output"].tolist())) for l in tmpData]
        aduLen1 = aduLen + [sum(aduLen)]
        inputText = [" ".join(i[1]["input"].tolist()) for i in tmpData]
        outputText = [" ".join(i[1]["output"].tolist()) for i in tmpData]
        loc_inputText = [" ".join(i[1]["locution_input"].tolist()) for i in tmpData]
        loc_outputText = [" ".join(i[1]["locution_output"].tolist()) for i in tmpData]
        inputSpeakers = [set(s[1]["speaker_input"].tolist()) for s in tmpData]
        outputSpeakers = [set(s[1]["speaker_output"].tolist()) for s in tmpData]
        allSpeakers = [x[0] | x[1] for x in zip(inputSpeakers, outputSpeakers)]
        inputSpeakersLen = [len(l) for l in inputSpeakers]
        outputSpeakersLen = [len(l) for l in outputSpeakers]
        allSpeakersLen = [len(l) for l in allSpeakers]
        inputWordsLen = [len(l.split(" ")) for l in inputText]
        outputWordsLen = [len(l.split(" ")) for l in outputText]
        allWordsLen = [a[0] + a[1] for a in zip(inputWordsLen, outputWordsLen)]
        loc_inputWordsLen = [len(l.split(" ")) for l in loc_inputText]
        loc_outputWordsLen = [len(l.split(" ")) for l in loc_outputText]
        allLocutionLen = [x[0] + x[1] for x in zip(loc_inputWordsLen, loc_outputWordsLen)]
        inputSpeakersLen1 = inputSpeakersLen + [sum(inputSpeakersLen)]
        outputSpeakersLen1 = outputSpeakersLen + [sum(outputSpeakersLen)]
        allSpeakersLen1 = allSpeakersLen + [sum(allSpeakersLen)]
        inputWordsLen1 = inputWordsLen + [sum(inputWordsLen)]
        outputWordsLen1 = outputWordsLen + [sum(outputWordsLen)]
        allWordsLen1 = allWordsLen + [sum(allWordsLen)]
        loc_inputWordsLen1 = loc_inputWordsLen + [sum(loc_inputWordsLen)]
        loc_outputWordsLen1 = loc_outputWordsLen + [sum(loc_outputWordsLen)]
        allLocutionLen1 = allLocutionLen + [sum(allLocutionLen)]
        statsDF = pd.DataFrame(data={"Corpus":names1,"# Words in ilocutions":allWordsLen1,"# Words in locutions":allLocutionLen1,
            "# ADUs":aduLen1,"# Speakers":allSpeakersLen1,"# Speakers input":inputSpeakersLen1,"# Speakers output":outputSpeakersLen1})
        statsDF.index += 1
        # st.write(tmpData)
        st.table(make_pretty(statsDF.style))
        #st.write(allSpeakers)

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