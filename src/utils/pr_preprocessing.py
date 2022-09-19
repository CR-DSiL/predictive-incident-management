import re
import nltk

def data_preprocessing(description):
    """
    This function takes full description as input, converts it to short decription and cleans its
    """
    # create a short decrition from full decription
    short_description=extract_short_description(description)

    #remove persaonl information from short description
    short_description_pii=remove_personal_info(short_description)

    #clean the decription
    clean_descriprion=text_preprocessing(short_description_pii)

    return short_description,clean_descriprion



################################# All required Helper function ################################################################

# 1. Extracting the content in identified pattern

## Return function to extract the content after the keyword

keywordList1 = ["Subject:",
"Issue user reported :",
"\nIssue:",
"Error :",
"Issue Description:",
"Actual Issue :",
"\nProblem :",
"Problem:",            
"Issue Description:",
"Incident Notes :",
"\nSummary:",
"Summary of the issue:",
"Customer's Summary:",
"customer summary :",
"p -",
"\nP:",
"\n\n\np--",
"Important =-\n\n",
"Remote \n\n",
"Remote  \n\n",
"Alert :",
"MB Notification:-",
"\n\n\nSummary:","\n\nP: P:"]

def pattern_extraction(text,key_word):
    sen = text.split(key_word)[1]
    content = sen.split("\n" )[0]
    return content



# 2. Return to extracted the sentances without pattern  

keywordList2 = ["\nTicket: ",
           "\nAffected User Phone:","RCA -","Log Analytics","Azure Storage","Connection Monitor","  Azure AD -","ExpressRoute","  Azure AD or Azure AD B2C"]
#"Azure AD","RCA -","  Log Analytics/Azure Sentinel ","  Log Analytics","  Azure Storage","Connection Monitor","important information"

def without_pattern_extraction(text,key_word):
    sen = text.split(key_word)[1]
    content = sen.split("\n" )[1]

    return content

# 3. Extracting the first line sentences which address the inicdent issues
keywordList3 = ["\nUser Name: ","\nStatus:"]

def first_sen_extraction(text,key_word):
    sen = text.split(key_word)[0]
    content = sen.split("\n" )[0]
    return content

keywordList4=['Short Description:']
def short_description_pattern(text,key_word):
    text=text.split('\n')[0]
    text=re.sub('Short Description:','',text)
    return text    

### Stored all keywords in master keyword list
master_keyword_list=["Subject:", 
"Issue user reported :",
"\nIssue:",
"Error :",
"Issue Description:",  
"Actual Issue :",
"Problem :",
"Problem:",
"Issue Description:",
"Incident Notes :",
"\nSummary:",
"Summary of the issue:",
"Customer's Summary:",
'Short Description:',
"p -",
"\nP:",
"\n\n\np--", 
"Important =-\n\n",
"Remote \n\n",
"Remote  \n\n",                                    
"Alert :",
"\nTicket: ",
"nAffected User Phone:",
"customer summary :",
"\nUser Name: ",
"\nStatus::" ,
"MB Notification:-",
"\n\n\nSummary:","\n\nP: P:",
 "  Azure AD -","RCA -",
 "Log Analytics/Azure Sentinel ",
"Log Analytics",
"Azure Storage","  Azure AD or Azure AD B2C","ExpressRoute"]

# return a function to extract the keyword
def to_extract_keywords(text):
    for keyword in master_keyword_list:
        if keyword in text:
            return keyword

## return a function to extract the short desciption

def extract_short_description(text):
    
    # to extract the keywords
    key_word=to_extract_keywords(text)
    
    #  extact incident cause with defined pattern
    if key_word in keywordList1:
        return pattern_extraction(text,key_word)

    
    # extract incident cause without any defined pattern 
    elif key_word in keywordList2:
        return without_pattern_extraction(text,key_word)   
    
    # extract incident cause in first sentences
    elif key_word in keywordList3:
        return first_sen_extraction(text,key_word)  
    
    # extract incident cause in short description pattern
    elif key_word in keywordList4:
        return short_description_pattern(text,key_word)  
    
    else:
        return text

#################################################################################
##  To remove the personal data on short description

## function remove the personal data from the text

def remove_personal_info(text):
    
    # remove the warning msg 
    text=text.replace("This message contains information which is privileged and confidential and is solely for the use of the intended recipient. If you are not the intended recipient, be aware that any review, disclosure, copying, distribution, or use of the contents of this message is strictly prohibited. If you have received this in error, please destroy it immediately and notify us at ",' ')

    # remove the email id
    text  =re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"," ",str(text))
    
    # remove the contact num
    text=re.sub(r'((\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))',' ',text)
    text=re.sub(r'\d{10}|\d{11}|\d{3}-d{3}-d{4}', '', text)

    # remove the  employee Id
    text=re.sub(r'\d{4}|\d{5}|\d{6}\d{3}', '', text)

    return text

## To clean the short description
# ## to clean the data

def text_preprocessing(text):
    
    ## will replace the html characters with " "
    text =re.sub('<.*?>', ' ', text)
    
    #to remove the timestamp from description
    text=re.sub(r'\d{2}[-/]\d{2}[-/]\d{4} (2[0-3]|[01][0-9]|[0-9]):([0-5][0-9]|[0-9]):([0-5][0-9]|[0-9])',' ',text)
    
    ## remove the dash line and other characters
    text = re.sub('[^a-zA-Z0-9\.]',' ',text)   
    
    #will replace newline with space
    text = re.sub("\n"," ",text)
    
    #will convert to lower case
    text = text.lower()
    
    # will split and join the words
    text=' '.join(text.split())
    
    return text   

    
stopwords = nltk.corpus.stopwords.words('english')
new_words=('id','name', 'customer','user', 'email','remote','phone','morning','thank','hello', 'team','good', 'afternoon','hi','affected' ,'employee','agent','office','contact ','number','external',' message ','think', 'Click ')
for i in new_words:
    stopwords.append(i)
    #return stopwords