import streamlit as st
import pandas as pd
from typing import Tuple

import sys
sys.path.insert(0,"..")
from data_display.display_single_corpus import WordCloudOfEmotions
from data_display.display_single_corpus import Piechart
from config.config_data_colector import DataProvider
from submenus.tweaker import st_tweaker

class SingleCorpusMenu:
    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="0_", anType: str="DynRephAn for Sentiment") -> None:
        tmp = DataProvider.getDynRephrESconfig()
        # ADU or Speaker
        self.__units = ""
        # Speaker type, default is ""
        self.__speaker = ""
        self.__anCfg = tmp[anType]
        self.__dataDic = dataDic
        self.__ticker = {}
        for key in dataDic:
            self.__ticker[key] = False
        self.__prefix = prefix
        self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df
        print("Reloaded!!!")

    def cleanSelections(self):
        for key in self.__dataDic:
            st.session_state[self.__prefix + key] = False
        st.session_state[self.__prefix + "US2016reddit"] = False
        st.session_state[self.__prefix + "US2016tv"] = False
        self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df

    def __update_corpora_checkbox(self):
        dfLst = []
        for key in self.__dataDic:
            if st.session_state[self.__prefix + key]:
                dfLst.append(self.__dataDic[key])
        if len(dfLst) > 1:
            self.__rephrase_df = pd.concat(dfLst)          
        elif len(dfLst) == 1:
            self.__rephrase_df = dfLst[0]
        else:
            self.__rephrase_df = pd.DataFrame()
        self.__rephrase_old = self.__rephrase_df

    def __update_block(self, name: str):
        for key in self.__dataDic:
            if key.find(name) != -1:
                print("Block:", self.__prefix + name," Updates: ",self.__prefix + key)
                st.session_state[self.__prefix + key] = st.session_state[self.__prefix + name]
                self.__update_corpora_checkbox()

    def __corporaPickerChckBox(self):
        tv = False
        reddit = False
        for ctr, key in enumerate(self.__dataDic):
            if key.find("US2016reddit") != -1:
                if not reddit:
                    reddit = True
                    st.checkbox("US2016reddit", \
                        key = self.__prefix + "US2016reddit",
                        help = self.__prefix + "US2016reddit",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "US2016reddit"},
                        disabled=False
                    )           
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "Reddit" + str(ctr)
                )
            elif key.find("US2016tv") != -1:
                if not tv:
                    tv = True
                    st.checkbox("US2016tv", \
                        key = self.__prefix + "US2016tv",
                        help = self.__prefix + "US2016tv",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "US2016tv"},
                        disabled=False
                    )                     
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "US2016tv" + str(ctr) 
                )                
            else:
                st.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False
                )
        st.markdown("""
        <style>
        #Reddit0,#Reddit1,#Reddit2,#US2016tv3,#US2016tv4,#US2016tv5 {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
            

    def sidebar(self):
        with st.sidebar:
            st.subheader("Choose Corpora: ")           
            st.button("Clean selection",key=self.__prefix+"clear_corpo_button",on_click=self.cleanSelections)
            self.__corporaPickerChckBox()
            st.write("****************************")
            st.subheader("Analysis Units")
            units_choice = st.radio("", ("ADU-Based Analysis",
                                            "Speaker-Based Analysis"
                                            ), key=self.__prefix+"units")

            #if units == "ADU-Based Analysis":
            st.write("****************************")
            st.subheader("Analitics module")
            module_choice = st.radio("An. Module", \
                                        ("Distribution","Wordcloud","Cases"), \
                                        key=self.__prefix+"post", label_visibility="hidden"
                                    )

        if module_choice == "Cases":
            WordCloudOfEmotions(self.__rephrase_df,analysisType="Cases",unit=units_choice, configDic=self.__anCfg)
        elif module_choice == "Wordcloud":
            WordCloudOfEmotions(self.__rephrase_df,analysisType="Wordcloud",unit=units_choice, configDic=self.__anCfg)
        elif module_choice == "Distribution":
            Piechart(self.__rephrase_df,unit=units_choice, configDic=self.__anCfg)
        else:
            raise NotImplementedError("Unsupported option of Analytical module in single_corpus.py .")
        
    #Returns criteria to which data is selected
    def getCriteria(self) -> str:
        if len(self.__dataDic) > 0:
            newLst = []
            if self.__units == "ADU-Based Analysis":
                newLst = ['ADU based']
            elif self.__units == "Speaker-Based Analysis":
                newLst = ['Speaker '+self.__speaker]
            ctr = 1
            for key in self.__dataDic:
                if st.session_state[self.__prefix + key]:
                    ctr += 1
                    newLst.append(key)
                    if ctr == 2:
                        newLst.append("\n")
                        ctr = 0
            self.criteria = "|".join(newLst)
        else:
            self.criteria = ""
        return self.criteria

    def tab(self, units):
        self.__units = units
        st.subheader("Choose Corpora: ")
        self.__corporaPickerChckBox()
        if len(self.__rephrase_old) > 0:
            if self.__units == "ADU-Based Analysis":
                st.write("ADU units selected.")
                self.__rephrase_df = self.__rephrase_old
            elif self.__units == "Speaker-Based Analysis":
                speaker = st.radio("Choose Speaker Unit Type: ",
                    ("SS rephrase",
                    "SO rephrase"),
                    key=self.__prefix+"Rephrase_Cmp_Speaker")
                if speaker == "SS rephrase":
                    self.__rephrase_df = self.__rephrase_old
                    self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] == self.__rephrase_df['speaker_output']]
                elif speaker == "SO rephrase":
                    self.__rephrase_df = self.__rephrase_old
                    self.__rephrase_df = self.__rephrase_df.loc[self.__rephrase_df['speaker_input'] != self.__rephrase_df['speaker_output']]
                self.__speaker = speaker
        else:
            st.write("Choose corpora above.")

    #Returns data for diagrams
    def getDF(self) -> pd.DataFrame():
        return self.__rephrase_df