import re
import string
import pickle
import os
import yaml
#lemmatization for text
import spacy
nlp = spacy.load('en_core_web_sm')



""" This function pefroms the pre-procesing for env incident types"""

def env_preprocessing_for_incident_type(short_description):
    text=short_description
   # remove the warning msg
    text=text.replace("This message contains information which is privileged and confidential and is solely for the use of the intended recipient. If you are not the intended recipient, be aware that any review, disclosure, copying, distribution, or use of the contents of this message is strictly prohibited. If you have received this in error, please destroy it immediately and notify us at ",' ')

   # remove the email id
    text  =re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"," ",str(text))
    
    # remove the contact num
    text=re.sub(r'((\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))',' ',text)
    text=re.sub(r'\d{10}|\d{11}|\d{3}-d{3}-d{4}|/d{5}', '', text)

   # remove the  employee Id
    text=re.sub(r'\d{4}|\d{5}|\d{6}\d{3}', '', text)
    
    ## will replace the html characters with " "
    text =re.sub('<.*?>', ' ', text)
  
    #remove the punctuations
    text = text.translate(str.maketrans(' ',' ',string.punctuation))
    
    ## remove the dash line and other characters
    text = re.sub('[^a-zA-Z0-9\.]',' ',text)  
    
    #to remove the timestamp from description
    text=re.sub(r'\d{2}[-/]\d{2}[-/]\d{4} (2[0-3]|[01][0-9]|[0-9]):([0-5][0-9]|[0-9]):([0-5][0-9]|[0-9])',' ',text)
    
    #will replace newline with space
    text = re.sub("\n"," ",text)
    
    #remove only numbers but not digits from aplhanumeric
    text = re.sub(" \d+| \d+ ", " ", text)
    
    #will convert to lower case
    text = text.lower()
    
    # will split and join the words
    text=' '.join(text.split())
    
    return text


def env_preprocessing_for_subgroups(short_description):   
    text=short_description 
    # remove the warning msg
    text=text.replace("This message contains information which is privileged and confidential and is solely for the use of the intended recipient. If you are not the intended recipient, be aware that any review, disclosure, copying, distribution, or use of the contents of this message is strictly prohibited. If you have received this in error, please destroy it immediately and notify us at ",' ')



   # remove the email id
    text  =re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"," ",str(text))
    
    # remove the contact num
    text=re.sub(r'((\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))',' ',text)
    text=re.sub(r'\d{10}|\d{11}|\d{3}-d{3}-d{4}|/d{5}', '', text)



   # remove the  employee Id
    text=re.sub(r'\d{4}|\d{5}|\d{6}\d{3}', '', text)
    
    ## will replace the html characters with " "
    text =re.sub('<.*?>', ' ', text)
    
    ## remove the dash line and other characters
    text = re.sub('[^a-zA-Z0-9\.]',' ',text)  
    
    #to remove the timestamp from description
    text=re.sub(r'\d{2}[-/]\d{2}[-/]\d{4} (2[0-3]|[01][0-9]|[0-9]):([0-5][0-9]|[0-9]):([0-5][0-9]|[0-9])',' ',text)
    
    #will replace newline with space
    text = re.sub("\n"," ",text)
    
    #to remove the numbers from the text
    text=re.sub(r'[0-9]',' ',text)
    
    #will convert to lower case
    text = text.lower()
    
    # will split and join the words
    text=' '.join(text.split())
    ### applying the lemmatization
    text   = [' '.join([x.lemma_ for x in nlp(text)])]
    return text    