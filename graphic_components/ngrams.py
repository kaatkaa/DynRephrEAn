import streamlit as st
import sys
import pandas as pd
import numpy as np
import re
from nltk.util import ngrams
from nltk import FreqDist
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from graphic_components.superComponent import SuperTextComponent

class Ngrams(SuperTextComponent):
    
    def dataDisplay(self, data: Any, t: str) -> None:
        lstOfInOut = []
        restLst = []
        if set(self._cf['inOutLst']) <= set(DataProvider.getInOutColLst()):
            lstOfInOut = DataProvider.getInOutColLst()
            restLst = DataProvider.getLocInOut()
        elif set(self._cf['inOutLst']) <= set(DataProvider.getLocInOut()):
            lstOfInOut = DataProvider.getLocInOut()
            restLst = DataProvider.getInOutColLst()
        else:
            st.warning("Wrong list inOut values in n-gram data display.")
        def backgroung_color(v):
            return f"background-color: {DataProvider.getRephraseAndEmptycolors()['Rephrase']};"
        wordLst = []
        if len(data) > 0:  
            for inOut in self._cf['inOutLst']:
                for token in map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")):
                    wordLst.extend(ngrams(token.split(" "), 1))
        if len(wordLst) > 0:
            wordLst = FreqDist(wordLst)
            number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst))
            ngramType = st.slider("Choose n-gram type: (1-4)",1,value=1, max_value=4)
            st.subheader("Pick phrase to analyse: ")
            NgramLst = []
            for inOut in self._cf['inOutLst']:
                for token in map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")):
                    NgramLst.extend(ngrams(token.split(" "), ngramType))
            NgramLst = FreqDist(NgramLst)
            common = NgramLst.most_common(number)
            w2 = [" ".join(item[0])+" : "+str(item[1]) for item in common if item[0] != ('',)]
            word = st.selectbox("Pick "+str(ngramType)+"-gram to analyse: ",w2,index=0,key='Dropdown_'+str(ngramType)+'-gramLst')
            regexpStr = re.sub(r"^(.*)\s:\s[0-9]+$", r"\1", word)
            regExpCode = r"\s"+regexpStr+r"\s|^"+regexpStr+r"\s|\s"+regexpStr+r"$|^"+regexpStr+r"$"
            st.subheader("Selected phrase is marked in text below between stars: \*\*"+regexpStr+"\*\*")
            if lstOfInOut[0] in self._cf['inOutLst'] and lstOfInOut[1] in self._cf['inOutLst']:
                filteredInputDF = data[data[lstOfInOut[0]].str.contains(regExpCode, case=False, regex=True)]
                filteredInputDF.reset_index(inplace=True)
                filterInOutDF = filteredInputDF[filteredInputDF[lstOfInOut[1]].str.contains(regExpCode, case=False, regex=True)]
                tmpDf = filterInOutDF[[*lstOfInOut,*restLst]]
                tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                tmpDf.index += 1
                st.table(tmpDf[[*lstOfInOut,*restLst]].style.applymap(backgroung_color,subset=lstOfInOut))
            elif lstOfInOut[0] in self._cf['inOutLst']:
                filteredInputDF = data[data[lstOfInOut[0]].str.contains(regExpCode, case=False, regex=True)]
                filteredInputDF.reset_index(inplace=True)
                tmpDf = filteredInputDF[[*lstOfInOut,*restLst]]
                tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                tmpDf.index += 1
                st.table(tmpDf.style.applymap(backgroung_color,
                    subset=lstOfInOut[0]))
            elif lstOfInOut[1] in self._cf['inOutLst']:
                filteredOutputDF = data[data[lstOfInOut[1]].str.contains(regExpCode, case=False, regex=True)]
                filteredOutputDF.reset_index(inplace=True)
                tmpDf = filteredOutputDF[[*lstOfInOut,*restLst]]
                tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                tmpDf.index += 1
                st.table(tmpDf.style.applymap(backgroung_color,
                    subset=lstOfInOut[1]))
            else:
                st.error("Wrong input-output options for dataframe")
        else:
            st.warning("Not enought data to display in text analysis.")