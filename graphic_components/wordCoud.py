import streamlit as st
import sys
import pandas as pd
import matplotlib.pyplot as plt
from typing import Any, Tuple, List
from wordcloud import WordCloud

from graphic_components.superComponent import SuperTextComponent
sys.path.insert(0,"..")

class WordCloudOfRephrase(SuperTextComponent):

    def getChartObj(self, data: Any, t: str) -> Any:
        joined_set = set()
        for inOut in self._cf['inOutLst']: 
            emo_set = set(",".join(data[inOut].dropna().to_numpy(na_value="")).split(","))
            joined_set = joined_set | emo_set
        lexicon = list(joined_set)
        wordcloud = WordCloud(background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                            normalize_plurals=False).generate(" ".join(lexicon))
        fig, ax = plt.subplots(figsize=(10, 10), facecolor=None)
        ax.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        return fig
    
    def getTextObj(self, data: Any, t: str) -> Any:
        text = ""
        for inOut in self._cf['inOutLst']:
            text += " ".join(map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")))
        if text != "":
            wordLst = sorted(WordCloud().process_text(text).items(), key=lambda x:x[1], reverse=True)
            if not self._cf['imediatePlot']:
                self._cf['textInstances'] = st.slider("Pick top n unigrams: ", 1, value=10, max_value=len(wordLst))
            index = []
            for i in range(1,self._cf['textInstances']+1):
                index.append(i)
            unigramsDf = pd.DataFrame(wordLst[:self._cf['textInstances']],columns = ['Top phrase', 'Frequency'],index=pd.Index(index, name='Ranking'))
            unigramsDf.columns.name = unigramsDf.index.name
            unigramsDf.index += 1
            return unigramsDf
        else:
            return pd.DataFrame()
    
    def dataDisplay(self, data: pd.DataFrame(), t: str) -> None:
        if len(data) > 0 and len(self._cf['inOutLst']) > 0:
            st.subheader(self._cf['generalConfig']["Wordcloud_display"]+" "+self._cf['ADU_or_Speaker']+" "+t)

            wordcloudTab, tableTab = st.tabs([":cloud: Wordcloud",":black_square_button: Cases"])
            with wordcloudTab:
                chart = self.getChartObj(data=data, t=t)
                st.pyplot(fig=chart)
            with tableTab:
                df = self.getTextObj(data, t=t)
                st.dataframe(df, width=800, height=40*self._cf['textInstances'])
        else:
            st.warning("You have to provide corpora for text analysis.")