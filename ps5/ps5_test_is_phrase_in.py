# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Gabriel Munoz
# Collaborators: None
# Time: Wednesday, March 10, 2021 - Tuesday, March 30, 2021

# NOT ORIGINALLY IN ps5 - file here is my own
# This is a prototype for the the PhraseTrigger method is_phrase_in
# implementing idea for a possible solution and testing it here in separate function and file

import string

def is_phrase_in(phrase, text):
    """
    Checks whether the phrase is in the given text.

    :param text: (string) a snippet or long body of text in which to look for the phrase

    :return: (boolean) True if the whole phrase is present in text, False otherwise - NOT case-sensitive
    """

    # Algorithm
    # assumption(s): phrase is a valid phrase
    # 1. lower case both the text and the phrase
    # 2. iterate through text, replace characters in string.punctuation with spaces
    # 3. Create word lists of text and phrase by splitting it over the spaces
    # 4. Need to check 2 things: that all words from phrase are in text; that they appear consecutively -- ie. that
    #       the words in phrase all have consecutive indices in the word list for text (consecutive indices have
    #       indices that when subtracted == 1)

    # working with text and phrase NOT case-sensitive
    phrase = phrase.lower()
    text = text.lower()
    # lets replace all the special characters with spaces
    for char in string.punctuation:
        text = text.replace(char, " ")
    # lets list all the words in the text by splitting over whitespace (space(s))
    text_word_list = text.split()
    # could we get any empty strings? If so, remove them...
    # the words in our phrase as well
    phrase_word_list = phrase.split()
    # initialize boolean to return for phrase trigger if phrase found in text
    found = True
    # create empty list to append INDICES of words from phrase that appear in the text
    test_word_indices = []
    # iterate over phrase word list
    for i in range(len(phrase_word_list)):
        # compare every word in text to each word in phrase
        for j in range(len(text_word_list)):
            if phrase_word_list[i] == text_word_list[j]:
                test_word_indices.append(j)
    # if did not at least find all the words in the phrase, we know the phrase is NOT in the text
    if len(test_word_indices) < len(phrase_word_list):
        return not found
    # now we check that every consecutive pair of words in the LIST is consecutive in the TEXT (are 1 index apart)
    for i in range(len(test_word_indices) - 1):
        # if any consecutive pair of words in the LIST is NOT consecutive in the LIST, we know phrase is not in text
        if test_word_indices[i + 1] - test_word_indices[i] != 1:
            return not found
    # if we finish the loop, we know every word in the phrase was found at consecutive locations in the text and
    # i.e. the phrase was found in the text
    return found


print("Phrase: purple COW")
phrase = "purple COW"

# Should result in True:
test_True_text = ["PURPLE COW", "The purple cow is soft and cuddly.", "The farmer owns a really PURPLE cow.",
                  "Purple!!! Cow!!!", "purple@#$%cow", "Did you see a purple cow?"]
print('\n'+"Test True test snippets")
for elem in test_True_text:
    print(is_phrase_in(phrase, elem))

# Should result in False:
test_False_text = ["Purple cows are cool!", "The purple blob over there is a cow.", "How now brown cow.",
                   "Cow!!! Purple!!!", "purplecowpurplecowpurplecow"]
print('\n'+"Test False test snippets")
for elem in test_False_text:
    print(is_phrase_in(phrase, elem))

