import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.data as pdata
from data_display.barchart3d import barchart3d
from pandas.api.types import CategoricalDtype
from typing import Tuple, List
from wordcloud import WordCloud, STOPWORDS
from nltk.util import ngrams
from nltk import FreqDist

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class WordCloudOfEmotions:

    def __Make_Word_Cloud(self, lexicon, data: pd.DataFrame(), options: list[str]) -> None:
        st.subheader("Word Cloud : ")
        wordcloudTab, tableTab = st.tabs([":cloud: Wordcloud",":black_square_button: Cases"])

        with wordcloudTab:
            wordcloud = WordCloud(stopwords=self.__stop_words, background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                                normalize_plurals=False).generate(" ".join(lexicon))
            fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
            ax.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig=fig)

        with tableTab:
            text = ""
            for inOut in options: 
                text += " ".join(map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")))
            if text != "":
                wordLst = sorted(WordCloud(stopwords=self.__stop_words).process_text(text).items(), key=lambda x:x[1], reverse=True)
                number = st.slider("Pick top n unigrams: ", 1, value=10, max_value=len(wordLst))
                index = []
                for i in range(1,number+1):
                    index.append(i)
                unigramsDf = pd.DataFrame(wordLst[:number],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
                unigramsDf.columns.name = unigramsDf.index.name
                st.dataframe(unigramsDf, width=800, height=40*number)

    def __prepareWordCloud(self, data: pd.DataFrame()) -> list():
        #st.subheader(f"Word Clouds for distribution of ethos dynamics in rephrase:")
        DataProvider.addSpacelines(1)        
        filteredDf, columnNamesLst = self.__filterInterface(data)
        joined_set = set()
        for inOut in columnNamesLst: 
            emo_set = set(",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(","))
            joined_set = joined_set | emo_set
        return list(joined_set), filteredDf, columnNamesLst
    
    def __init__(self, data: pd.DataFrame(), unit: str, configDic: dict[str , str], prefix: str) -> None:
        self.cf = configDic
        self.prefix = prefix
        if len(data) > 0:
            if unit == "ADU-Based Analysis":
                st.subheader(self.cf['Wordcloud_editReph_ADU'])
                wl, df, options = self.__prepareWordCloud(data)
                self.__Make_Word_Cloud(wl, df, options)
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                col_radio1, col_radio2, col_radio3 = st.columns(3)
                with col_radio2:
                    display_speakers = st.radio("Choose speaker type: ",
                        ("SS rephrase",
                        "OS rephrase"),
                        key=self.prefix+"_Rephrase_Wordcloud_SSvsSO")
                    if display_speakers == 'SS rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_sameSp'])
                        wl, df, options = self.__prepareWordCloud(sameSpeakerDf)
                        self.__Make_Word_Cloud(wl, df, options)
                    elif display_speakers == 'OS rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_diffSp'])
                        wl2, df, options = self.__prepareWordCloud(diffSpeakerDf)
                        self.__Make_Word_Cloud(wl2, df, options)
        else:
            st.warning("You have to provide corpora for text analysis.")