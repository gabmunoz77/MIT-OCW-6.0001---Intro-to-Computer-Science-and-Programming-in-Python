# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Gabriel Munoz
# Collaborators : None
# Time spent    : Thursday, October 8, 2020 - Tuesday, October 20, 2020

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # handling only lower case, so use copy of word in lower case
    word = word.lower()

    # initialize first component
    comp1 = 0
    # iterate through word and add each letter's points using the dictionary for scrabble letter values
    for letter in word:
        comp1 += SCRABBLE_LETTER_VALUES[letter]

    # compute second component
    comp2 = 7*len(word) - 3*(n-len(word))

    # return score: if comp2 > 1, use comp2, else use 1
    if comp2 > 1:
        return comp1*comp2
    else:
        return comp1*1

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    # modified to leave space to add wildcard - '*'
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    # add in the wildcard - '*'
    if '*' not in hand:
        hand['*'] = hand.get('*', 0) + 1

    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    # should not modify original hand, so make a copy first - name "hand" okay, right...? because of scope?!
    hand = hand.copy()

    # iterate through letters in word
    for letter in word:
        # CASE INSENSITIVE - need lower case
        letter = letter.lower()
        # if that letter is in player's hand at least once, decrease frequency by 1
        if letter in hand and hand[letter] > 0:
            hand[letter] -= 1
            # if letter no longer in hand, delete from hand dictionary
            if hand[letter] < 1:
                del(hand[letter])

    # return the updated dictionary
    return hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    # Letters in hand?
    # Do not want to mutate original hand, so make copy to modify
    hand = hand.copy()
    # bool True if word composed of letters in the hand
    letters_in_hand = True
    # check every letter in word - make copy of word in lower case to modify
    word_lower = word.lower()
    for letter in word_lower:
        # if letter in hand, remove letter, decrement its frequency by one, and if freq falls to 0, delete it
        if letter in hand and hand[letter] > 0:
            hand[letter] -= 1
            if hand[letter] < 1:
                del(hand[letter])
        # if letter not in hand, know word is not valid, exit out of loop
        else:
            letters_in_hand = False
            break

    # Valid word?
    # bool to check if valid word - True if word is valid wildcard word or if word is in the word list
    valid_word = False
    # if wildcard '*' used in word, check for wildcard word
    wild_index = word.find('*')
    if wild_index != -1:
        # make copy of word with '*' replaced by a vowel
        for i in range(len(VOWELS)):
            # need LIST b/c strings immutable
            word_wild = list(word.lower())
            word_wild[wild_index] = VOWELS[i]
            # stitch word back together to check if it's in list
            word_wild = ''.join(word_wild)
            # if potential word is a word in the word list, mark bool True and exit loop
            if word_wild in word_list:
                valid_word = True
                break
    # else if wildcard '*' not used in word, check that word in lower case exists in word list
    else:
        valid_word = word.lower() in word_list

    # now return True if valid word AND if word's letters are in hand
    return valid_word and letters_in_hand

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    # count up the number of letters in the hand and return the total
    len = 0
    for letter in hand:
        # adds the frequency of each letter in the hand to the counter
        len += hand[letter]
    return len

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0

    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("\nCurrent Hand: ", end='')
        display_hand(hand)
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                word_score = get_word_score(word, calculate_handlen(hand))
                total_score += word_score
                print('"' + word + '"' + " earned " + str(word_score) + " points. Total: "
                      + str(total_score) + " points")
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if word == "!!":
        print("\nTotal score: " + str(total_score) + " points")
    else:
        print("\nRan out of letters. Total score for this hand: " + str(total_score) + " points")
    # separate hands by dashed line
    print("----------")
    # Return the total score as result of function
    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    # replace the letter with a random choice of any vowel or consonant NOT IN HAND ALREADY
    # create copy of hand - not to mutate original
    hand = hand.copy()
    # to select random letter to sub in
    alpha = list("*abcdefghijklmnopqrstuvwxyz")
    for let in hand.keys():
        del(alpha[alpha.index(let)])
    # if letter is in hand, replace it with random choice
    if letter in hand:
        # create new key with random letter in alpha list - which already excluded letters in hand
        #   and assign it the value of the letter to be replaced - return 0 as default value if key doesn't exist
        hand[random.choice(alpha)] = hand.pop(letter, 0)

    return hand
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # ask for user input
    num_hands = int(input("Enter total number of hands: "))
    # counter to track the total score of every hand
    total_score = 0
    # user has one letter substitution and one hand replay
    letter_sub, hand_replay = 1, 1

    # start playing hands
    while num_hands > 0:
        # deal a hand, display the hand to user
        hand = deal_hand(HAND_SIZE)
        print("Current hand: ", end='')
        display_hand(hand)

        # if the user has letter substitution option, ask them if they want to use it and proceed
        if letter_sub > 0:
            lsub = input("Would you like to substitute a letter? ").lower()
            if lsub == "yes":
                letter_out = input("Which letter would you like to replace: ")
                hand = substitute_hand(hand, letter_out)
                letter_sub -= 1
            else:
                pass

        # continue playing hand, whether it was changed or not, and store the played hand's score
        score_curr = [play_hand(hand, word_list)]

        # if the user has replay hand option, ask them if they want to use it and proceed
        if hand_replay > 0:
            hreplay = input("Would you like to replay the hand? ").lower()
            if hreplay == "yes":
                # replay the hand and the store replay score
                score_curr.append(play_hand(hand, word_list))
                hand_replay -= 1
            else:
                pass

        # add the current hand score to the total - if hand replayed, add the higher of the two
        score_curr.sort()
        total_score += score_curr[0]
        # decrement hands played - shouldn't for a replayed hand
        num_hands -= 1

    # print out the score over all hands
    print("Total score over all hands: " + str(total_score))

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
