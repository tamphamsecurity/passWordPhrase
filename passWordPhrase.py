import string
import secrets
import json
import math
from string import digits, ascii_letters, punctuation, ascii_uppercase
import argparse

"""
Json Password file downloaded from
https://github.com/matthewreagan/WebstersEnglishDictionary
"""
class LoadDictionaryFile():
    def __init__(self):
        self.WebstersDictionary = None 

    def LoadFile(self):
        with open("./data/dictionary.json") as fileHandle:
            self.WebstersDictionary = json.load(fileHandle)
       
    def RandomCharacters(self, count=1)->string:
        myPassword = str()
        passwordCharacters = digits + ascii_letters + punctuation

        combinations = math.pow(len(passwordCharacters), count)
        # print("The number of base2 combinations for random %d characters are %d" % (count, math.log2(combinations)))

        for x in range(count):
            myPassword += secrets.choice(passwordCharacters)
        return myPassword


    def PassWord(self, count=2, insertNumbers=False, insertSpecial=False, insertChars=False, insertUpper=False)->str:
        dictionary_combinations = 0
        separator_combinations = 0
        total_combinations = 0

        myPassword = str()
        iteration = 0
        websters = list(self.WebstersDictionary.keys())
        # print(str(len(webstersDictionary)) + "\n")
        lenDictionary = len(websters)
        dictionary_combinations = math.pow(lenDictionary, count)

        separators = self.AdditionalSeparatorCharacters(insertNumbers, insertSpecial, insertChars, insertUpper)
        lenSep = len(separators)

        if(separators):
            separator_combinations = math.pow(lenSep, count-1)

        if(separators):
            total_combinations = dictionary_combinations * separator_combinations
        else:
            total_combinations = dictionary_combinations

        # print("The number of base2 combinations for count of %d are %d" %(count, math.log2(total_combinations)))
        
        for iteration in range(count):
            # iteration += 1
            word = secrets.choice(websters)
            word.replace(" ", "") # remove apostrophes
            myPassword += word # secrets.choice(websters)

            if (count > 1) and (iteration < count-1):
                if insertNumbers or insertSpecial or insertChars or insertUpper:
                    myPassword += secrets.choice(separators)
        
        return myPassword

    def AdditionalSeparatorCharacters(self,insertNumbers=False, insertSpecial=False, insertChars=False, insertUpper=False)->str:
        separatorCharacters = ""

        if(insertChars): separatorCharacters += ascii_letters
        if(insertUpper): separatorCharacters += ascii_uppercase
        if(insertNumbers): separatorCharacters += digits
        if(insertSpecial): separatorCharacters += punctuation
        return separatorCharacters


def main():
    parser = argparse.ArgumentParser(description="Generate password phrases using a dictionary.")
    parser.add_argument('--count', type=int, default=4, help='Number of words in the password phrase')
    parser.add_argument('--insertNumbers', action='store_true', help='Include numbers as separators')
    parser.add_argument('--insertSpecial', action='store_true', help='Include special characters as separators')
    parser.add_argument('--insertChars', action='store_true', help='Include letters as separators')
    parser.add_argument('--insertUpper', action='store_true', help='Include uppercase letters as separators')
    parser.add_argument('--repeat', type=int, default=1, help='Number of password phrases to generate')
    args = parser.parse_args()

    myFile = LoadDictionaryFile()
    myFile.LoadFile()

    for _ in range(args.repeat):
        result = myFile.PassWord(
            count=args.count,
            insertNumbers=args.insertNumbers,
            insertSpecial=args.insertSpecial,
            insertChars=args.insertChars,
            insertUpper=args.insertUpper
        )
        print(result)


if __name__ == "__main__":
    main()



