import streamlit as st
import sys
import pandas as pd
from typing import Tuple
from pandas.api.types import CategoricalDtype
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class WordCloudOfEmotions:

    def __Make_Word_Cloud(self, lexicon) -> None:
        st.subheader("Word Cloud : ")
        wordcloud = WordCloud(stopwords=self.__stop_words, background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                            normalize_plurals=False).generate(" ".join(lexicon))
        fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
        ax.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig=fig)

    def __filterInterface(self, data: pd.DataFrame()) -> Tuple[any, list[str]]:
        dyn_rephrase_options = st.multiselect(self.cf["Wordcloud_filterInterface"], 
                                    DataProvider.getDynRephDimentions(), 
                                    DataProvider.getDynRephDimentions()[:],
                                    key = "multi_sel"+str(self.__keyCtr))
        self.__keyCtr += 1
        data_WS = data.loc[data[self.cf['colNameWS']].isin(dyn_rephrase_options)]
        source_options = st.multiselect("Choose source of data you would like to visualise", 
                                    ["input","output"], 
                                    ["input","output"][:],
                                    key = "multi_sel"+str(self.__keyCtr))
        self.__keyCtr += 1
        return data_WS, source_options
    
    def __prepareWordCloud(self, data: pd.DataFrame()) -> list():
        #st.subheader(f"Word Clouds for distribution of ethos dynamics in rephrase:")
        DataProvider.addSpacelines(1)        
        filteredDf, columnNamesLst = self.__filterInterface(data)
        joined_set = set()
        for inOut in columnNamesLst: 
            emo_set = set(",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(","))
            joined_set = joined_set | emo_set
        return list(joined_set)

    def __textAnalysis(self, data: pd.DataFrame()) -> None:
        filteredDf, columnNamesLst = self.__filterInterface(data)
        text = ""
        for inOut in columnNamesLst: 
            text += " ".join(map(str,",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(",")))
        if text != "":
            wordLst = sorted(WordCloud(stopwords=self.__stop_words).process_text(text).items(), key=lambda x:x[1], reverse=True)
            number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst))
            index = []
            for i in range(1,number+1):
                index.append(i)
            phrasesDf = pd.DataFrame(wordLst[:number],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
            phrasesDf.columns.name = phrasesDf.index.name
            st.dataframe(phrasesDf, width=800, height=30*number)

    def __init__(self, data: pd.DataFrame(), analysisType: str, unit: str, configDic: dict[str , str]) -> None:
        self.cf = configDic
        if len(data) > 0:
            self.__keyCtr = 0
            self.__stop_words = DataProvider.getCustomStopWords() + list(STOPWORDS)
            if unit == "ADU-Based Analysis":
                if analysisType == 'Wordcloud':
                    st.subheader(self.cf['Wordcloud_editReph_ADU'])
                    wl = self.__prepareWordCloud(data)
                    self.__Make_Word_Cloud(wl)
                elif analysisType == 'Cases':
                    st.subheader(self.cf['Cases_editReph_ADU'])
                    self.__textAnalysis(data)
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                if analysisType == 'Wordcloud':
                    st.subheader(self.cf['Wordcloud_editReph_sameSp'])
                    wl = self.__prepareWordCloud(sameSpeakerDf)
                    self.__Make_Word_Cloud(wl)
                    st.subheader(self.cf['Wordcloud_editReph_diffSp'])
                    wl2 = self.__prepareWordCloud(diffSpeakerDf)
                    self.__Make_Word_Cloud(wl2)
                elif analysisType == 'Cases':
                    st.subheader(self.cf['Cases_editReph_sameSp'])
                    self.__textAnalysis(sameSpeakerDf)
                    st.subheader(self.cf['Cases_editReph_diffSp'])
                    self.__textAnalysis(diffSpeakerDf)
        else:
            st.warning("You have to provide corpora for text analysis.")

class Piechart:
    def __drawDistribution(self, data, unit, col_name):
        displayer = ""
        if unit == "percentage":
            displayer = 'percent+label'
        elif unit == "number":
            displayer = 'text+label'
        pie_df = (data.groupby([col_name]).size()).reset_index(name="number")
        fig = px.pie(pie_df, values='number', names=col_name, color=col_name,
                    color_discrete_map=DataProvider.getEthosColors()
        )
        fig.update_traces(textposition='inside', 
                    text=pie_df['number'].map("#{:,}".format),
                    textinfo=displayer)
        return fig

    def __init__(self, data: pd.DataFrame(), unit: str, configDic: dict[str , str]) -> None:
        self.cf = configDic
        st.subheader(self.cf['Distribution_top'])
        DataProvider.addSpacelines(1)
        if len(data) > 0:
            if unit == "ADU-Based Analysis":
                col_radio1, = st.columns(1)
                with col_radio1:
                    display_unit = st.radio("Choose display type: ",
                        ("percentage",
                        "number"),
                        key="Rephrase_Distribution_Piechart")
                f1 = self.__drawDistribution(data, display_unit, self.cf['colName'])
                st.subheader(self.cf['Distribution_general_plot'])
                st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                st.subheader(self.cf['Distribution_detailed_plot'])
                f2 = self.__drawDistribution(data, display_unit, self.cf['colNameWS'])
                st.plotly_chart(f2, config=DataProvider.getSaveConfig())
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                col_radio1, = st.columns(1)
                with col_radio1:
                    display_unit = st.radio("Choose display type: ",
                        ("percentage",
                        "number"),
                        key="Rephrase_Distribution_Piechart")
                f1 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colName'])
                st.subheader(self.cf['Distribution_general_1speaker'])
                st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                st.subheader(self.cf['Distribution_detailed_1speaker'])
                f2 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colNameWS'])
                st.plotly_chart(f2, config=DataProvider.getSaveConfig())
                f3 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colName'])
                st.subheader(self.cf['Distribution_general_2speakers'])
                st.plotly_chart(f3, config=DataProvider.getSaveConfig())
                st.subheader(self.cf['Distribution_detailed_2speakers'])
                f4 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colNameWS'])
                st.plotly_chart(f4, config=DataProvider.getSaveConfig())
        else:
            st.warning("You have to select data for analysis.")