# Problem Set 4C
# Name: Gabriel Munoz
# Collaborators: None
# Time Spent: Wednesday, November 4, 2020 - Wednesday, February 24, 2021

import string
from ps4a import get_permutations

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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
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

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # initialize an empty dictionary
        dict = {}
        # concatenate alpha strings
        alpha = string.ascii_uppercase + string.ascii_lowercase
        # concatenate vowel permutation strings
        vowels = vowels_permutation.upper() + vowels_permutation
        # iterate i = 0 to i = 4 for 5 vowels - set up counter
        j = 0
        # iterate i = 0 to i = 51 for all 52 upper and lower case letters
        for i in range(len(alpha)):
            # assign keys to their values
            # if consonant, keep the same
            if alpha[i] in CONSONANTS_UPPER or alpha[i] in CONSONANTS_LOWER:
                dict[alpha[i]] = dict.get(alpha[i], alpha[i])
            # if vowel
            else:
                dict[alpha[i]] = dict.get(alpha[i], vowels[j])
                j += 1
        return dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        # get the message text
        message_text = self.get_message_text()
        # initialize empty string for the transposed message
        transposed_message = ""

        # iterate through message - if alphabetical, append the transposed character; if not, append it as is
        for char in message_text:
            if char.isalpha():
                transposed_message += transpose_dict[char]
            else:
                transposed_message += char
        return transposed_message
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # get all the permutations of the vowels
        vowel_permutations = get_permutations("aeiou")
        # create empty list to count number of valid words each vowel permutation yields
        num_valid_words = []

        # iterate through list of permutations (5! = 120 permutations)
        for perm in vowel_permutations:
            # build the current permutation's transpose dictionary
            transpose_dict = self.build_transpose_dict(perm)
            # apply the transpose to the encrypted message to decrypt the message
            decrypt_message = self.apply_transpose(transpose_dict)

            # get every word in the decrypted message
            words = decrypt_message.split(' ')
            # start counter for valid words for current permutation's decrypted message
            valid_words = 0
            for word in words:
                if is_word(self.get_valid_words(), word):
                    valid_words += 1
            # append valid word count to the current permutation's index position in the list
            num_valid_words.append(valid_words)

        # find the first index position--the permutation--that yields the max number of valid words
        decryption_permutation_index = num_valid_words.index(max(num_valid_words))
        # return the decrypted message using the permutation found above
        decrypt_dict = self.build_transpose_dict(vowel_permutations[decryption_permutation_index])
        decrypted_message = self.apply_transpose(decrypt_dict)
        return decrypted_message

if __name__ == '__main__':

    # Example test case 1
    print("Example Test Case 1", end="\n")
    message = SubMessage("HEllo World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "HAllu Wurld!")
    encrypt_text = message.apply_transpose(enc_dict)
    print("Actual encryption:", encrypt_text, end="\n\n")

    # now create EncryptedMessage object with the encrypted text from message
    print("Now to decrypt our freshly encrypted message...", end="\n")
    encrypted_message = EncryptedSubMessage(encrypt_text)
    # decrypt EncryptedMessage
    decrypt_message = encrypted_message.decrypt_message()
    print("Decrypted message:", decrypt_message)
    # check if decryption was successful
    if decrypt_message == message.get_message_text():
        print("Decryption successful! :" + ")", end="\n\n\n")
    else:
        print("Decryption unsuccessful! :" + "(", end="\n\n\n")


    # Example test case 2 - same message, different permutation
    print("Example Test Case 2", end="\n")
    permutation = "eiuao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption: " + "HIlla Warld!")
    print("Actual encryption: " + message.apply_transpose(enc_dict), end="\n\n")

    # now create EncryptedMessage object with the encrypted text from message, using permutation 2
    print("Now to decrypt our freshly encrypted message...", end="\n")
    encrypted_message = EncryptedSubMessage(encrypt_text)
    # decrypt EncryptedMessage
    decrypt_message = encrypted_message.decrypt_message()
    print("Decrypted message:", decrypt_message)
    # check if decryption was successful
    if decrypt_message == message.get_message_text():
        print("Decryption successful! :" + ")", end="\n\n\n")
    else:
        print("Decryption unsuccessful! :" + "(", end="\n\n\n")


    # Example test case 3 - new message, permutation 2
    print("Example Test Case 3", end="\n")
    message = SubMessage("I ate fruit and cheese for lunch yesterday")
    permutation = "eiuao"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "U eti frout end chiisi far lonch yistirdey")
    encrypt_text = message.apply_transpose(enc_dict)
    print("Actual encryption:", encrypt_text, end="\n\n")

    # now create EncryptedMessage object with the encrypted text from message
    print("Now to decrypt our freshly encrypted message...", end="\n")
    encrypted_message = EncryptedSubMessage(encrypt_text)
    # decrypt EncryptedMessage
    decrypt_message = encrypted_message.decrypt_message()
    print("Decrypted message:", decrypt_message)
    # check if decryption was successful
    if decrypt_message == message.get_message_text():
        print("Decryption successful! :" + ")", end="\n\n\n")
    else:
        print("Decryption unsuccessful! :" + "(", end="\n\n\n")


    # Example test case 4 - new message, random permutation

    # to select a random vowel permutation
    import random
    print("Example Test Case 4", end="\n")
    message = SubMessage("I will eat spaghetti and vegetables with an Italian meat sauce tonight")
    # list of permutations
    vowel_permutations = get_permutations(VOWELS_LOWER)
    # generate a random permutation index and access the list of permutations to select and store it
    permutation = vowel_permutations[random.randrange(0, len(vowel_permutations))]
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Uhh, depends on the vowel permutation??!")
    encrypt_text = message.apply_transpose(enc_dict)
    print("Actual encryption:", encrypt_text, end="\n\n")

    # now create EncryptedMessage object with the encrypted text from message
    print("Now to decrypt our freshly encrypted message...", end="\n")
    encrypted_message = EncryptedSubMessage(encrypt_text)
    # decrypt EncryptedMessage
    decrypt_message = encrypted_message.decrypt_message()
    print("Decrypted message:", decrypt_message)
    # check if decryption was successful
    if decrypt_message == message.get_message_text():
        print("Decryption successful! :" + ")", end="\n\n\n")
    else:
        print("Decryption unsuccessful! :" + "(", end="\n\n\n")

