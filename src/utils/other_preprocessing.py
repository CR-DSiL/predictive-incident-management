'''This file is used for additional pre-processsing'''
import re
from utils.pr_preprocessing import *
import pickle
import os
import yaml

#lemmatization for text
import spacy
nlp = spacy.load('en_core_web_sm')


def other_subgroup_preprocessing(clean_short_description):
    text=clean_short_description
# #to remove the numbers from the text
    text=re.sub(r'[0-9]',' ',text)
    ### applying the lemmatization
    text   = [' '.join([x.lemma_ for x in nlp(text)])]
    text =''.join(text)
    return text    

#---------------------------------------------------------    