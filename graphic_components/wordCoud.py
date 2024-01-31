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
from typing import Tuple, List
from wordcloud import WordCloud, STOPWORDS
from nltk.util import ngrams
from nltk import FreqDist

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator