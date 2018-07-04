"""File containing function utilised by the app"""
import json

import requests as req

import pybot.config as conf

import re

#Fonction de test à supprimer
def make_text(question):
    """Fonction pour test"""
    return 'Vous avez saisi : ' + question

def parser(question):
    """Function used to parse the question of the user
    Remove the word containing in the stopword base to keep
    only key words"""
    #Variable use to remove all punctuation symbols
    punctuation = ['.',',','!',':','\'',':','&',';','-','?']
    #Variable that contains the final keywords
    list_keywords = []
    for char in question:
        if char in punctuation:
            question = question.replace(char,' ')
    list_word = question.split()
    with open('pybot/stopwords.json', 'r') as file:
        stopwords = json.load(file)
        for word in list_word:
            if word.lower() not in stopwords:
                list_keywords.append(word)
    key_words = " "
    return key_words.join(list_keywords)


def parser_for_wiki(address):
    """Function use to parse the address recieve from google to try a request on the road name"""
    regex = '[0-9]+'
    result = ''
    address_without_number = re.split(regex, address)
    address_without_number = result.join(address_without_number).split(', ')
    address_without_number = address_without_number
    if 'France' in address_without_number:
        result = result.join(address_without_number).split("France")[0]
    else:
        result = result.join(address_without_number)
    return result

def parser_for_name_of_road(address):
    """Function to get only the name of the road in an address"""
    list_keywords = []
    list_word = address.split()
    with open('pybot/stopwords_address.json', 'r') as file:
        stopwords = json.load(file)
        for word in list_word:
            if word.lower() not in stopwords:
                list_keywords.append(word)
    key_words = " "
    result =  key_words.join(list_keywords)
    result = parser(result)
    return result

def request_api(url):
    """Request the selected url and return data from the api as json"""
    data = req.get(url)
    return data.json()

def get_data_from_google_maps(keywords):
    """Do request to the google maps API"""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(\
        keywords, conf.GOOGLE_MAPS_KEY)
    data = request_api(url)
    try:
        result_lat = data["results"][0]["geometry"]["location"]["lat"]
        result_long = data["results"][0]["geometry"]["location"]["lng"]
        try:
            address = data["results"][0]["formatted_address"]
            return result_lat, result_long, address
        except KeyError:
            return result_lat, result_long, ''
    except IndexError:
        pass

def get_title_from_wiki(keywords):
    """Request media wiki to get the title of the first article link to the keywords"""
    #Return all the articles link to the keywords
    url = 'https://fr.wikipedia.org/w/api.php?action=opensearch&search={}'.format(keywords)  
    data = request_api(url)
    #Try to get and return the firt article
    try:
        article_title = data[1][0]
    #Return an error message if there is no result
    except IndexError:
        msg_error = "Euh... Non en fait je ne connais rien d'intéressant à ce sujet."
        return msg_error
    return article_title


def get_data_from_wiki(keywords):
    """Request wikimedia to get the firt sentences of a wikipedia article"""
    article_title = get_title_from_wiki(keywords)
    #Return the first sentence of a wikipedia article
    url = 'https://fr.wikipedia.org/w/api.php?action=query&titles={}&prop=extracts&exsentences=1 \
        &format=json&explaintext'.format(article_title)
    data = request_api(url)
    #Loop on only one element (page_id), but usefull because we don't know the id of the page
    for page_id in data['query']['pages']:
        result = data['query']['pages'][page_id]['extract']
    return result