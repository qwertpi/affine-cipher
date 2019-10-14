#need regex to check for special characters
import re
#need random numbers to perform random shifts
from random import randint, choice
from string import ascii_lowercase as lowercase
def SortList(l):
    '''
    Removes duplicates and sorts a list by how many duplicates there were
    :param l: list, the list to be sorted
    :return: a list in decending order of the number of duplicates
    '''
    #creates a dictionary with keys of the list elements and values of how often the key appears in the list
    l = {x: l.count(x) for x in set(l)}
    #sorts the dict by the keys and pulls out the keys
    l = [x for x in sorted(l, key=l.get, reverse=True)]
    return l
    
def NgramFinder(text, n=2):
    '''
    Finds ngrams in a string
    :param text: string, the string to search for ngrams input
    :param n: int, the n value for the n gram eg. 2 for bigram, 3 for trigram etc.
    :return: a list of all the ngrams (may contain duplicates)
    '''
    grams = []
    i = 0
    try:
        while True:
            ngram = text[i]
            #bigram needs current character and one character ahead, trigram needs up to second character etc.
            for step in range(1, n):
                ngram += text[i+step]
            
            clean = True
            for char in ngram:
                if char not in lowercase:
                    clean = False
                    break
            if clean:
                grams.append(ngram)
            i += 1
    #once we get to the end of the string an index error will be caused
    except IndexError:
        pass

    return grams

def char_to_num(char):
    '''
    Takes a letter and converts it to it's postion in the alphabet
    :param char: string, the letter to be converted
    :return: int, the position
    '''
    if ALPHABET_STARTS_AT_0:
        return ord(char) - 97
    else:
        return ord(char) - 96
    
def num_to_char(n):
    '''
    Takes a letter's position in the alphabet and converts it to the letter
    :param n: int, the postion to be converted
    :return: str, the letter
    '''
    if ALPHABET_STARTS_AT_0:
        return chr(n + 97)
    else:
        return chr(n + 96)
    
def encrypt(string, multiplier, shift):
    '''
    Encrypts a string with the caeser cipher
    :param string: string, the string to encrypt
    :param multiplier: int, the multiplication portion of the key
    :param shift: int, the shift to use
    :return: string, the encrypted text
    '''
    #inits the variable storing our ciphertext so that we can append to it
    ciphertext = ""
    
    #loops over every character in the string
    #makes everything lowercase to make my life easier
    for char in string.lower():
        #if the character is alphabetical encrypts it
        if re.match("[a-z]", char):
            #gets the character as a ascii number
            #subtracts 96 to make it a number from 1-26
            #adds the shift
            #does modulo 26 so we wrap back around if we go above 26
            #adds 96 to turn it back into a valid asci character code
            #converts that number to a charcater
            #and appends it to the ciphertext variable
            ciphertext += num_to_char((char_to_num(char) * multiplier  + shift) % 26)

            #26=z but 26%26=0 which results in the ` character this fixes this
            #if the last character (the one we jsut appended) is an `
            if ciphertext[-1] == "`":
                #removes the last character
                ciphertext = ciphertext[:-1]
                #appends a z to cipher text
                ciphertext += "z"
        else:
            #adds non alphabetical characters as they are
            ciphertext += char
            
    return ciphertext

def decrypt(string, multiplier, shift):
    '''
    Encrypts a string with the caeser cipher
    :param string: string, the string to encrypt
    :param multiplier: int, the multiplication portion of the key
    :param shift: int, the shift to use
    :return: string, the encrypted text
    '''
    #first step of decryption is just encrytion with a negative shift
    plaintext = encrypt(string, 1, -shift)
    #second step is the same as encyption with the inverse key and a 0 shift
    plaintext = encrypt(plaintext, INVERSES[multiplier], 0)
    return plaintext

#dcode.fr says a=0, b=1 etc. but some other sites say a=1, b=2 etc.
#encrpytion and decryption will still work regardess 
#but key based decryption and the accuracy of clauated keys from brute force rely upon this being the same as what was used for encryption

ALPHABET_STARTS_AT_0 = False
INVERSES = {}
class NoSolution(Exception):
    'Raised when no inverse exists'
def inverse(x, m):
    for a in range(0, m):
        if (x*a) % m == 1:
            return a
    raise NoSolution

for i in range(0, 26):
    try:
        INVERSES[i] = inverse(i, 26)
    except NoSolution:
            pass
MODE = input("Would you like to 1) Encrypt or 2) Decrypt    ").lower()

if MODE == "1" or MODE == "encrypt":
    text = input("Enter the text you wish to encrypt or place it in a file named input.txt   ").lower()
    if text == "":
        try:
            with open("input.txt", "r") as f:
                text = f.read().lower()
        except FileNotFoundError:
            print("No text was provided and the file input.txt doesn't exist, non-existant text can't be encrypted!")
    try:
        multiplier = int(input("Enter the multiplier you wish to use or leave blank to use a random shift    "))
        shift = int(input("Enter the shift you wish to use or leave blank to use a random shift    "))
        
    #if they left it blank the cast to int will fail raising this error
    except ValueError:
        shift = randint(1, 26)
        multiplier = choice(list(INVERSES.keys()))

    print(encrypt(text, multiplier, shift))
    print(multiplier, shift)
    
elif MODE == "2" or MODE == "decrypt":
    text = input("Enter the text you wish to decrypt or place it in a file named input.txt   ").lower()

    #opens the file if no text input was provided
    if text == "":
        try:
            with open("input.txt", "r") as f:
                text = f.read().lower()
        except FileNotFoundError:
            print("No text was provided and the file input.txt doesn't exist, non-existant text can't be decrypted!")
    
    try:
        multiplier = int(input("Enter the multiplier if you know it else leave this blank    "))
        shift = int(input("Enter the shift if you know it else leave this blank    "))
        plaintext = decrypt(text, multiplier, shift)
        print(plaintext)

    #if they left the shift blank the cast to int will fail raising this error
    except ValueError:
        CRIB = input("Enter a crib to search for in the posible decryptions if you know it else leave this blank    ").lower()

        plaintexts = [decrypt(text, multiplier, shift) for shift in range(1, 26) for multiplier in INVERSES.keys()]
        #if they typed a crib
        if CRIB != "":
            #shows each of the plaintexts along with their shift
            while True:
                for el in plaintexts:
                    if CRIB in el:
                        #TODO caluclate and print multiplier and shift
                        #prints the plaintext with the option for them to press enter when they want to see the next plaintext
                        input(el)
        else:
            #without a crib we fall back to bigrams and trigrams
            for el in plaintexts:
                #gets the bigrams and trigrams in the text in lists of decending order of frequency
                letter_frequencies = SortList(NgramFinder(el, 1))
                BIGRAMS = SortList(NgramFinder(el))
                TRIGRAMS = SortList(NgramFinder(el, 3))
                #checks if any of the top three bigrams for enlish text are in the top two bigrams for this plaintext
                #then does the same for trigrams
                #and the same for the top 2 single letters
                if (BIGRAMS[0] == "th" or BIGRAMS[1] == "th" or
                    BIGRAMS[0] == "he" or BIGRAMS[1] == "he" or
                    BIGRAMS[0] == "in" or BIGRAMS[1] == "in" or
                    TRIGRAMS[0] == "the" or TRIGRAMS[1] == "the" or
                    TRIGRAMS[0] == "and" or TRIGRAMS[1] == "and" or
                    TRIGRAMS[0] == "ing" or TRIGRAMS[1] == "ing" or
                    letter_frequencies[0] == "e" or letter_frequencies[1] == "e" or
                    letter_frequencies[0] == "t" or letter_frequencies[1] == "t"):
                        #TODO caluclate and print multiplier and shift
                        #prints the plaintext with the option for them to press enter when they want to see the next plaintext
                        input(el)
                    
else:
    print("That mode doesn't exist, please restart the program") 
