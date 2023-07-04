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

    def __Make_Word_Cloud(self, lexicon, data: pd.DataFrame(), options: list[str]) -> None:
        st.subheader("Word Cloud : ")
        wordcloud = WordCloud(stopwords=self.__stop_words, background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                            normalize_plurals=False).generate(" ".join(lexicon))
        fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
        ax.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig=fig)

        text = ""
        for inOut in options: 
            text += " ".join(map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")))
        if text != "":
            wordLst = sorted(WordCloud(stopwords=self.__stop_words).process_text(text).items(), key=lambda x:x[1], reverse=True)
            number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst))
            index = []
            for i in range(1,number+1):
                index.append(i)
            phrasesDf = pd.DataFrame(wordLst[:number],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
            phrasesDf.columns.name = phrasesDf.index.name
            st.dataframe(phrasesDf, width=800, height=40*number)

    def __filterInterface(self, data: pd.DataFrame()) -> Tuple[any, list[str]]:
        col_radio1, = st.columns(1)
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: ",
                ("4-categories",
                    "6-categories"),                                                  
                key="Rephrase_Piechart_ADU_4-6cat")
        if display_complexity == '4-categories':
            dyn_rephrase_options = st.multiselect(self.cf["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentions(), 
                                        DataProvider.getDynRephDimentions()[:],
                                        key = "multi_sel"+str(self.__keyCtr))
            self.__keyCtr += 1
            data_tmp = data.loc[data[self.cf['colName']].isin(dyn_rephrase_options)]
        elif display_complexity == '6-categories':
            dyn_rephrase_options = st.multiselect(self.cf["Wordcloud_filterInterface"], 
                                        DataProvider.getDynRephDimentionsWS(), 
                                        DataProvider.getDynRephDimentionsWS()[:],
                                        key = "multi_sel"+str(self.__keyCtr))
            self.__keyCtr += 1
            data_tmp = data.loc[data[self.cf['colNameWS']].isin(dyn_rephrase_options)]
        source_options = st.multiselect("Choose source of data you would like to visualise", 
                                    ["input","output"], 
                                    ["input","output"][:],
                                    key = "multi_sel"+str(self.__keyCtr))
        self.__keyCtr += 1
        return data_tmp, source_options
    
    def __prepareWordCloud(self, data: pd.DataFrame()) -> list():
        #st.subheader(f"Word Clouds for distribution of ethos dynamics in rephrase:")
        DataProvider.addSpacelines(1)        
        filteredDf, columnNamesLst = self.__filterInterface(data)
        joined_set = set()
        for inOut in columnNamesLst: 
            emo_set = set(",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(","))
            joined_set = joined_set | emo_set
        return list(joined_set), filteredDf, columnNamesLst

    def __textAnalysis(self, data: pd.DataFrame()) -> None:
        def backgroung_color(v):
            return f"background-color: {DataProvider.getRephraseAndEmptycolors()['Rephrase']};"
        filteredDf, columnNamesLst = self.__filterInterface(data)
        text = ""
        for inOut in columnNamesLst: 
            text += " ".join(map(str,",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(",")))
        if text != "":
            wordLst = sorted(WordCloud(stopwords=self.__stop_words).process_text(text).items(), key=lambda x:x[1], reverse=True)
            number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst))
            st.subheader("Pick word to analyse: ")
            w = [item[0] for item in wordLst]
            word = st.selectbox("Pick word/phrase to analyse: ",w[:number],index=0,key='Dropdown_lst')
            st.subheader("Selected phrase is marked in text below between stars: \*\*"+word+"\*\*")
            col1, col2 = st.columns([2,2])
            regexpStr = "^"+word+"\\s|\\s"+word+"\\s|\\s"+word+"$|^"+word+"$"
            if 'input' in columnNamesLst:
                with col1:
                    filteredInputDF = filteredDf[filteredDf['input'].str.contains(regexpStr, case=False, regex=True)]
                    filteredInputDF.reset_index(inplace=True)
                    tmpDf = filteredInputDF[['input','output']]
                    tmpDf = tmpDf.replace(regexpStr," **"+word+"** ", regex=True)
                    tmpDf = tmpDf.style.applymap(backgroung_color,subset="input")
                    st.table(tmpDf)
            if 'output' in columnNamesLst:
                with col2:
                    filteredOutputDF = filteredDf[filteredDf['output'].str.contains(regexpStr, case=False, regex=True)]
                    filteredOutputDF.reset_index(inplace=True)
                    tmpDf = filteredOutputDF[['input','output']]
                    tmpDf = tmpDf.replace(regexpStr," **"+word+"** ", regex=True)
                    st.table(tmpDf[['input','output']].style.applymap(backgroung_color,
                        subset="output"))

    def __init__(self, data: pd.DataFrame(), analysisType: str, unit: str, configDic: dict[str , str]) -> None:
        self.cf = configDic
        if len(data) > 0:
            self.__keyCtr = 0
            self.__stop_words = DataProvider.getCustomStopWords() + list(STOPWORDS)
            if unit == "ADU-Based Analysis":
                if analysisType == 'Wordcloud':
                    st.subheader(self.cf['Wordcloud_editReph_ADU'])
                    wl, df, options = self.__prepareWordCloud(data)
                    self.__Make_Word_Cloud(wl, df, options)
                    
                elif analysisType == 'Cases':
                    self.__textAnalysis(data)
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                col_radio1, col_radio2, col_radio3 = st.columns(3)
                with col_radio2:
                    display_speakers = st.radio("Choose speaker type: ",
                        ("SS rephrase",
                        "SO rephrase"),
                        key="Rephrase_Wordcloud_SSvsSO")
                if analysisType == 'Wordcloud':
                    if display_speakers == 'SS rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_sameSp'])
                        wl, df, options = self.__prepareWordCloud(sameSpeakerDf)
                        self.__Make_Word_Cloud(wl, df, options)
                    elif display_speakers == 'SO rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_diffSp'])
                        wl2, df, options = self.__prepareWordCloud(diffSpeakerDf)
                        self.__Make_Word_Cloud(wl2, df, options)
                elif analysisType == 'Cases':
                    if display_speakers == 'SS rephrase':
                        st.subheader(self.cf['Cases_editReph_sameSp'])
                        self.__textAnalysis(sameSpeakerDf)
                    elif display_speakers == 'SO rephrase':
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
                col_radio1, col_radio2 = st.columns(2)
                with col_radio1:
                    display_unit = st.radio("Choose display type: ",
                        ("percentage",
                        "number"),
                        key="Rephrase_Piechart_ADU_%_#")
                with col_radio2:
                    display_complexity = st.radio("Choose complexity level: ",
                        ("4-categories",
                         "6-categories"),                                                  
                        key="Rephrase_Piechart_ADU_4-6cat")
                if display_complexity == "4-categories":
                    #st.subheader(self.cf['Distribution_general_plot'])
                    f1 = self.__drawDistribution(data, display_unit, self.cf['colName'])
                    st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                elif display_complexity == "6-categories":
                    #st.subheader(self.cf['Distribution_detailed_plot'])
                    f2 = self.__drawDistribution(data, display_unit, self.cf['colNameWS'])
                    st.plotly_chart(f2, config=DataProvider.getSaveConfig())
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                col_radio1, col_radio2, col_radio3= st.columns(3)
                with col_radio1:
                    display_unit = st.radio("Choose display type: ",
                        ("percentage",
                        "number"),
                        key="Rephrase_Piechart_Speaker_%_#")
                with col_radio2:
                    display_complexity = st.radio("Choose complexity level: ",
                        ("4-categories",
                         "6-categories"),                                                  
                        key="Rephrase_Piechart_Speaker_4-6cat")
                with col_radio3:
                    display_SSRephr_chckbox = st.checkbox("SS rephrase",value=True,key="SS_rephr_chckbox")
                    display_SORephr_chckbox = st.checkbox("SO rephrase",value=False,key="SO_rephr_chckbox")
                if display_SSRephr_chckbox:
                    if display_complexity == "4-categories":
                        #st.subheader(self.cf['Distribution_general_1speaker'])
                        f1 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colName'])
                        st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                    elif display_complexity == '6-categories':
                        #st.subheader(self.cf['Distribution_detailed_1speaker'])
                        f2 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colNameWS'])
                        st.plotly_chart(f2, config=DataProvider.getSaveConfig())
                if display_SORephr_chckbox:
                    if display_complexity == "4-categories":
                        #st.subheader(self.cf['Distribution_general_2speakers'])
                        f3 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colName'])
                        st.plotly_chart(f3, config=DataProvider.getSaveConfig())
                    elif display_complexity == '6-categories':
                        #st.subheader(self.cf['Distribution_detailed_2speakers'])
                        f4 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colNameWS'])
                        st.plotly_chart(f4, config=DataProvider.getSaveConfig())
        else:
            st.warning("You have to select data for analysis.")