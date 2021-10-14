# Problem Set 4A
# Name: Gabriel Munoz
# Collaborators: None
# Time Spent: Monday, October 26, 2020

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # base case - if sequence is of length 1, return the sequence (or if empty string, the empty string)
    if len(sequence) <= 1:
        return [sequence]

    # recursive case
    else:
        # initialize a list for permutations
        perms = []

        # NEED to call this function again on the same sequence starting at the NEXT index position
        # (insert each of the chars in sequence into different spots in the sub-sequence)
        # recursive call WILL CUT THE SEQUENCE BY ONE EACH TIME - decreasing the input "n" to ensure
        # original function call terminates - i.e. we reach the base case
        char_one = sequence[0]
        sub_sequence = sequence[1:]
        perms_sub = get_permutations(sub_sequence)

        # for every permutation in list of permutations of sub sequence, insert char into every spot in curr perm
        for perm_sub in perms_sub:
            # will form perm of length of sub_sequence + 1 b/c adding char into sub_sequence
            for i in range(len(perm_sub) + 1):
                # perm_sub[0:i=0] gives '', so will start inserting char at start of perm and following with rest
                # next iter, perm_sub[0:i=1] gives first char of perm_sub and inserts char at second position, etc.
                perm = perm_sub[0:i] + char_one + perm_sub[i:]
                # append the newly formed permutation into the perms list
                perms.append(perm)

        # return the list of permutations
        return perms

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # test 1
    test_in_1 = "abc"
    print("Input: " + test_in_1)
    print("Expected output: " + str(['abc', 'bac', 'bca', 'acb', 'cab', 'cba']))
    print("Actual output: " + str(get_permutations(test_in_1)), end='\n\n')

    # test 2
    test_in_2 = "bust"
    print("Input: " + test_in_2)
    print("Expected output: " + str(['bust', 'ubst', 'usbt', 'ustb', 'bsut', 'sbut', 'subt', 'sutb']))
    print("Actual output: " + str(get_permutations(test_in_2)), end='\n\n')

    # test 3
    test_in_3 = "plum"
    print("Input: " + test_in_3)
    print("Expected output: " + str(['plum', 'lpum', 'lupm', 'lump', 'pulm', 'uplm', 'ulpm', 'ulmp']))
    print("Actual output: " + str(get_permutations(test_in_3)), end='\n\n')
