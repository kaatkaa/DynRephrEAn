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
from typing import Tuple
from wordcloud import WordCloud, STOPWORDS
from nltk.util import ngrams
from nltk import FreqDist

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
            number = st.slider("Pick top n unigrams: ", 1, value=10, max_value=len(wordLst))
            index = []
            for i in range(1,number+1):
                index.append(i)
            unigramsDf = pd.DataFrame(wordLst[:number],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
            unigramsDf.columns.name = unigramsDf.index.name
            st.dataframe(unigramsDf, width=800, height=40*number)

    def __RemoveStopWordsFromDf(self, dataF: pd.DataFrame(), columns: list[str]) -> pd.DataFrame:
        for stop_phrase in self.__stop_words_set:
            p1 = re.compile(r"\s"+stop_phrase+r"\s", flags=re.IGNORECASE)
            p2 = re.compile(r"^"+stop_phrase+r"\s|\s"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.IGNORECASE)
            for column in columns:
                #dataF[column].str.lower()
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        return dataF

    def __filterInterface(self, data: pd.DataFrame(), hideInOut: bool=False, useStopWords: bool=True) -> Tuple[any, list[str]]:
        col_radio1, = st.columns(1)
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: WordCloudOfEmotions",
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
        else:
            st.warning("Oprion not implemented in __filterInterface, class: WordCloudOfEmotions")
        if not hideInOut:
            source_options = st.multiselect("Choose source of data you would like to visualise", 
                                        ["input","output"], 
                                        ["input","output"][:],
                                        key = "multi_sel"+str(self.__keyCtr))
        else:
            source_options = ["input","output"]
        self.__keyCtr += 1
        col1, col2 = st.columns([2,2])
        showStopWords = False
        with col1:
            useStopWords = st.checkbox(label="Enable stop_words",value=useStopWords,key="StopWordsChck"+str(self.__keyCtr))
        with col2:
            showStopWords = st.checkbox(label="Show stop_words",value=showStopWords,key="ShowWordsChck"+str(self.__keyCtr))
        if showStopWords:
            st.write(self.__stop_words_set)
        if useStopWords:
            return self.__RemoveStopWordsFromDf(dataF=data_tmp, columns=source_options), source_options
        else:
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
        filteredDf, columnNamesLst = self.__filterInterface(data, hideInOut=True)
        plotDf = DataManipulator.getGruppedData(filteredDf,self.cf['colName'],"Frequency")
        wordLst = []
        for inOut in columnNamesLst: 
            for token in map(str,",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(",")):
                wordLst.extend(ngrams(token.split(" "), 1))
        wordLst = FreqDist(wordLst)
        number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst))
        ngramType = st.slider("Choose n-gram type: (1-4)",1,value=1, max_value=4)
        st.subheader("Pick phrase to analyse: ")
        NgramLst = []
        for inOut in columnNamesLst:
            for token in map(str,",".join(filteredDf[inOut].dropna().to_numpy(na_value="")).split(",")):
                NgramLst.extend(ngrams(token.split(" "), ngramType))
        NgramLst = FreqDist(NgramLst)
        common = NgramLst.most_common(number)
        w2 = [" ".join(item[0])+" : "+str(item[1]) for item in common]
        ndic = {}
        for ngram in common:
            if self.cf['colName'] in ndic:
                ndic[self.cf['colName']].append(" ".join(ngram[0]))
            else:
                ndic[self.cf['colName']] = [" ".join(ngram[0])]
            if 'Frequency' in ndic:
                ndic['Frequency'].append(ngram[1])
            else:
                ndic['Frequency'] = [ngram[1]]
        word = st.selectbox("Pick "+str(ngramType)+"-gram to analyse: ",w2,index=0,key='Dropdown_'+str(ngramType)+'-gramLst')
        regexpStr = re.sub(r"^(.*)\s:\s[0-9]+$", r"\1", word)
        regExpCode = r"\s"+regexpStr+r"\s|^"+regexpStr+r"\s|\s"+regexpStr+r"$|^"+regexpStr+r"$"
        st.subheader("Selected phrase is marked in text below between stars: \*\*"+regexpStr+"\*\*")
        col1, col2 = st.columns([2,2])
        if 'input' in columnNamesLst:
            with col1:
                filteredInputDF = filteredDf[filteredDf['input'].str.contains(regExpCode, case=False, regex=True)]
                filteredInputDF.reset_index(inplace=True)
                tmpDf = filteredInputDF[['input','output']]
                tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                tmpDf = tmpDf.style.applymap(backgroung_color,subset="input")
                st.table(tmpDf)
        if 'output' in columnNamesLst:
            with col2:
                filteredOutputDF = filteredDf[filteredDf['output'].str.contains(regExpCode, case=False, regex=True)]
                filteredOutputDF.reset_index(inplace=True)
                tmpDf = filteredOutputDF[['input','output']]
                tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                st.table(tmpDf[['input','output']].style.applymap(backgroung_color,
                    subset="output"))

        wyk = pd.DataFrame(ndic)            
        plotDf = pd.concat([plotDf, pd.DataFrame(ndic)])
        plotDf.reset_index(inplace=True)
        #st.write(len(plotDf[self.cf['colName']]))
        fig = barchart3d( \
            plotDf[self.cf['colName']], \
            plotDf['Frequency'].to_list(), \
            "Top "+str(number)+" most freguent "+str(ngramType)+"-grams", \
            str(ngramType)+"-gram frequency", \
            colorscale='Bluered', \
            opacity=0.6, \
            flatshading=True)

        #fig = go.Figure(
        #    data=go.Surface(z=filteredDf),
        #    layout=go.Layout(
        #        title="N-gram frequencies: ",
        #        width=500,
        #        height=500,
        #    )
        #)
        #fig.update_layout(template="plotly_dark", title="This is test")

        st.plotly_chart(fig, config=DataProvider.getSaveConfig())

    def __init__(self, data: pd.DataFrame(), analysisType: str, unit: str, configDic: dict[str , str]) -> None:
        self.cf = configDic
        if len(data) > 0:
            self.__keyCtr = 0
            self.__stop_words = DataProvider.getCustomStopWords() + list(STOPWORDS)
            self.__stop_words_set = set()
            for word in DataProvider.getCustomStopWords():
                self.__stop_words_set.add(word)
            for word in list(STOPWORDS):
                self.__stop_words_set.add(word)
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
                        "OS rephrase"),
                        key="Rephrase_Wordcloud_SSvsSO")
                if analysisType == 'Wordcloud':
                    if display_speakers == 'SS rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_sameSp'])
                        wl, df, options = self.__prepareWordCloud(sameSpeakerDf)
                        self.__Make_Word_Cloud(wl, df, options)
                    elif display_speakers == 'OS rephrase':
                        st.subheader(self.cf['Wordcloud_editReph_diffSp'])
                        wl2, df, options = self.__prepareWordCloud(diffSpeakerDf)
                        self.__Make_Word_Cloud(wl2, df, options)
                elif analysisType == 'Cases':
                    if display_speakers == 'SS rephrase':
                        st.subheader(self.cf['Cases_editReph_sameSp'])
                        self.__textAnalysis(sameSpeakerDf)
                    elif display_speakers == 'OS rephrase':
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
                    display_SORephr_chckbox = st.checkbox("OS rephrase",value=False,key="SO_rephr_chckbox")
                if display_SSRephr_chckbox:
                    if display_complexity == "4-categories":
                        st.subheader(self.cf['Distribution_general_1speaker'])
                        f1 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colName'])
                        st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                    elif display_complexity == '6-categories':
                        st.subheader(self.cf['Distribution_detailed_1speaker'])
                        f2 = self.__drawDistribution(sameSpeakerDf, display_unit, self.cf['colNameWS'])
                        st.plotly_chart(f2, config=DataProvider.getSaveConfig())
                if display_SORephr_chckbox:
                    if display_complexity == "4-categories":
                        st.subheader(self.cf['Distribution_general_2speakers'])
                        f3 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colName'])
                        st.plotly_chart(f3, config=DataProvider.getSaveConfig())
                    elif display_complexity == '6-categories':
                        st.subheader(self.cf['Distribution_detailed_2speakers'])
                        f4 = self.__drawDistribution(diffSpeakerDf, display_unit, self.cf['colNameWS'])
                        st.plotly_chart(f4, config=DataProvider.getSaveConfig())
        else:
            st.warning("You have to select data for analysis.")