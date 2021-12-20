import spacy
from SnippetDetails import SnippetDetails
#import nltk import Tree
from spacy.pipeline.dep_parser import DEFAULT_PARSER_MODEL
from urllib.request import Request, urlopen
import requests

from bs4 import BeautifulSoup
from operator import attrgetter
#from googlesearch import search
from googlesearch.googlesearch import GoogleSearch

# progress bar
from tqdm import tqdm

# copying file
from shutil import copyfile

config = {
   "moves": None,
   "update_with_oracle_cut_size": 100,
   "learn_tokens": False,
   "min_action_freq": 30,
   "model": DEFAULT_PARSER_MODEL,
}

import json

# default weighting for google results
google_base_weight = 100
google_weight_scale = 5
max_search_count = 20

# element to search in the json file, change to whatever is needed
element_to_search = "abstract"

nlp = spacy.load("en_core_web_sm")
# add default dependency parsing with spacy
#nlp.add_pipe("parser", config=config)
# good sentence
google_one = "In computer science, a Btree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The Btree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "Btree is a data structure that store data in its node in sorted order"

def ScoreSentence(snippet, word_one, word_two, base_score = 0):
        snippet_details = SnippetDetails(snippet)
        snippet_details.score = base_score
        processed = nlp(snippet)
        #print("\nstart of snippet:\n")
        #print(Lemmatization("Machine Learning"))
        #print(snippet)
        for token in processed:
                # searching for dependencies between the keywords
                # don't care about case sensitivity
                if (token.text.lower() in word_one.lower()):
                        children = [child for child in token.children]
                        for child in children:
                                if (word_two in child.text):
                                        snippet_details.score += 200
                                        # if found, add score and stop searching
                                        break
                                grandchildren = [child for child in child.children]
                                for grandchild in grandchildren:
                                        if (word_one in grandchild.text):
                                                snippet_details.score += 100
                                                break

                if (token.text.lower() in word_two.lower()):
                        children = [child for child in token.children]
                        for child in children:
                                if (word_one in child.text):
                                        snippet_details.score += 200
                                        # if found, add score and stop searching
                                        break
                                grandchildren = [child for child in child.children]
                                for grandchild in grandchildren:
                                        if (word_one in grandchild.text):
                                                snippet_details.score += 100
                                                break

                # take one point off for each word in the snippet
                snippet_details.score -= 1


        if (word_one.lower() in snippet.lower()):
                snippet_details.score += 100
        if (word_two.lower() in snippet.lower()):
                snippet_details.score += 100

        return snippet_details

def FindRelationship(word_one, word_two, n=3, deeper_web_search=False):
        # TODO: search google and corpus for snippets of sentences containing
        # the relationship of word 1 and 2

        # currently using hard coded phrases
        snippet_list = []
        google_result = SearchGoogle(word_one, word_two, deeper_web_search)
        snippet_list.extend(google_result)
        scores = []
        base_score = google_base_weight
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score)
                scores.append(updated_snippet)
                
                base_score -= google_weight_scale
                if (base_score < 0):
                        base_score = 0

        PrintBestScores(scores, n)

def FindRelationshipJson(word_one, word_two, json_path, n=3, deeper_web_search=False):
        snippet_list = SearchJsonFile(word_one, word_two, json_path)

        scores = []
        cur_size = len(snippet_list)
        for i in range(cur_size):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)

        google_result = SearchGoogle(word_one, word_two, deeper_web_search=False)
        snippet_list.extend(google_result)
        
        base_score = google_base_weight
        for i in range(cur_size, len(snippet_list)):
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score)
                scores.append(updated_snippet)
                
                base_score -= google_weight_scale
                if (base_score < 0):
                        base_score = 0
                
        PrintBestScores(scores, n)

# add additional argument for filtered json file,
def FindRelationshipModifiedJson(word_one, word_two, json_path, modified_json_path, n=3, deeper_web_search=False):
        snippet_list = SearchJsonFile(word_one, word_two, json_path, modified_json_path)

        scores = []
        cur_size = len(snippet_list)
        for i in range(cur_size):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)

        google_result = SearchGoogle(word_one, word_two, deeper_web_search=False)
        snippet_list.extend(google_result)
        base_score = google_base_weight
        for i in range(cur_size, len(snippet_list)):
                snippet = snippet_list[i]
                updated_snippet = ScoreSentence(snippet, word_one, word_two, base_score)
                scores.append(updated_snippet)
                
                base_score -= google_weight_scale
                if (base_score < 0):
                        base_score = 0
        
        PrintBestScores(scores, n)

def FindRelationshipGivenSentences(word_one, word_two, list, n=3):
        scores = []
        for snippet in list:
                updated_snippet = ScoreSentence(snippet, word_one, word_two)
                scores.append(updated_snippet)
        PrintBestScores(scores, n)
        
def PrintBestScores(scores, n):
        #scores = scores.sort()
        scores.sort(key=attrgetter('score'))

        # for i in range(len(scores)):
        #         print(scores[i].score)

        if (n > len(scores)):
                print("Not enough good snippets found. Returning top " + len(scores) + " snippets instead")

        snippet_count = min(len(scores), n)
        print("Printing top " + str(snippet_count) + " snippets")
        for i in range(snippet_count):
                cur_index = len(scores) - i - 1
                print("Snippet " + str(i) + " sentence:")
                print(scores[cur_index].string)
                print("With a score of " + str(scores[cur_index].score))

def Lemmatization(words):
        processed = nlp(words)
        result = ""
        for token in processed:
                result += token.lemma_
        return result

def LemmatizeEntireFile(input_path, output_path):

        # create or delete output_path
        # try:
        #         open(output_path, "w")
        #         print("output path file found, overwriting contents")
        # except IOError:
        #         print("output path file not found, creating one instead")
        
        copyfile(input_path, output_path)

        with open(output_path, "r") as output_file:
                json_data = json.load(output_file)
                print("LENGTH =========== ")
                print(len(json_data))
                #cut_json = json_data[:295306]
                size_to_lemma = 50000
                json_data = json_data[:size_to_lemma]
                for i in tqdm(range(size_to_lemma)):
                        # value = json_data[i]
                        json_data[i][''] = Lemmatization(json_data[i][element_to_search])
                        # lemmatized = Lemmatization(value['abstract'])
                        # to_write = {
                        #         "abstract" : lemmatized,
                        # }
                        # json.dump(to_write, output_file)
                output_file.close()
        with open(output_path, 'w') as output_file:
                output_file.write(json.dumps(json_data))

def SearchJsonFile(word_one, word_two, path, modified_json_path=None, max_limit=40):
        snippets = []
        with open(path) as json_file:
                simplified_one = Lemmatization(word_one).lower()
                simplified_two = Lemmatization(word_two).lower()
                # lemmatized json file has been initialized already
                if modified_json_path != None:
                        with open(modified_json_path) as modified_json_file:
                                json_data = json.load(json_file)
                                modified_json_data = json.load(modified_json_file)
                                length = min(len(json_data), len(modified_json_data))
                                for i in range(length):
                                        snippet = modified_json_data[i][element_to_search].lower()
                                        if (simplified_one in snippet or simplified_two in snippet):
                                                # print(snippet)
                                                # print(json_data[i]['abstract'])
                                                sentences = snippet.split(".")
                                                for j in range(len(sentences)):
                                                        if (simplified_one in sentences[j] or simplified_two in sentences[j]):
                                                                snippets.append(json_data[i][element_to_search].split(".")[j] + ".")
                                        # stop after hitting max amount
                                        if (len(snippets) >= max_limit):
                                                break
                                        
                # searching regular json file
                else:
                        json_data = json.load(json_file)
                        # simplify words down into lemmmas, so that the words can be found
                        
                        # search for abstracts that fit the expected path
                        for value in json_data:
                                #simplified_abstract = Lemmatization(value['abstract'])
                                compare = value[element_to_search].replace(" ", "")
                                # check each sentence
                                sentences = compare.split(".")
                                for i in range(len(sentences)):
                                        if (simplified_one in sentences[i]) or (simplified_two in sentences[i]):
                                                snippets.append(value[element_to_search].split(".")[i] + ".")
                                
                                # stop after hitting max amount
                                if (len(snippets) >= max_limit):
                                        break

        return snippets

def SearchGoogle(word_one, word_two, deeper_web_search=False):
        snippets = []
        # replace space with + for google query
        item_one = word_one.replace(' ', '+')
        item_two = word_two.replace(' ', '+')
        google_query = 'https://www.google.com/search?q='+item_one+'+'+item_two

        # getting snippets from google search
        page = requests.get(google_query)
        html_page = page.text
        # takes the snippet from the page
        soup = BeautifulSoup(html_page, "html.parser")
        snippet_soup = soup.select(".s3v9rd.AP7Wnd")

        # TODO: Work on Deep search
        # # get links from 
        # # https://stackoverflow.com/questions/25471450/python-getting-all-links-from-a-google-search-result-page
        # for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #         full_link = re.split(":(?=http)",link["href"].replace("/url?q=",""))
        #         print(full_link)
        #         cur_html_page = requests.get(google_query).text
        #         soup = BeautifulSoup(cur_html_page, "html.parser")
        #         # print(soup.prettify())
        #         # for elem in soup(text=re.compile(r' #\S{11}')):
        #                 # check if possible snippet
        #                 # if (word_one in elem.parent) or (word_two in elem.parent):
        #                 #         print(elem.parent)
        #                 # print(elem.parent)
        #         pattern_one = re.compile(word_one)
        #         pattern_two = re.compile(word_two)
        #         # for tag in soup.find_all(True):
        #         #         if (word_one in tag or word_two in tag):
        #         #                 print(tag)

        # to search 
        # soup = BeautifulSoup(html_page, 'lxml')
        # for result in soup.select('.tF2Cxc'):
        #         link = result.select_one('.yuRUbf a')['href']
        #         print(link, sep='\n')
        
        # links = soup.findAll("a")
        # print(links)
        # for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #         print(re.split(":(?=http)",link["href"].replace("/url?q=","")))
                
                

        
        # direct snippets from google
        for item in snippet_soup:
                # dont want repeats
                to_add = item.getText(strip=True)
                if (any(to_add in string for string in snippets)):
                        #print("hi....")
                        #print(to_add)
                        
                        snippets.append(to_add)
                        if (len(snippets) >= max_search_count):
                                break
        return snippets

## helper function taken from
## https://stackoverflow.com/questions/42824129/dependency-parsing-tree-in-spacy
#def to_nltk_tree(node):
#        if node.n_lefts + node.n_rights > 0:
#            return Tree(token_format(node),
#                       [to_nltk_tree(child) 
#                        for child in node.children]
#                   )
#        else:
#            return token_format(node)


