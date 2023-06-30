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

class Overall:
    def __init__(self, data: pd.DataFrame()):
        st.subheader(f" Statistics and Qualitative analysis: ")
        unit = st.radio("Choose unit: ", ("Number", "Percentage"))
        DataProvider.addSpacelines(1)
        options = st.multiselect("Choose rephrase categories you would like to visualise", DataProvider.getRephraseDimentions(), DataProvider.getRephraseDimentions()[:])

        if (len(data) > 0):
            refEmpty_df = data.copy()
            refEmpty_df['Rephrase_type'] = refEmpty_df['Rephrase_type'].replace(DataProvider.getRephraseDimentions(), "Rephrase")
            rephrase_order = CategoricalDtype(
                DataProvider.getRephraseDimentions(), 
                ordered=True
            )
            if unit == "Number":
                data = data.loc[data['Rephrase_type'].isin(options)]
                data['Rephrase_type'] = data['Rephrase_type'].astype(rephrase_order)
                DataProvider.addSpacelines(2)
                # st.subheader(f"Frequency: Rephrase vs No Rephrase")
                # f1 = sns.catplot(kind = "count", data = refEmpty_df.sort_values(by = ["Rephrase_type"]), x = "Rephrase_type",
                # aspect = 1.7, height = 7, alpha = 1, legend = False, palette = DataProvider.getRephraseAndEmptycolors())
                # st.pyplot(f1)

                DataProvider.addSpacelines(1)
                st.subheader(f"Rephrase frequencies detected: ")
                f2 = sns.catplot(kind = "count", data = data.sort_values('Rephrase_type'), x = "Rephrase_type",
                aspect = 1.7, height = 7, alpha = 1, legend = False, palette = DataProvider.getRephraseColors())
                st.pyplot(f2)
            elif unit == "Percentage":
                sns.set_style('whitegrid')
                den = len(data)
                data = data.loc[data['Rephrase_type'].isin(options)]
                data_Ref = DataManipulator.getGruppedPercentages(d=data, denominator=den,groupBy="Rephrase_type", col_name="Percentage")
                data_Ref['Rephrase_type'] = data_Ref['Rephrase_type'].astype(rephrase_order)
                refEmpty_df = DataManipulator.getGruppedPercentages(d=refEmpty_df, denominator=den,groupBy="Rephrase_type", col_name="Percentage")
                DataProvider.addSpacelines(2)

                # st.subheader(f"Percentage: Rephrase vs No Rephrase")
                # fig1 = plt.figure(figsize=(10, 5))
                # f1 = sns.barplot(data = refEmpty_df.sort_values(by = ['Rephrase_type']), y = "Percentage", x = "Rephrase_type",
                #     alpha = 1, palette = DataProvider.getRephraseAndEmptycolors())
                # st.pyplot(fig1)

                DataProvider.addSpacelines(1)
                st.subheader(f"Rephrase percentages detected: ")
                fig2 = plt.figure(figsize=(10, 5))
                f2 = sns.barplot(data = data_Ref.sort_values('Rephrase_type'), y = "Percentage", x = "Rephrase_type",
                    alpha = 1, palette = DataProvider.getRephraseColors())
                st.pyplot(fig2)
            DataProvider.addSpacelines(1)
            st.write(f"*Title:*")
            number = st.slider("Pick a number of examples. ", 0, value=15, max_value=data.shape[0])
            st.dataframe(data[['rephrased_node_id','Rephrase_type','input', 'output']].iloc[:number].set_index("rephrased_node_id"))
            st.write("Number of examples: ",number,' .')
        else:
            st.write("Select Corpora...")

class DataStatsAnalyzer:
    def __init__(self, dataDic: dict[str: pd.DataFrame()]) -> None:
        st.subheader(f" Corpora stats: ")

        corporaColumnsDic = {}

        for key in dataDic:
            data_stats = dataDic[key].groupby(['Rephrase_type']).size().reset_index(name = 'Appearences')
            st.write("Corpora: \""+key+"\" Rephrase types & freq"+": ",data_stats)

            corporaColumnsDic[key] = {}
            for col in dataDic[key].columns:
                corporaColumnsDic[key][col] = True

        uncoherentColumnsDic = {}
        for key in corporaColumnsDic:
            for column in corporaColumnsDic[key]:
                for key1 in corporaColumnsDic:
                    if column not in corporaColumnsDic[key1]:
                        if column in uncoherentColumnsDic:
                            uncoherentColumnsDic[column].append(key1)
                        else:
                            uncoherentColumnsDic[column] = [key1]
        st.write("************************************************")
        st.write("Uncoherent columns: ")
        for col in uncoherentColumnsDic:
            st.write("Column: \""+col+"\" not in corpora: "+",".join(uncoherentColumnsDic[col]))

class Sentiment:
    def __SentimentAndRephrase(self, data: pd.DataFrame(), unit: str, scale: str, sentiment_type):
        def addTraceNumber(numerical_df: pd.DataFrame()):
            for i, j in DataProvider.getSentimentColors().items():
                single_sent = numerical_df[(numerical_df[sentiment_type] == i)]
                fig1.add_trace(go.Bar(x=single_sent["Rephrase_type"],
                                    y=single_sent["Number"],
                                    name=i,
                                    marker_color=j,
                                    hovertemplate="Rephrase: %{x} <br> Sentiment: %{y}", ))
        def addTracePercentage(percentage_df: pd.DataFrame()):
             for i, j in DataProvider.getSentimentColors().items():
                single_sent = percentage_df[(percentage_df[sentiment_type]== i)]
                fig1.add_trace(go.Bar(x=single_sent["Rephrase_type"],
                                    y=single_sent["Percentage"],
                                    name=i, marker_color=j,
                                    hovertemplate="Rephrase: %{x} <br> Sentiment: %{y}%",
                                    ))
        rephrase_order = CategoricalDtype(
                DataProvider.getRephraseDimentions(), 
                ordered=True
        )   
        scale_desc = ""
        if scale == "log":
            scale_desc = "Sentiment count (log scale)"
        elif scale == "linear":
            scale_desc = "Sentiment count (linear scale)"
        if unit == "number":
            sent_data = data.groupby(["Rephrase_type",sentiment_type])["input"].count().reset_index(name="Number")
            sent_data['Rephrase_type'] = sent_data['Rephrase_type'].astype(rephrase_order)
            all_sent_data = data.groupby([sentiment_type]).size().reset_index(name="Number")
            lst = []
            for cell in range(len(all_sent_data)):
                lst.append("All")
            all_sent_data["Rephrase_type"] = lst
            fig1 = go.Figure()
            sent_data = pd.concat([all_sent_data,sent_data.sort_values('Rephrase_type')])
            addTraceNumber(sent_data)
            fig1.update_layout(barmode='group',
                            width=1100,
                            height=400,
                            title={
                                'text': "Sentiment distribution across different reprases",
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
            fig1.update_yaxes(type=scale, ticklabelstep=2)
            fig1.update_xaxes(title_text='Rephrases', showgrid=True, ticks="outside", tickson="boundaries")
            fig1.update_yaxes(title_text=scale_desc)
        elif unit == "percentage":
            sent_data = (100 * data.groupby(["Rephrase_type", sentiment_type])["input"].count() / data.groupby(["Rephrase_type"])[
                "input"].count()).reset_index(name="Percentage")
            all_sent_data = DataManipulator.getGruppedPercentages(data,data.shape[0],sentiment_type,"Percentage")
            lst = []
            for cell in range(len(all_sent_data)):
                lst.append("All")
            all_sent_data["Rephrase_type"] = lst
            sent_data['Percentage'] = sent_data['Percentage'].round().astype(int)
            sent_data['Rephrase_type'] = sent_data['Rephrase_type'].astype(rephrase_order)
            fig1 = go.Figure()
            sent_data = pd.concat([all_sent_data,sent_data.sort_values('Rephrase_type')])
            addTracePercentage(sent_data)
            fig1.update_layout(barmode='group',
                            width=1100,
                            height=400,
                            title={
                                'text': "Sentiment distribution % across different rephrases",
                                'y': 0.9,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
            fig1.update_yaxes(type=scale, ticklabelstep=2)
            fig1.update_xaxes(title_text='Rephrases', showgrid=True, ticks="outside", tickson="boundaries")
            fig1.update_yaxes(title_text=scale_desc)
        return fig1
    
    def __init__(self, data: pd):
        st.subheader(f"Sentiment distribution across Rephrase types.")
        DataProvider.addSpacelines(1)
        if len(data) > 0:
            col_radio1, col_radio2, col_radio3 = st.columns(3)
            with col_radio1:
                    unit = st.radio("Choose the unit of y-axis",
                                    ("percentage",
                                    "number"),
                                    key="across rephrase")
            with col_radio2:
                scale = st.radio("Choose scale type: ", ("log","linear"))
            with col_radio3:
                sentiment_type = st.radio("Choose data source: ",("input_sentiment","output_sentiment"))
            f1 = self.__SentimentAndRephrase(data, unit, scale, sentiment_type)
            st.plotly_chart(f1)
        else:
            st.warning("You have to select data for analysis.")

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
        dyn_rephrase_options = st.multiselect("Choose dynamic ethos rephrase types: ", 
                                    DataProvider.getDynRephDimentions(), 
                                    DataProvider.getDynRephDimentions()[:],
                                    key = "multi_sel"+str(self.__keyCtr))
        self.__keyCtr += 1
        data_WS = data.loc[data['dyn_ethosWS'].isin(dyn_rephrase_options)]
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

    def __init__(self, data: pd.DataFrame(), analysisType: str, unit: str) -> None:
        if len(data) > 0:
            self.__keyCtr = 0
            self.__stop_words = DataProvider.getCustomStopWords() + list(STOPWORDS)
            if unit == "ADU-Based Analysis":
                if analysisType == 'Wordcloud':
                    st.subheader("Edit ADU data for worldcloud")
                    wl = self.__prepareWordCloud(data)
                    self.__Make_Word_Cloud(wl)
                elif analysisType == 'Cases':
                    self.__textAnalysis(data)
            elif unit == "Speaker-Based Analysis":
                sameSpeakerDf = data.loc[data['speaker_input'] == data['speaker_output']]
                diffSpeakerDf = data.loc[data['speaker_input'] != data['speaker_output']]
                if analysisType == 'Wordcloud':
                    st.subheader("Edit rephrase for worldcloud of same speaker: ")
                    wl = self.__prepareWordCloud(sameSpeakerDf)
                    self.__Make_Word_Cloud(wl)
                    st.subheader("Edit data for worldcloud of different speakers: ")
                    wl2 = self.__prepareWordCloud(diffSpeakerDf)
                    self.__Make_Word_Cloud(wl2)
                elif analysisType == 'Cases':
                    st.subheader("Edit cases for single speaker rephrase: ")
                    self.__textAnalysis(sameSpeakerDf)
                    st.subheader("Edit cases for two speakers rephrase: ")
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

    def __init__(self, data: pd.DataFrame(), unit: str) -> None:
        st.subheader(f"**Distribution of ethos dynamics in rephrase:**")
        DataProvider.addSpacelines(1)
        if len(data) > 0:
            if unit == "ADU-Based Analysis":
                col_radio1, = st.columns(1)
                with col_radio1:
                    display_unit = st.radio("Choose display type: ",
                        ("percentage",
                        "number"),
                        key="Rephrase_Distribution_Piechart")
                f1 = self.__drawDistribution(data, display_unit, "dyn_ethos")
                st.subheader("General ADU based plot")
                st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                st.subheader("Detailed ADU based plot")
                f2 = self.__drawDistribution(data, display_unit, "dyn_ethosWS")
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
                f1 = self.__drawDistribution(sameSpeakerDf, display_unit, "dyn_ethos")
                st.subheader("General single speaker rephrase analysis: ")
                st.plotly_chart(f1, config=DataProvider.getSaveConfig())
                st.subheader("Detailed single speaker rephrase analysis:")
                f2 = self.__drawDistribution(sameSpeakerDf, display_unit, "dyn_ethosWS")
                st.plotly_chart(f2, config=DataProvider.getSaveConfig())
                f3 = self.__drawDistribution(diffSpeakerDf, display_unit, "dyn_ethos")
                st.subheader("General dialog rephrase analysis: ")
                st.plotly_chart(f3, config=DataProvider.getSaveConfig())
                st.subheader("Detailed dialog rephrase analysis:")
                f4 = self.__drawDistribution(diffSpeakerDf, display_unit, "dyn_ethosWS")
                st.plotly_chart(f4, config=DataProvider.getSaveConfig())
        else:
            st.warning("You have to select data for analysis.")