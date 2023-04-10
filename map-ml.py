# Using machine learning NER appraoch to find place names in James Joyce Ulysses

import spacy
from spacy.lang.en import English #English
from spacy.pipeline import EntityRuler #create rules for finding entities


import json

from spacy import displacy
import string

from list_countr import list_countr

# test original spacy model
"""with open('Ulysses.txt','r') as f:
    text = f.read()
    chapters= text.split(f'CHAPTER ')[1:]
    #print(chapters[3])
    #print(len(chapters))

    nlp = spacy.load("en_core_web_lg")
    doc = nlp(chapters[0])

    # gets the entity name, type and sentence in the chapter.
    for ent in doc.ents:
        if (ent.label_ == 'GPE'):
            print(ent.text,ent.label_)
            print(ent.sent)

        if (ent.label_ == 'LOC'):
            print(ent.text,ent.label_)
            print(ent.sent)

        if (ent.label_ == 'FAC'):
            print(ent.text,ent.label_)
            print(ent.sent) """


def load_data(file): #load json data
    with open(file,'r') as g:
        places = json.load(g) #get GPE for training data. This is a gazetteer
        return places

def save_data(file,data):
    with open(file,'w') as f:
        json.dump(data,f,indent=4)

def load_better_places(file): #create training set of place names
    place_names = [] #list of atomic places and compound places to develop a pattern for the machine learning model. To represent all possible ways the place names may appear in the text.
    places = load_data(file) # e.g. training data included because elements mostly appear once. Original method to train based on context failed with less accuracy possibly because of unique Ulysses writing style across chapters.
    for place in places:
        place_names.append(place)
        row_places = place.split()
        if len(row_places) == 3:
            place_names.append(row_places[0] + ' ' + row_places[1])
            place_names.append(row_places[1] + ' ' + row_places[2])
        if len(row_places) == 4:
            place_names.append(row_places[0] + ' ' + row_places[1])
            place_names.append(row_places[1] + ' ' + row_places[2])
            place_names.append(row_places[2] + ' ' + row_places[3]) #Get all possible ways a place name can show in the text
        for row_place in row_places:
            #print(row_place)
            place_names.append(row_place)

    #print(len(place_names))
    # eliminate duplicates in list
    place_names = list(set(place_names))
    if 'of' in place_names: # Remove prepositions in training data
        place_names.remove('of')
    if 'The' in place_names:
        place_names.remove('The')
    place_names.sort()
    return place_names

def create_training_data(file,type):
    places = load_better_places(file)
    patterns = []
    for place in places:
        pattern = {
        'label': type,
        'pattern': place #create (place name) pattern for spacy to learn for its entity ruler
        }
        patterns.append(pattern) # create a list of patterns

    return patterns #list of dictionaries of patterns for place names

def generate_rules(patterns): # make rules in spacy
    nlp = spacy.load("en_core_web_lg")
    ruler = nlp.add_pipe('entity_ruler') # rules based NER pipe
    ruler.add_patterns(patterns) # add patterns to spacy model
    nlp.to_disk('ul_ner') # save model

# generate model

patterns = create_training_data('uplaces.json','GPE') # A training set containing all possible place names
generate_rules(patterns) # create a spacy model that can accurately identify texts in Ulysses

def remove_badwords(text,sent): # Remove or modify bad place names. Used: test_model()
    #print(text)
    #print(sent)
    new_text = text
    if new_text == 'street': # modify 'street' to full street names
        list_sent = sent.split()
        #print(list_sent)
        list_sent = nopunc_list(list_sent)
        new_text = list_sent[list_sent.index(text) - 1] + ' ' + 'street'

    # modify to full road name
    list_sent = sent.split()
    list_sent = nopunc_list(list_sent)
    if 'road' in list_sent:
        #print(list_sent)
        #print(text)
        if list_sent[list_sent.index('road') - 1] == new_text:
            new_text = list_sent[list_sent.index('road') - 1] + ' ' + 'road'


    if new_text == 'avenue': # modify 'avenue' to full avenue names
        list_sent = sent.split()
        #print(list_sent)
        list_sent = nopunc_list(list_sent)
        new_text = list_sent[list_sent.index(text) - 1] + ' ' + 'avenue'

    if new_text.islower(): # return true if all characters in the string are uncapitalised (They are not place names)
        new_text = 'XD' # This is a string that will act as a flag to terminate the text from the final list

    if new_text == 'Sir': # remove 'Sir' from list
        new_text = 'XD' # This is a string that will act as a flag to terminate the text from the final list

    list_countries = ['Athens','Oxford','Ireland','Dublin','Belfast','Paris','England','London','Wales','Liverpool','Italy','Austria','Troy','Rome','Greece','Egypt','Europe','Jerusalem','Bethlehem','Barcelona','Manchester','France','York','Edom','America','Asia','Ireland','China','Mercury','Venus','Earth','Mars','Jupiter','Neptune','Saturn','Uranus','Pluto','Ohio','Israel','New York','Morocco','Africa','South Africa','India','Canada','Yorkshire'] + list_countr

    if new_text in list_countries: # Remove countries except Dublin from list
        new_text = 'XD' # This is a string that will act as a flag to terminate the text from the final list

    list_chars = ['Malachi','Haines','Mercurial Malachi','Carlisle','Alexandria','Drumont','Paddy Dignam','Dignam','Paddy','Bloom','Florry','Little','LYNCH','Heigho','Evening','Walk','Salt']

    if new_text in list_chars: # Remove characters from list
        new_text = 'XD' # This is a string that will act as a flag to terminate the text from the final list

    return new_text

def nopunc_list(my_list): # remove punctuations from list. Used: remove_badwords
    new_list = []
    for word in my_list:

        for character in word:
            #print(character)
            if character in string.punctuation+'—':

                word = word.replace(character,"")
        new_list.append(word)

    return new_list

def test_model(model,text): # load model and test on segments
    doc = nlp(text) #get entities that are place names from text
    results = []
    for ent in doc.ents:
        if (ent.label_ == 'GPE'):
            #print(ent.text,ent.label_)
            sent_string = str(ent.sent)
            ent_text = remove_badwords(ent.text, sent_string)
            if not ent_text == 'XD': # if 'XD' flag has not been raised, do not termiante
                results.append([ent_text, sent_string])


        if (ent.label_ == 'LOC'):
            sent_string = str(ent.sent)
            ent_text = remove_badwords(ent.text, sent_string)
            if not ent_text == 'XD': # if 'XD' flag has not been raised, do not termiante
                results.append([ent_text, sent_string])

        if (ent.label_ == 'FAC'):
            sent_string = str(ent.sent)
            ent_text = remove_badwords(ent.text, sent_string)
            if not ent_text == 'XD': # if 'XD' flag has not been raised, do not termiante
                results.append([ent_text, sent_string])

    return results

# test new trained spacy model

with open('Ulysses.txt','r') as f:
    nlp = spacy.load("ul_ner")
    ie_data = {} # temporarily placed inside
    text = f.read()
    chapters = text.split(f'CHAPTER ')[1:]
    #print(chapters[3])
    #print(len(chapters))

    for chapter in chapters:
        chapter_num, chapter_title = chapter.split("\n\n")[0:2] #get chapter number and title
        chapter_num = chapter_num.strip()
        segments = chapter.split("\n\n")[2:] #get paragraphs in chapter

        hits = []
        for segment in segments:
            segment = segment.strip()
            segment = segment.replace('\n',' ') # Remove line breaks to increase NLP accuracy
            results = test_model(nlp,segment) # list of entities in text
            for result in results:
                hits.append(result)
        ie_data[chapter_num] = hits

    print(ie_data)
    save_data('new_uplaces.json',ie_data) # list of place names in each chapter that accounts for different patterns that may exist


    # Spacy entity visualiser in browser
    # options = {"ents": ["GPE",'LOC','FAC']}
    # displacy.serve(doc, style="ent", options=options)

    # loads a spacy NER model and extracts the place names of the chapters
