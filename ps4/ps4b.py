# Problem Set 4B
# Name: Gabriel Munoz
# Collaborators: None
# Time Spent: Wednesday, October 28, 2020 - Wednesday, November 4, 2020

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    # close the file??? - 06/09/2021
    inFile.close()
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        # initialize an empty dictionary
        dict = {}
        # concatenate alpha strings
        alpha = string.ascii_uppercase + string.ascii_lowercase
        # iterate i = 0 to i = 51 for 52 alphabet letters -> 0-25 upper and 26-51 lower
        for i in range(len(alpha)):
            # two cases - uppercase and lowercase letters
            # if letter is uppercase
            if i < 26:
                # if shifted index within uppercase, proceed and map to shifted value
                if i + shift < 26:
                    # if key doesn't already exist, add it and assign the value - the alphabet letter shifted down
                    dict[alpha[i]] = dict.get(alpha[i], alpha[i + shift])
                # if shifted index falls into lowercase range, circle back to upper case
                else:
                    dict[alpha[i]] = dict.get(alpha[i], alpha[(i+shift) % 26])
            # if letter is lowercase
            else:
                # if shifted index within lowercase, proceed and map to shifted value
                if i + shift < 52:
                    dict[alpha[i]] = dict.get(alpha[i], alpha[i + shift])
                # else if shifted index falls outside the list, need to circle back up to lowercase
                else:
                    # need to mod 26 to get to corresponding UPPERCASE letter, then add 26 to get to lowercase
                    dict[alpha[i]] = dict.get(alpha[i], alpha[((i+shift) % 26) + 26])
        return dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''

        # build the shift dictionary
        shift_dict = self.build_shift_dict(shift)
        # get the message text
        message = self.get_message_text()
        # initialize empty string for the shifted message text
        shifted_message = ""

        # iterate through message text
        for char in message:
            # if curr char is alphabetical, concatenate (append) the char by accessing shift_dict
            if char.isalpha():
                shifted_message += shift_dict[char]
            # else (if space or symbol), concatenate (append) the char as is
            else:
                shifted_message += char
        return shifted_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''

        # call the Message constructor within PlaintextMessage constructor - assigns message_text and valid_words
        # assign other 3 attributes within PlaintextMessage
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        # don't want the original dictionary to be mutated
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        # call the parent class (Message) constructor - parameter text is an encrypted message
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        # create empty list to append number of valid words created by each shift value
        num_valid_words = []

        # iterate integers 0 to 25 and try every shift value
        for i in range(26):
            # apply the shift and store it
            decrypted_message = self.apply_shift(26-i)
            # get every word in the message and iterate through list, counting the valid words
            words = decrypted_message.split(' ')
            valid_words = 0
            for word in words:
                if is_word(self.get_valid_words(), word):
                    valid_words += 1
            # append the valid word count to its shift/index position in the list
            num_valid_words.append(valid_words)

        # return the first index position--shift value--with the max number of words, and the decrypted message
        shift_to_decrypt = num_valid_words.index(max(num_valid_words))
        decrypted_message = self.apply_shift(26-shift_to_decrypt)
        return (shift_to_decrypt, decrypted_message)

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    print("Test case 1 - PlaintextMessage - encryption")
    plaintext = PlaintextMessage("hello", 2)
    print("Message: " + plaintext.get_message_text())
    print("Expected Output: jgnnq")
    print("Actual Output: " + plaintext.get_message_text_encrypted(), end='\n\n')

    print("Test case 2 - PlaintextMessage - encryption")
    plaintext2 = PlaintextMessage("OKAY Computer", 4)
    print("Message: " + plaintext2.get_message_text())
    # OK Computer? Ahaha
    print("Expected Output: SO Gsqtyxiv")
    print("Actual Output: " + plaintext2.get_message_text_encrypted(), end='\n\n')

    print("Test case 3 - CiphertextMessage - decryption")
    ciphertext = CiphertextMessage(plaintext.get_message_text_encrypted())
    print("Expected output: (2, 'hello')")
    print("Actual output: " + str(ciphertext.decrypt_message()), end='\n\n')

    print("Test case 4 - CiphertextMessage - decryption")
    ciphertext2 = CiphertextMessage(plaintext2.get_message_text_encrypted())
    # rip, OK not a word in our wordlist, so had to use OKAY
    print("Expected output: (4, 'OKAY Computer')")
    print("Actual output: " + str(ciphertext2.decrypt_message()), end='\n\n')

    #TODO: best shift value and unencrypted story 

    print("Test case 5 - story - decryption")
    cipher_story = CiphertextMessage(get_story_string())
    print("Encrypted story:" + '\n' + cipher_story.get_message_text(), end='\n\n')
    print("Shift value: " + str(cipher_story.decrypt_message()[0]), end='\n')
    print("Decrypted story:" + '\n' + cipher_story.decrypt_message()[1], end='\n\n')
