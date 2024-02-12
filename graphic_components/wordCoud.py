import streamlit as st
import sys
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, List
from wordcloud import WordCloud

from graphic_components.superComponent import SuperTextComponent
sys.path.insert(0,"..")

class WordCloudOfRephrase(SuperTextComponent):

    def __Make_Word_Cloud(self, lexicon, data: pd.DataFrame()) -> None:

        wordcloudTab, tableTab = st.tabs([":cloud: Wordcloud",":black_square_button: Cases"])
        with wordcloudTab:
            wordcloud = WordCloud(background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                                normalize_plurals=False).generate(" ".join(lexicon))
            fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
            ax.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig=fig)

        with tableTab:
            text = ""
            for inOut in self.cf['inOutLst']:
                text += " ".join(map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")))
            if text != "":
                wordLst = sorted(WordCloud().process_text(text).items(), key=lambda x:x[1], reverse=True)
                number = st.slider("Pick top n unigrams: ", 1, value=10, max_value=len(wordLst))
                index = []
                for i in range(1,number+1):
                    index.append(i)
                unigramsDf = pd.DataFrame(wordLst[:number],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
                unigramsDf.columns.name = unigramsDf.index.name
                st.dataframe(unigramsDf, width=800, height=40*number)

    def __prepareWordCloud(self, data: pd.DataFrame()) -> list():
        joined_set = set()
        for inOut in self.cf['inOutLst']: 
            emo_set = set(",".join(data[inOut].dropna().to_numpy(na_value="")).split(","))
            joined_set = joined_set | emo_set
        return list(joined_set)
    
    def dataDisplay(self, data: pd.DataFrame(), t: str) -> None:
        if len(data) > 0 and len(self.cf['inOutLst']) > 0:
            st.subheader(self.cf['generalConfig']["Wordcloud_display"]+" "+self.cf['ADU_or_Speaker']+" "+t)
            word_list = self.__prepareWordCloud(data)
            self.__Make_Word_Cloud(word_list, data)
        else:
            st.warning("You have to provide corpora for text analysis.")