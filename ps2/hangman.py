# Problem Set 2, hangman.py
# Name: Gabriel Munoz
# Collaborators: None
# Time spent: Monday, September 28, 2020 - Wednesday, September 30, 2020

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    # count num of letters guessed correctly
    letters_correct = 0
    # check if each letter in the secret word has been guessed by the user
    for letter in secret_word:
        # if curr letter guessed correctly, increment counter
        if letter in letters_guessed:
            letters_correct += 1
    # return bool true if letters guessed correctly == length of secret word
    return letters_correct == len(secret_word)



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    # check whether word has been guessed - if it has, return secret word, otherwise continue
    if is_word_guessed(secret_word, letters_guessed):
        return secret_word
    else:
        # make a list copy of secret word to iterate over
        secret_word_list = list(secret_word)
        # iterate over the secret word list
        for i in range(len(secret_word_list)):
            # if the current letter is NOT guessed yet, replace it with and underscore and space
            if secret_word_list[i] not in letters_guessed:
                secret_word_list[i] = '_ '
        return ''.join(secret_word_list)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    # create list copy of lower alpha letters string
    lower_alpha_list = list(string.ascii_lowercase)
    # iterate through letters in letters guessed and remove from lower alpha
    for letter in letters_guessed:
        # in case letter is not a letter, list.remove(letter) would give an error - don't want that
        if letter in letters_guessed:
            lower_alpha_list.remove(letter)
    # return the string version of the remaining lower alpha list
    return ''.join(lower_alpha_list)
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    # initialize number of guesses, warnings, unique letters, and an empty list to retrieve the available letters
    num_guesses = 6
    letters_guessed = []
    warnings = 3
    unique_letters = 0

    # greet the player
    print("Welcome to the game Hangman!")
    # let user know how many letters are in the computer's word
    print("I am thinking of word that is " + str(len(secret_word)) + " letters long.")
    print("You have " + str(warnings) + " warnings left.")
    print("-------------")

    # start the game - continue while the user has not guessed the secret word and has not run out of guesses
    while not is_word_guessed(secret_word, letters_guessed) and num_guesses > 0:
        # get available letters
        available_letters = get_available_letters(letters_guessed)
        # let user know the number of guesses left and the available letters to guess
        print("You have " + str(num_guesses) + " guesses left.\nAvailable letters: " + available_letters)
        # ask the user for a guess and validate input - only work with lower case, but accept upper
        guess = str.lower(input("Please guess a letter: "))

        # while the user does not supply a valid guess
        while not str.isalpha(guess) or guess in letters_guessed:
            # user loses warning if their guess is not alphabetical or if they have guessed the letter before
            warnings -= 1
            if not str.isalpha(guess):
                print("Oops! That is not a valid letter.")
            elif guess in letters_guessed:
                print("Oops! You've already guessed that letter.")
            # tell user how many warnings they have left
            if warnings >= 0:
                print("You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
            # if user gives unacceptable input when out of warnings, they lose a guess
            else:
                num_guesses -= 1
                print("You have no warnings left so you lose one guess: " +
                      get_guessed_word(secret_word, letters_guessed))
            print("-------------")
            # if user still has guesses, continue, otherwise break out of loop, game lost
            if num_guesses > 0:
                # let user know the number of guesses left and the available letters to guess
                print("You have " + str(num_guesses) + " guesses left.")
                print("Available letters: " + available_letters)
                # new guess
                guess = input("Please guess a letter: ")
                guess = str.lower(guess)
            # if guesses go to 0, break out
            else:
                break

        # add user guess to list of guessed letters and check it only if alphabetical
        if str.isalpha(guess):
            letters_guessed.append(guess)
            # tell user whether guess in secret word or not and print secret word with only the guessed letters shown
            if guess in secret_word:
                print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
                print("-------------")
                # number of correct guesses is the same as the number of unique letters in the secret word
                unique_letters += 1
            else:
                # lose 2 guesses if wrong guess was vowel, 1 if consonant
                if guess in "aeiou":
                    num_guesses -= 2
                else:
                    num_guesses -= 1
                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print("-------------")

    # exited the loop - check if win or loss
    if num_guesses < 1:
        print("Sorry, you ran out of guesses. The word was " + secret_word + ".")
    # congratulate and print out score
    else:
        print("Congratulations, you won!")
        # print out the total score - it equals num_guesses remaining X unique_letters
        print("Your total score for this game is: " + str(num_guesses*unique_letters))



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    # first need copy of my_word without spaces
    my_word_no_spaces = my_word.replace(" ", "")
    # if the two words' lengths are not the same, no match, return False
    if len(my_word_no_spaces) != len(other_word):
        return False
    # otherwise, check letters
    for i in range(len(my_word_no_spaces)):
        # if character is alphabetical and does not equal the current letter in other word, return False
        if str.isalpha(my_word_no_spaces[i]) and my_word_no_spaces[i] != other_word[i]:
            return False
        # if character is a blank and the current letter in other word is in the word guessed, return False
        else:
            if my_word_no_spaces[i] == "_" and other_word[i] in my_word_no_spaces:
                return False
    # if reach this point, there is a match
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    # iterate through entire word list - if match_with_gaps(my_word, curr word) == True, print, else no matches
    # boolean to check to false if there are matches
    no_matches = True
    for i in range(len(wordlist)):
        if match_with_gaps(my_word, wordlist[i]):
            # print words without newline
            print(wordlist[i] + " ", end="")
            no_matches = False
    if no_matches:
        print("No matches found")



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    # initialize number of guesses, warnings, unique letters, and an empty list to retrieve the available letters
    num_guesses = 6
    letters_guessed = []
    warnings = 3
    unique_letters = 0

    # greet the player
    print("Welcome to the game Hangman!")
    # let user know how many letters are in the computer's word
    print("I am thinking of word that is " + str(len(secret_word)) + " letters long.")
    print("You have " + str(warnings) + " warnings left.")
    print("-------------")

    # start the game - continue while the user has not guessed the secret word and has not run out of guesses
    while not is_word_guessed(secret_word, letters_guessed) and num_guesses > 0:
        # get available letters
        available_letters = get_available_letters(letters_guessed)
        # let user know the number of guesses left and the available letters to guess
        print("You have " + str(num_guesses) + " guesses left.\nAvailable letters: " + available_letters)
        # ask the user for a guess and validate input - only work with lower case, but accept upper
        guess = str.lower(input("Please guess a letter: "))

        # while the user does not supply a valid guess
        while not str.isalpha(guess) or guess in letters_guessed or guess == "*":
            # user loses warning if their guess is not alphabetical or if they have guessed the letter before
            if guess != "*":
                warnings -= 1
                if not str.isalpha(guess):
                    print("Oops! That is not a valid letter.")
                elif guess in letters_guessed:
                    print("Oops! You've already guessed that letter.")

                # tell user how many warnings they have left
                if warnings >= 0:
                    print("You have " + str(warnings) + " warnings left: " +
                          get_guessed_word(secret_word, letters_guessed))
                # if user gives unacceptable input when out of warnings, they lose a guess
                else:
                    num_guesses -= 1
                    print("You have no warnings left so you lose one guess: " +
                          get_guessed_word(secret_word, letters_guessed))
            # HANGMAN WITH HINTS ADDITION
            else:
                print("Possible word matches are: ")
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                # to add newline not printed in show_possible_matches
                print("")

            print("-------------")

            # if user still has guesses, continue, otherwise break out of loop, game lost
            if num_guesses > 0:
                # let user know the number of guesses left and the available letters to guess
                print("You have " + str(num_guesses) + " guesses left.")
                print("Available letters: " + available_letters)
                # new guess
                guess = input("Please guess a letter: ")
                guess = str.lower(guess)
            # if guesses go to 0, break out
            else:
                break

        # add user guess to list of guessed letters and check it only if alphabetical
        if str.isalpha(guess):
            letters_guessed.append(guess)
            # tell user whether guess in secret word or not and print secret word with only the guessed letters shown
            if guess in secret_word:
                print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
                print("-------------")
                # number of correct guesses is the same as the number of unique letters in the secret word
                unique_letters += 1
            else:
                # lose 2 guesses if wrong guess was vowel, 1 if consonant
                if guess in "aeiou":
                    num_guesses -= 2
                else:
                    num_guesses -= 1
                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print("-------------")

    # exited the loop - check if win or loss
    if num_guesses < 1:
        print("Sorry, you ran out of guesses. The word was " + secret_word + ".")
    # congratulate and print out score
    else:
        print("Congratulations, you won!")
        # print out the total score - it equals num_guesses remaining X unique_letters
        print("Your total score for this game is: " + str(num_guesses*unique_letters))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
