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

from submenus.single_corpus import SingleCorpusMenu
from config.config_data_colector import DataProvider
from submenus.comparative_corpus import CmpCorpusMenu

from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import streamlit.components.v1 as components

pd.set_option("max_colwidth", 300)
sns.set_theme(style="whitegrid")
plt.style.use("seaborn-talk")
 
# ******************* path to file **************************************

all_tw = r"./data_xlsx/ExprEmo_ASTL_CA_UK_US_byMU.xlsx"

# ********************** functions **************************************

def style_css(file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data(dir_address: str, label: str):
    data = pd.read_excel(dir_address, sheet_name=label)
    return data

# ******************* multi pages functions **************************************

def MainPage():
    st.title("Emotan Analytics")
    DataProvider.addSpacelines(2)

    st.write("#### Proper name")
    with st.expander("Read abstract"):
        DataProvider.addSpacelines(1)
        st.write("Some more information...")

    with st.container():
        DataProvider.addSpacelines(3)

        st.write("Paper related to the project: ")
        st.write("**Budzynska, K. et al. (2022). ....**")

        st.write("**[The New Ethos Lab](https://newethos.org/)**")
        st.write(" ************************** ")

    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;font-size=18px;}</style>', unsafe_allow_html=True)

# funkcje He
def Make_Word_Cloud(lexicon):
    wordcloud = WordCloud(background_color="#493E38", colormap='YlOrRd', width=1500, height=800,
                          normalize_plurals=False).generate(" ".join(lexicon))
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
    ax.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    return fig

def Word_Cloud(data, var):
    if var == "angry":
        unique_words = list(set(",".join(data["angry"].dropna().values).split(",")))
    elif var == "fear":
        unique_words = list(set(",".join(data["fear"].dropna().values).split(",")))
    elif var == "joy":
        unique_words = list(set(",".join(data["joy"].dropna().values).split(",")))
    elif var == "sadness":
        unique_words = list(set(",".join(data["sadness"].dropna().values).split(",")))
    elif var == "surprise":
        unique_words = list(set(",".join(data["surprise"].dropna().values).split(",")))
    else:
        unique_words = list(set(",".join(data["angry"].dropna().values.tolist() +
                                         data["fear"].dropna().values.tolist() +
                                         data["joy"].dropna().values.tolist() +
                                         data["sadness"].dropna().values.tolist() +
                                         data["surprise"].dropna().values.tolist()).split(",")))
    if len(unique_words) == 1 and len(unique_words[0]) == 0:
        f = st.info("No word cloud because of no {} in this corpus".format(var.lower()))
    else:
        f = st.pyplot(Make_Word_Cloud(unique_words))
    return f

def Find_Emotion(data, var):
    if var == "angry":
        word_type = "angry"
    elif var == "fear":
        word_type = "fear"
    elif var == "joy":
        word_type = "joy"
    elif var == "sadness":
        word_type = "sadness"
    else:
        word_type = "surprise"
    if len(data[word_type].dropna()) != 0:
        df = pd.DataFrame(list(",".join(data[word_type].dropna().values).split(",")), columns=["words"])
        df = df["words"].value_counts().reset_index()
        df.columns = ["words", "frequency"] 
    else:
        df = pd.DataFrame()
    return df

def Emotion_Language_Word_Cloud():
    st.subheader(f"Common High Precision Words")
    DataProvider.addSpacelines(2)
    word_type = st.selectbox(
        'choose an emotion category inside the corpus you would like to visualise',
        rhetoric_dims)
    DataProvider.addSpacelines(1)
    threshold_cloud = st.slider('Select a precision value (threshold) for a WordCloud',
                                0, 100, 100, disabled=False)
    st.info(f'Selected precision: **{threshold_cloud}**')

    # if len(options) != 0:
    global data
    st.write("#### 1. Word Cloud Visualisation")
    data = data.groupby(["Stevevee0101"])
    st.write(data.head())
   
    Word_Cloud(data, word_type)

    # st.write("#### 2. Word Frequency Visualisation")
    # if word_type == "angry":
    #     title = "Angry"
    # elif word_type == "fear":
    #     title = "Fear"
    # elif word_type == "joy":
    #     title = "Joy"
    # elif word_type == "sadness":
    #     title = "Sadness"
    # else:
    #     title = "Surprise"
    # olw_dataframe = Find_Emotion(data=data, var=word_type)

def Single_Distribution(data):
    st.subheader(f" Distribution Analysis ")
    DataProvider.addSpacelines(1)
    options = st.multiselect("Choose rhetoric categories you would like to visualise", rhetoric_dims, rhetoric_dims[:])

    if (len(data) > 0):
        data_Empty = pd.DataFrame()
        data_Empty = data.copy()
        data_Empty['Emotions'] = data_Empty['Emotions'].replace(np.nan, "Empty")
        data = data.loc[data['Emotions'].isin(options)]
        options.append('Empty')
        data_Empty = data_Empty.loc[data_Empty['Emotions'].isin(options)]
        data_Empty['Emotions'] = data_Empty['Emotions'].replace(rhetoric_dims, "Emotions")

        color_emo_empty = {'Emotions': '#3333FF','Empty': '#707070'}

        color_emo = {'anger': '#FF0000','sadness': '#BB0000', 
        'fear':'#990000', 'surprise': '#D87D00','joy': '#00BB70'}

        DataProvider.addSpacelines(2)
        f1 = sns.catplot(kind = "count", data = data_Empty.sort_values(by = ['Emotions']), x = "Emotions",
        aspect = 1.7, height = 7, alpha = 1, legend = False, palette = color_emo_empty)
        st.pyplot(f1)
        f2 = sns.catplot(kind = "count", data = data.sort_values(by = ['Emotions']), x = "Emotions",
        aspect = 1.7, height = 7, alpha = 1, legend = False, palette = color_emo)
        st.pyplot(f2)
        DataProvider.addSpacelines(1)

        st.write(f"*Title:*")
        
        number = st.slider("Pick a number of examples. ", 0, value=15, max_value=data.shape[0])
        st.dataframe(data[['name','text', 'Emotions']].iloc[:number].set_index("name"))
        st.write("Number of examples: ", number, '.')
        DataProvider.addSpacelines(1)
    else:
        st.write("Select leaders...")

def Emo_Comparative_Distribution(data_dic):
    color_emo = {'anger': '#FF0000','sadness': '#BB0000', 
        'fear':'#990000', 'surprise': '#D87D00','joy': '#00BB70'}
    units = st.radio("Choose: ", ("Number", "Percentage"), label_visibility='collapsed')
    options = st.multiselect("Choose rhetoric categories you would like to visualise", rhetoric_dims, rhetoric_dims[:])
    if len(data_dic) > 2:
        fig, ax = plt.subplots(2, 2, figsize=(14,18), sharex=True)
    else:
        fig, ax = plt.subplots(1, 2, figsize=(14,9), sharex=True)
    fig.subplots_adjust(left=-0.1, bottom=0.1, right=1.2, top=0.9, wspace=0.2, hspace=0.2)
    sns.set(font_scale=2)
    four_dim = [[0,0],[0,1],[1,0],[1,1]]
    if units == "Number":
        for ctr, pairs in enumerate(data_dic.items()):
            data = pairs[1]
            data = data.loc[data['Emotions'].isin(options)]
            if len(data_dic) > 2:
                x = sns.countplot(data = data.sort_values(by = ['Emotions']), y = "Emotions", ax=ax[four_dim[ctr][0],four_dim[ctr][1]],
                        palette = color_emo)
            else:
                x = sns.countplot(data = data.sort_values(by = ['Emotions']), y = "Emotions", ax=ax[ctr],
                        palette = color_emo)
            x.set(title=DataProvider.getCountryNameFormOption(pairs[0]))
            x.set_xlabel("Number",fontsize=20)
            x.set_ylabel("Emotions", fontsize=20)
            x.tick_params(labelsize=15)
    elif units == "Percentage":
        for ctr, pairs in enumerate(data_dic.items()):
            data = pairs[1]
            denominator = len(data)
            data = data.loc[data['Emotions'].isin(options)].groupby(['Emotions']).size().reset_index(name = 'Percentage')
            data['Percentage'] = data['Percentage'] / denominator
            data['Percentage'] = data['Percentage'] * 100
            data['Percentage'] = data['Percentage'].round().astype(int)
            if len(data_dic) > 2:
                z = sns.barplot(data = data, y ='Emotions', x = 'Percentage', ax=ax[four_dim[ctr][0],four_dim[ctr][1]], palette = color_emo)
            else:
                z = sns.barplot(data = data, y ='Emotions', x = 'Percentage', ax=ax[ctr], palette = color_emo)
            z.set(title=DataProvider.getCountryNameFormOption(pairs[0]))
            z.set_xlabel("Percentage",fontsize=20)
            z.set_ylabel("Emotions", fontsize=20)
            z.tick_params(labelsize=20)       
    plt.show()
    st.pyplot(fig)

def Comparative_Distribution(data, corpus):
    DataProvider.addSpacelines(1)
    data.rename(columns = {'Stevevee0101':'Emotions'}, inplace = True)

    data_Empty = pd.DataFrame()
    data_Empty = data.copy()
    data_Empty['Emotions'] = data_Empty['Emotions'].replace(np.nan, "Empty")
    data = data.loc[data['Emotions'].isin(options)]
    options.append('Empty')
    data_Empty = data_Empty.loc[data_Empty['Emotions'].isin(options)]
    data_Empty['Emotions'] = data_Empty['Emotions'].replace(rhetoric_dims, "Emotions")
    DataProvider.addSpacelines(2)

    color_emo_empty = {'Emotions': '#3333FF','Empty': '#707070'}

    color_emo = {'anger': '#FF0000','sadness': '#BB0000', 
    'fear':'#990000', 'surprise': '#D87D00','joy': '#00BB70'}

    f1 = sns.catplot(kind = "count", data = data_Empty.sort_values(by = ['Emotions']), x = "Emotions",
            aspect = 1.7, height = 7, alpha = 1, legend = False, palette = color_emo_empty)
    st.pyplot(f1)
    
    f2 = sns.catplot(kind = "count", data = data.sort_values(by = ['Emotions']), x = "Emotions",
            aspect = 1.7, height = 7, alpha = 1, legend = False, palette = color_emo)
    st.pyplot(f2)

    DataProvider.addSpacelines(1)
    st.write(f"*Title:*\n", corpus)
    number = st.slider("Pick a number of examples. ", 0, value=15, max_value=data.shape[0])
    st.dataframe(data[['source','sentence', 'Emotions', 'corpus']].iloc[:number])
    st.write("Number of examples: ", number, '.')
    DataProvider.addSpacelines(1)

def Time_Texts_Tendency(data):
    st.subheader(f"Text Type Distribution Across Different Dates")
    DataProvider.addSpacelines(1)
    col_radio1, col_radio2 = st.columns([2, 2], gap="medium")
    with col_radio1:
            unit = st.radio("Choose the unit of y-axis",
                            ("percentage",
                             "number",),
                            key="across dates")
    with col_radio2:
            var3 = st.radio("Choose the unit of text", ("post",))
    f1 = Emotional_Text_Tendency(data, unit)
    st.plotly_chart(f1)


def Emotional_Text_Tendency(data, unit):
    
    color_emo = {'anger': '#FF0000','sadness': '#BB0000', 
    'fear':'#990000', 'surprise': '#D87D00','joy': '#00BB70'}

    options = st.multiselect("Choose rhetoric categories you would like to visualise", rhetoric_dims, rhetoric_dims[:])

    if unit == "number":
        emo_data = data.groupby(["create_at"])["text"].count().reset_index()
        fig1 = go.Figure()
        for i, j in color_emo.items():
            fig1.add_trace(go.Bar(x=emo_data["create_at"],
                                  y=emo_data["text"],
                                  name=i,
                                  marker_color=j,
                                  hovertemplate="Date: %{x} <br> Number: %{y}", ))

        fig1.update_layout(barmode='group',
                           width=800,
                           height=400,
                           title={
                               'text': "Text Type Distribution Across Different Dates",
                               'y': 0.9,
                               'x': 0.5,
                               'xanchor': 'center',
                               'yanchor': 'top'})
        fig1.update_yaxes(type="log", ticklabelstep=2)
        fig1.update_xaxes(title_text='Dates', showgrid=True, ticks="outside", tickson="boundaries")
        fig1.update_yaxes(title_text='Number (log scale)')
    elif unit == "percentage":
        emo_data = (100 * data.groupby(["create_at"])["text"].count() / data.groupby(["create_at"])[
            "text"].count()).reset_index()
        fig1 = go.Figure()
        for i, j in color_emo.items():
            fig1.add_trace(go.Bar(x=emo_data["create_at"],
                                  y=emo_data["text"], name=i, marker_color=j,
                                  hovertemplate="Date: %{x} <br> Percentage: %{y}%",
                                  ))

        fig1.update_layout(barmode='group',
                           width=800,
                           height=400,
                           title={
                               'text': "Text Type Distribution Across Different Dates",
                               'y': 0.9,
                               'x': 0.5,
                               'xanchor': 'center',
                               'yanchor': 'top'})
        fig1.update_yaxes(type="log", ticklabelstep=2)
        fig1.update_xaxes(title_text='Dates', showgrid=True, ticks="outside", tickson="boundaries")
        fig1.update_yaxes(title_text='Percentage % (log scale)')
    return fig1

style_css(r"./multi_style.css")

@st.cache_resource
def SingleCorporaMenuLoader(data: pd, submenu_prefix: str) -> SingleCorpusMenu:
    return SingleCorpusMenu(data = data,tickerDic=DataProvider.getLeadersTicker(),prefix = submenu_prefix)

@st.cache_resource
def ComparativeCorpusMenuLoader(data: pd) -> CmpCorpusMenu:
    return CmpCorpusMenu(data)

#  *************************** sidebar  *********************************

with st.sidebar:
    st.write('<style>div[class="css-1siy2j7 e1fqkh3o3"] > div{background-color: #d2cdcd;}</style>', unsafe_allow_html=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
    st.title("Contents")
    emo_model = st.selectbox("Choose emotional model: ",("emotions_T5","emotions_MV","emotions_stevevee0101"),index = 1)
    data = load_data(all_tw, emo_model)
    single_corpora_menu = SingleCorporaMenuLoader(data=data, submenu_prefix="0_")
    comparative_corpus_menu = ComparativeCorpusMenuLoader(data=data)
    contents_radio = st.radio("Choose: ", ("Main Page", "Single Corpus Analysis", "Comparative Corpora Analysis"),label_visibility='collapsed')

if contents_radio == "Main Page":
    MainPage()
elif contents_radio == "Single Corpus Analysis":
    single_corpora_menu.sidebar()
elif contents_radio == "Comparative Corpora Analysis":
    comparative_corpus_menu.display()
else:
    st.error("Wrong option of main sidemenu radiobitton.")