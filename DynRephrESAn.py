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
    'showPoS_subFreq': True,
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

    with st.expander("Abstract"):
        DataProvider.addSpacelines(1)
        st.write("""
Dynamics of Rephrase Analytics is the other foundational tool in Rhetoric Analytics, 
as it allows us to analyse the transformations of the use of rhetorical devices as a result of rephrasing information, 
i.e. to analyse them as they change when speakers rephrase what they say. 
The special role of DynRephAn consists in treating an argument relation of rephrase as a process of how a debate is evolving, 
how rhetorical devices are changed and manipulated by speakers. 
This means that we are able to inspect not only results of rhetorical use of language, 
e.g., by comparing the frequencies of using ethos or sentiment - expressed emotions, 
but we are also able to trace how speakers were strategically influencing the character of the discussion, 
e.g., by using different dynamic types of rephrase.
        """
        )

    with st.expander("Implementation details"):
        DataProvider.addSpacelines(1)
        st.write(
            """
        Streamlit package and Python were employed for the implementation of the web application. 
        Pandas package was utilised for data manipulation and seaborn and matplotlib for visualisation of results.
        DynRephAn allows to combine several corpora into one and analyse it as a single corpora 
        as well as compare patterns of rhetorical behaviour of dynamic changes of ethos or sentiment across corpora. 
        The app DynRephAn operates on 10 corpora: US2016redditD1, US2016redditR1, US2016redditG1 
        (Reddit presidential debates during 2016 elections), US2016tvR1, US2016tvD1, US2016tvG1 
        (Television debates between candidates in 2016), 
        Hansart (UK parliament debates), PolarIs1 - COVID19 vaccines debates, 
        PolarIs4 - a climate change discussion and lastly: ToyCorpus prepared for testing purposes. 
        Finally - ToyCorpus with carefully selected very small data sample used for testing the tool.
        For now the data is provided through the *.xls file, but in the future it will be loaded directly from postgres database.
        The unit of the analysis is textual. The app was inspired by LEPAn tool.
        DynRephAn Analytics are a sense-making tools that provides insights into strategic use of rephrases in language of argumentative discourse. 
        The technology uses data analytics techniques incorporating  visualisations in the form of pie charts 
        and bar charts as well as table data exports to represent data in a way easy to comprehend that allows us to observe statistical patterns,trends and tendencies.
        The tool also provides a way to see actual text content that represents rephrase in means of qualitative analysis. 
        Other options are display of the most frequent n-grams, analytics of parts of speech in rephrase, 
        n-grams of the most frequent parts of speech and 3D-view comparative analysis.
        This allows for large-scale discourse analysis, i.e., 
        we are able to make meaningful interpretations of vast amounts of information on how people actually use rephrase in several corpus-analysed discussions.\n
        \n ***Logos*** \n
        The annotation of logos in  Online Visualisation of Argument analysis tool (OVA) 
        follows the theoretical framework of Inference Anchoring Theory 
        (IAT: Budzynska, K., & Reed, C., (2011). Whence inference. Technical Report, University of Dundee)
        that is used for obtaining a rephrase - the starting point of data visualisation and analysis.\n
        \n ***Rephrase*** \n 
        Rephrase is defined as rhetorical argument between 
        INPUT and OUTPUT which are similar, 
        but OUTPUT  introduces some novel content 
        for achieving a certain rhetorical gain, 
        including loading an information with 
        ethotic appeals or emotions (sentiment) content. 
        For rephrese understood this way 
        both (input) and (output) parts 
        can curry different ethotic and sentiment values.\n
        Rephrase Example: \n
        Todo88: I don't see PAUL vs. SANDERS happening ⮕ kevo7777: PAUL vs. SANDERS won't happen \n
        \n ***Ethos*** \n
        The ethos defined here is an argument for or against 
        the character (credibility) of the speaker
        We follow a redefinition of the traditional conceptualisation of ethotic arguments, 
        and regard ethos as a speaker's property, 
        which can be attacked or supported by other speakers or neutral (no ethos) E0. 
        Thus, we treat favourable (positive) references to a speaker 
        (a person, a group of persons or an organisation) as ethotic supports E+
        and unfavourable (negative) references as ethotic attacks E-. \n
        Here are some ethos examples:\n
        Cooper: You've been a Republican [E-]
        Chafee: I was a liberal Republican [E+]\n
        \n ***Sentiment*** \n
        In Dynrephan sentiment is defined as emotions expressed by the speaker 
        and similarly to ethos, there are 3 categories classifying the type of emotion:
        S+ positive emotion, S- negative and S0 - no emotion.
        In contrast to Ethos, sentiment was mined automatically 
        by ''cardiffnlp/twitter-roberta-base-sentiment-latest`` LLM
        executed in colaboratori enviroment 
        with transformers[sentencepiece] python library.\n
        Here are some sentiment examples:\n
        Ebonic_Plague: cage breeding is the true scale 
        of how farm animals are raised in parts of the United States [S0]
        Ebonic_Plague: cage breeding is horrible [S-]
        \n ***Ethos or Sentiment Dynamics in The Rephrase*** \n
        DynRephAn analytic shows the dynamic nature of rephrase by 
        taking into consideration both the rephrasing INPUT 
        and rephrased OUTPUT part of rephrase. 
        For example if rephrase statement  
        is rephrased from:
        \n- :green[neutral or negative (Etos/Sentiment) to 
    ⮕ 
    positive : it would be called **Amelioration**,]\n
    Dynamic Ethotic Amelioration Example\:\n 
    :green[p_sweezy\: *It’s not like TRUMP was going to have a huge amount 
    support from the black community anyway* \[E-\]
    ⮕
    HollywoodCote\: *TRUMP doesn’t have much to lose from the black community* \[E+\]]
        \n\n There are also other combinations:  
        \n- :red[positive or neutral ⮕ negative is called **Pejorativization**,]\n
    Dynamic Ethotic Pejorativization Example\:\n
    :red[SaxMan100: *let TRUMP control the narrative* \[E+\]
    ⮕
    Hatewrecked: *stick to policy and facts let Tump be the ignorant talkative buffoon* \[E-\]]
        \n- :blue[positive or negative ⮕ neutral is called **Neutralization**,]\n
    Dynamic Ethotic Neutralization Example\:\n
    :blue[Wormhog\: *it does matter to woman in this country if they are
    represented in a government that tries to dictate what can and can’t do with
    our uteruses and tries to defund clinics providing birth control
    and reproductive health screenings to low-income women* \[E-\]
    ⮕
    Wormhog: *it’s important women have representation* \[E0\]]
        \n- neutral or positive, or negative 
        ⮕ 
    is the same as INPUT argument\: **No_Change**.\n
    Ethotic No_Change Example\:\n
    Speaker-1\: *gut reactions to a man screaming at a woman like a psychopath are usually negative* \[E-\]
    ⮕
    Speaker-1\: *I'm talking about viewers reaction to Trump's terrible pointing* \[E-\]
        """
        )

    with st.expander("Corpora statistics"):
        def make_pretty(styler):
            styler.set_caption("Basic Corpora Statistics")
            styler.set_table_styles(DataProvider.getTableStatsFormat())
            return styler
        
        def make_pretty2(styler):
            styler.set_caption("Basic Ethos & Sentiment Statistics")
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
        loc_outputText = [" ".join(i[1]["locution_output"].astype(str).tolist()) for i in tmpData]
        # loc_outputText = []
        # for i in tmpData:
        #     lst = i[1]["locution_output"].tolist()
        #     loc_outputText.append(" ".join(i[1]["locution_output"].tolist()))
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

        input_ethos = [ i[1]["input_ethos"].tolist() for i in tmpData]
        output_ethos = [ i[1]["output_ethos"].tolist() for i in tmpData]
        input_sentiment = [ i[1]["input_sentiment"].tolist() for i in tmpData]
        output_sentiment = [ i[1]["output_sentiment"].tolist() for i in tmpData]

        input_ethos_attacks = [ len([y for y in x if y=='E-']) for x in input_ethos]
        input_ethos_supports = [ len([y for y in x if y=='E+']) for x in input_ethos]
        input_ethos_noEthos = [ len([y for y in x if y=='no_ethos']) for x in input_ethos]
        output_ethos_attacks = [ len([y for y in x if y=='E-']) for x in output_ethos]
        output_ethos_supports = [ len([y for y in x if y=='E+']) for x in output_ethos]
        output_ethos_noEthos = [ len([y for y in x if y=='no_ethos']) for x in output_ethos]

        input_negative_sentiment = [ len([y for y in x if y=='negative']) for x in input_sentiment]
        input_positive_sentiment = [ len([y for y in x if y=='positive']) for x in input_sentiment]
        input_neutral_sentiment = [ len([y for y in x if y=='neutral']) for x in input_sentiment]
        output_negative_sentiment = [ len([y for y in x if y=='negative']) for x in output_sentiment]
        output_positive_sentiment = [ len([y for y in x if y=='positive']) for x in output_sentiment]
        output_neutral_sentiment = [ len([y for y in x if y=='neutral']) for x in output_sentiment]

        ethotic_attacks = [ x[0] + x[1] for x in zip(input_ethos_attacks, output_ethos_attacks)]
        ethotic_attacks1 = ethotic_attacks + [sum(ethotic_attacks)]
        ethotic_supprts = [ x[0] + x[1] for x in zip(input_ethos_supports, output_ethos_supports)]
        ethotic_supprts1 = ethotic_supprts + [sum(ethotic_supprts)]
        no_ethos = [ x[0] + x[1] for x in zip(input_ethos_noEthos, output_ethos_noEthos)]
        no_ethos1 = no_ethos = no_ethos + [sum(no_ethos)]

        negative_sentiment = [ x[0] + x[1] for x in zip(input_negative_sentiment, output_negative_sentiment) ]
        negative_sentiment1 = negative_sentiment + [sum(negative_sentiment)]
        positive_sentiment = [ x[0] + x[1] for x in zip(input_positive_sentiment, output_positive_sentiment) ]
        positive_sentiment1 = positive_sentiment + [sum(positive_sentiment)]
        no_sentiment = [ x[0] + x[1] for x in zip(input_neutral_sentiment, output_neutral_sentiment) ]
        no_sentiment1 = no_sentiment + [sum(no_sentiment)]

        ethosSentimentDF = pd.DataFrame(data={"Corpus":names1,"# Ethotic attacks":ethotic_attacks1,"# Ethotic Supports":ethotic_supprts1,
            "# No Ethos":no_ethos1,"# Negative Sentiment":negative_sentiment1,"# Positive Sentiment":positive_sentiment1,"# No Sentiment":no_sentiment1})

        DataProvider.addSpacelines(1)
        ethosSentimentDF.index += 1
        st.table(make_pretty2(ethosSentimentDF.style))

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