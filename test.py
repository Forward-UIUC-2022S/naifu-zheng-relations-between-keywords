import FindRelationship
import SnippetDetails
import unittest

# sample sentences used in testing
# good sentences
google_one = "In computer science, a Btree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time."
# missing second keyword
google_two = "The Btree generalizes the binary search tree, allowing for nodes with more than two children."
# Concise, but lacks information
google_three = "Btree is a data structure that store data in its node in sorted order"
snippet_list = [google_one, google_two, google_three]

class TestFindRelationships(unittest.TestCase):

    # TEST 1: small sample for running files
    def test_lemma(self):
        print("Running Test 1\n")
        FindRelationship.LemmatizeEntireFile("/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv_lemmatized.json")
        
    # TEST 2: test the example sentences
    def test_individual_sentence(self):
        print("Running Test 2\n")
        print("score 1:")
        print(FindRelationship.ScoreSentence(google_one, "Btree", "Data Structure").score)
        print("score 2:")
        print(FindRelationship.ScoreSentence(google_two, "Btree", "Data Structure").score)
        print("score 2:")
        print(FindRelationship.ScoreSentence(google_three, "Btree", "Data Structure").score)
    
    # Test 3: test the sentences as a list
    def test_list(self):
        print("Running Test 3\n")
        FindRelationship.FindRelationshipGivenSentences("Btree", "Data Structure", snippet_list)
    
    # Test 4: testing basic online search
    def test_web_search(self):
        FindRelationship.FindRelationship("Btree", "Data Structure")
    
    # Test 5: testing basic json search
    def test_json(self):
        print("Running Test 5\n")
        FindRelationship.FindRelationshipJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv.json")
    
    # Test 6: testing output of test 1 
    def test_modified_json(self):
        print("Running Test 6\n")
        FindRelationship.LemmatizeEntireFile("/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv_lemmatized.json")
        FindRelationship.FindRelationshipModifiedJson("Btree", "Data Structure", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv.json", "/Users/enteilegend/forward_lab/Meaningful-Relations-Between-Keywords/sample_arxiv_lemmatized.json")    


suite = unittest.TestSuite()
#suite.addTest(TestFindRelationships("test_lemma"))
#suite.addTest(TestFindRelationships("test_individual_sentence"))
#suite.addTest(TestFindRelationships("test_list"))
#suite.addTest(TestFindRelationships("test_web_search"))

# note: test 5 and 6 are mostly for catching crashes, as web results are better than json sample snippets.
#suite.addTest(TestFindRelationships("test_json"))
#suite.addTest(TestFindRelationships("test_modified_json"))
runner = unittest.TextTestRunner()
runner.run(suite)
