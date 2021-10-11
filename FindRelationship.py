import spacy
from SnippetDetails import SnippetDetails

nlp = spacy.load("en_core_web_sm")
# good sentence
google_one = "In computer science, a B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The B-tree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "B-tree is a data structure that store data in its node in sorted order"

def ScoreSentence(snippet):
        snippet_details = SnippetDetails()
        print(type(snippet))
        processed = nlp(snippet)
        for token in processed:
                print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                        token.shape_, token.is_alpha, token.is_stop)
        #TODO:
        # dependency graph between the keywords

        
        return snippet_details

def FindRelationship(word_one, word_two):
        # TODO: search google and corpus for snippets of sentences containing
        # the relationship of word 1 and 2

        # currently using hard coded phrases
        snippet_list = [google_one, google_two, google_three]
        scores = []
        for snippet in snippet_list:
                updated_snippet = ScoreSentence(snippet)
                scores.append(updated_snippet.score)

        print(scores)

