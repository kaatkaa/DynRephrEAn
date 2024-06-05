import pandas as pd
import numpy as np
import streamlit as st
import ast
from typing import Dict, Set, List, Tuple
import spacy
nlp = spacy.load("en_core_web_sm")

class DataManipulator:

    @staticmethod
    def getGruppedPercentages(d: pd, denominator: int, groupBy: str="", col_name: str="Percentage"):
        d = d.groupby([groupBy]).size().reset_index(name = col_name)
        d[col_name] = d[col_name] / denominator
        d[col_name] = d[col_name] * 100
        d[col_name] = d[col_name].round().astype(int)
        return d
    
    @staticmethod
    def getGruppedData(d: pd, groupBy: str="", col_name: str="Number"):
        d = d.groupby([groupBy]).size().reset_index(name = col_name)
        return d
    
    @staticmethod
    def getSpacyPoSTagsFreq(d: pd, colLst: List[str], PoS_set: Set[str], spacyTagType: str, percentage: bool=False) -> Tuple[Dict[str,int], Dict[str, float or int]]:
        tags = dict()
        adv_tags = dict()
        spacyDataLst = []
        ctr = 0
        for column in colLst:
            for text_line in d[column].values.tolist():
                spacyDataLst.append(nlp(u'{s}'.format(s=text_line)))
        for doc in spacyDataLst:
            for tag in doc:
                if tag.pos_ in PoS_set:
                    tmpDic = {}
                    tmpDic['text'] = tag.text
                    tmpDic['lemma_'] = tag.lemma_
                    tmpDic['pos_'] = tag.pos_
                    tmpDic['tag_'] = tag.tag_
                    tmpDic['dep_'] = tag.dep_
                    tmpDic['shape_'] = tag.shape_
                    tmpDic['morph'] = tag.morph
                    tmpDic['ent_type_'] = tag.ent_type_
                    tmpDic['ent_iob_'] = tag.ent_iob_
                    if spacyTagType not in tmpDic:
                        st.error("Wrong tag name provided to 'getSpacyPoSTagsFre' in data_manipulator.py .")
                    ctr += 1
                    tags[tag.pos_] = tags.get(tag.pos_, 0) + 1
                    if tag.pos_ in adv_tags:
                        if tmpDic[spacyTagType] in adv_tags[tag.pos_]:
                            adv_tags[tag.pos_][tmpDic[spacyTagType]] += 1
                        else:
                            adv_tags[tag.pos_][tmpDic[spacyTagType]] = 1
                    else:
                        adv_tags[tag.pos_] = {}
                        adv_tags[tag.pos_][tmpDic[spacyTagType]] = 1
        # Descending sorting of dictonaries according to freqency
        tags = {k: v for k, v in sorted(tags.items(), key=lambda item: item[1], reverse=True)}
        for key in adv_tags.keys():
            adv_tags[key] = {k: v for k, v in sorted(adv_tags[key].items(), key=lambda item: item[1], reverse=True)}
        ##
        if percentage:
            for tag in tags.keys():
                tags[tag] /=  ctr
                tags[tag] *= 100
                tags[tag] = int(round(tags[tag]))
            for key in adv_tags.keys():
                for k in adv_tags[key].keys():
                    adv_tags[key][k] /= ctr
                    adv_tags[key][k] *= 100
        return (tags, adv_tags, )