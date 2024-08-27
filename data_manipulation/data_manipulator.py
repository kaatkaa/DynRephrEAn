import pandas as pd
import numpy as np
import streamlit as st
from nltk.corpus import wordnet as wn
import subprocess
import ast
import sys
import os
from typing import Dict, Set, List, Tuple
import spacy

nlp = spacy.load("en_core_web_sm")
sys.path.insert(0,"..")

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
        wn.langs()
        adv_tags = dict()
        spacyDataLst = []
        synDic = dict()
        ctr = 0
        clusterSynCtr = 0
        def notInCluster(tagPos: str, token: str, syn: set) -> bool:
            flag = True
            # setOfMeanings = set()
            if tagPos in synDic:
                for clusterName in synDic[tagPos].keys():
                    if not isinstance(synDic[tagPos][clusterName], int) and token in synDic[tagPos][clusterName]['synSet']:
                        synDic[tagPos][clusterName]['ctr'] += 1
                        flag = False
                #         setOfMeanings.update(synDic[tagPos][clusterName]['synSet'])
                # if len(syn - setOfMeanings) >= 2:
                #     flag = False
            return flag
        for column in colLst:
            for text_line in d[column].values.tolist():
                spacyDataLst.append(nlp(u'{s}'.format(s=text_line)))
        for doc in spacyDataLst:
            for tag in doc:
                if tag.pos_ in PoS_set:
                    tmpDic = {}
                    tmpDic['text'] = tag.text
                    tmpDic['lemma_'] = tag.lemma_
                    tmpDic['SynonimClasses'] = wn.synonyms(tag.lemma_)
                    tmpDic['pos_'] = tag.pos_
                    tmpDic['tag_'] = tag.tag_
                    tmpDic['dep_'] = tag.dep_
                    tmpDic['shape_'] = tag.shape_
                    tmpDic['morph'] = str(tag.morph)
                    tmpDic['ent_type_'] = tag.ent_type_
                    tmpDic['ent_iob_'] = tag.ent_iob_
                    if spacyTagType not in tmpDic:
                        st.error("Wrong tag name provided to 'getSpacyPoSTagsFre' in data_manipulator.py .")
                    ctr += 1
                    tags[tag.pos_] = tags.get(tag.pos_, 0) + 1
                    if spacyTagType == "SynonimClasses":
                        for synonims in tmpDic['SynonimClasses']:
                            if tag.pos_ in synDic:
                                synDic[tag.pos_]['ctr'] += 1
                                notInClusterFlag = notInCluster(tagPos=tag.pos_, token = tmpDic['text'], syn=set(synonims))
                                if notInClusterFlag:
                                    clusterSynCtr += 1
                                    synDic[tag.pos_]["syn_"+tmpDic['text']] = {}
                                    synDic[tag.pos_]["syn_"+tmpDic['text']]['ctr'] = 1
                                    synDic[tag.pos_]["syn_"+tmpDic['text']]['synSet'] = set(synonims)
                                    synDic[tag.pos_]["syn_"+tmpDic['text']]['synSet'].add(tmpDic['text'])                                 
                            else:
                                clusterSynCtr += 1
                                synDic[tag.pos_] = {}
                                synDic[tag.pos_]['ctr'] = 1
                                synDic[tag.pos_]["syn_"+tmpDic['text']] = {}
                                synDic[tag.pos_]["syn_"+tmpDic['text']]['ctr'] = 1
                                synDic[tag.pos_]["syn_"+tmpDic['text']]['synSet'] = set(synonims)
                                synDic[tag.pos_]["syn_"+tmpDic['text']]['synSet'].add(tmpDic['text'])
                    else:
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
        def sortFunc(dict) -> int:
            if dict[0] == 'ctr':
                return 999999999
            else:
                return dict[1]['ctr']
        for key in synDic.keys():
            synDic[key] = {k: v for k, v in sorted(synDic[key].items(), key=lambda item: sortFunc(item), reverse=True)}
        ##
        if percentage:
            for key in adv_tags.keys():
                for k in adv_tags[key].keys():
                    adv_tags[key][k] /= tags[key]
                    adv_tags[key][k] *= 100
            for key in synDic.keys():
                for k in synDic[key].keys():
                    if k != 'ctr':
                        synDic[key][k]['ctr'] /= synDic[key]['ctr']
                        synDic[key][k]['ctr'] *= 100
            for tag in tags.keys():
                tags[tag] /=  ctr
                tags[tag] *= 100
                tags[tag] = int(round(tags[tag]))
        return (tags, adv_tags, synDic, )