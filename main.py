from email.quoprimime import quote
from math import remainder
from operator import index
from socket import if_indextoname
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# from numpy import append 
digit = "0123456789"
character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# string = 

class AnalisisLexico():
    def __init__(self, atg_file):
        print ('---------START----------')
        self.compiler = ""
        self.characters = ""
        self.keywords = ""
        self.tokens = ""
        self.readATG(atg_file)
    
    def readATG(self, atg_file):
        compiler = ""
        characters = []
        keywords = []
        tokens = []
        productions = []
        
        isCompiler = False
        isCharacters = False
        isKeywords = False
        isTokens = False
        isProductions = False

        temp = ''
        for line in atg_file:
            words = line.split()
            if len(words) > 0:
                if(words[0].lower() == 'compiler' and compiler == ""):
                    isCompiler = True
                    isCharacters = False
                    isKeywords = False
                    isTokens = False
                    isProductions = False
                elif(words[0].lower() == 'characters'):
                    isCompiler = False
                    isCharacters = True
                    isKeywords = False
                    isTokens = False
                    isProductions = False
                elif(words[0].lower() == 'keywords'):
                    isCompiler = False
                    isCharacters = False
                    isKeywords = True
                    isTokens = False
                    isProductions = False
                elif(words[0].lower() == 'tokens'):
                    isCompiler = False
                    isCharacters = False
                    isKeywords = False
                    isTokens = True
                    isProductions = False
                elif words[0].lower() == 'end':
                    break
                
            
                if isCompiler:
                    compiler = words[1]
                    isCompiler = False
                elif isCharacters:
                    characters.append(line)
                elif isKeywords:
                    keywords.append(line)
                elif isTokens:
                    temp += line
                    if line[-1] == '.' or temp == 'TOKENS':
                        tokens.append(temp)
                        temp = ''
                elif isProductions:
                    productions.append(line)
                    isProductions = False



        if len(characters) > 0:
            characters.pop(0)
    
        if len(tokens) > 0:
            tokens.pop(0)

        if len(keywords) > 0:
            keywords.pop(0)

        if len(productions) > 0:
            productions.pop(0)
        print(compiler)
        print('---------------------- CHARACTERS ------------------------------------------------------')
        print(characters)
        print('---------------------- KEYWORDS ------------------------------------------------------')
        print(keywords)
        print('---------------------- TOKENS ----------------------------------------------------------')
        print(tokens)
        print("\n\n")
        symbols = "{ .}=\"+|'()"
        regexsymbols = "+-/|#*.^?!\'\"\\"
        keys = []
        values = []
        isQuote = False
        isApostrophe = False
        isConcat = False
        isSubstract = False
        isValue = False
        quoteCounter = 0
        apostropheCounter = 0
        indxcnt = 0
        for line in characters:
            words = line.split()
            for word in words:
                indxcnt = 0
                interpreted = ''
                for n in word:
                    indxcnt = indxcnt + 1
                    if n == "\"":
                        quoteCounter = quoteCounter + 1
                        if quoteCounter%2 == 1:
                            isQuote = True
                        else:
                            isQuote = False
                    if n == "\'":
                        apostropheCounter = apostropheCounter + 1
                        if apostropheCounter%2 == 1:
                            isApostrophe = True
                        else:
                            isApostrophe = False
                    elif n == "=":
                        if isValue:
                            print("error: hay un = mal puesto en la linea ", characters.index(line))
                            break
                        else:
                            isValue = True
                    elif n == "+":
                        isConcat = True
                        if len(values) == len(keys) and isValue:
                            values[-1] = values[-1] + '|'

                    elif n == "-":
                        isSubstract = True
                   
                    if isQuote:
                        if n != "\"":
                            if word[indxcnt] == "\"":
                                if n in regexsymbols:
                                    interpreted = interpreted + '\\' + str(n)
                                else:
                                    interpreted = interpreted + str(n)
                            else:
                                if n in regexsymbols:
                                    interpreted = interpreted + '\\' + str(n) + '|'
                                else:
                                    interpreted = interpreted + str(n) + '|'

                    elif isApostrophe:
                        if n != "\'":
                            if n in regexsymbols:
                                    interpreted = interpreted + '\\' + str(n)
                            else:
                                interpreted = interpreted + str(n)
                    else:
                        if isValue:
                            if indxcnt == len(word):
                                if n == ".":
                                    #If there is no key to refer, keep adding logic to last value[]
                                    if interpreted[:4] == "CHR(":
                                        if int(interpreted[4:-1]) in range(0,100):
                                            if n in regexsymbols:
                                                interpreted = '\\' + chr(int(interpreted[4:-1]))
                                            else:
                                                interpreted = chr(int(interpreted[4:-1]))
                                        else:
                                            print("error leyendo ", interpreted)

                                    if len(values) == len(keys):
                                        if interpreted in keys:
                                            varadd = values[keys.index(interpreted)]
                                            varef = values[-1]
                                            values[-1] = varef[:len(varef)] + varadd[:len(varadd)]
                                        else:
                                            varef = values[-1]
                                            values[-1] = varef[:len(varef)] + interpreted
                                    elif len(values) < len(keys):
                                        values.append(interpreted)
                                    else:
                                        print("Hay mas values que keys")
                                    isValue = False

                                else:
                                    if interpreted[:4] == "CHR(":
                                        interpreted = interpreted + str(n)
                                        if int(interpreted[4:-1]) in range(0,100):
                                            if n in regexsymbols:
                                                interpreted = '\\' + chr(int(interpreted[4:-1]))
                                            else:
                                                interpreted = chr(int(interpreted[4:-1]))
                                        else:
                                            print("error leyendo ", interpreted)

                                    if n not in symbols:
                                        interpreted = interpreted + str(n)
                                    if len(values) == len(keys):
                                        #if word when operating in keys
                                        if interpreted in keys:
                                            values[-1] = values[-1] + values[keys.index(interpreted)]
                                        #if word when operating not in keys
                                        else:
                                            values[-1] = values[-1] + interpreted
                                    elif len(values) < len(keys):
                                        if interpreted != "":
                                            if interpreted in keys:
                                                values.append(values[keys.index(interpreted)])
                                            else:
                                                values.append(interpreted)
                            else:
                                if n != "\"" and n != "\'":
                                    interpreted = interpreted + str(n)
                                
                        elif not isValue:
                            if indxcnt == len(word):
                                #If there is no key to refer, keep adding logic to last value[]
                                if len(values) == len(keys):
                                    if interpreted in keys:
                                        print("error, variable ya definida antes")
                                    else:
                                        interpreted = interpreted + str(n)
                                        keys.append(interpreted)
                                else:
                                    print("error, mala sintaxis en variable definida")
                            else:
                                interpreted = interpreted + str(n)

                        else:
                            print("Error de programa :(")
                            break
        print("CHARACTERS\n")
        print("keys:",keys)
        print("values:",values)
        keys2 = []
        values2 = []
        isValue = False
        for line in keywords:
            words = line.split()
            for word in words:
                if word == "=":
                    if isValue:
                        print("error: hay un = mal puesto en la linea ", characters.index(line))
                        break
                    else:
                        isValue = True

                if isValue:
                    if word[-1] == ".":
                        if word[-2] == "\"" and word[0] == "\"":
                            values2.append(word[1:-2])   
                        isValue = False 
                else:
                    keys2.append(word)
        print("\n\KEYWORDS")
        print("keys:",keys2)
        print("values:",values2)
        
        symbols = "{ .}=\"|"
        keys3 = []
        values3 = []
        isQuote = False
        isApostrophe = False
        isConstrain = False
        isValue = False
        quoteCounter = 0
        apostropheCounter = 0
        indxcnt = 0
        for line in tokens:
            words = line.split()
            for word in words:
                indxcnt = 0
                interpreted = ''
                for n in word:
                    indxcnt = indxcnt + 1
                    if n == "=":
                        if isValue:
                            print("error: hay un = mal puesto en la linea ", characters.index(line))
                            break
                        else:
                            isValue = True
                        
                    if isValue:
                        if isQuote:
                            if n != "\"":
                                if n in ".":
                                    values3[-1] = values3[-1] + "\\" + str(n)
                                else:
                                    values3[-1] = values3[-1] + str(n)
                        elif interpreted in keys and word[indxcnt-1] in symbols:
                            if len(keys3) == len(values3):
                                values3[-1] = values3[-1] + '(' + values[keys.index(interpreted)] + ')'
                                interpreted = ''
                            elif len(keys3) > len(values3):
                                values3.append('(' + values[keys.index(interpreted)] + ')')
                                interpreted = ''
                        elif interpreted+str(n) in keys and indxcnt==len(word):
                            interpreted = interpreted + str(n)
                            if len(keys3) == len(values3):
                                values3[-1] = values3[-1] + '(' + values[keys.index(interpreted)] + ')'
                                interpreted = ''
                            elif len(keys3) > len(values3):
                                values3.append('(' + values[keys.index(interpreted)] + ')')
                                interpreted = ''
                        else:
                            interpreted = interpreted + str(n)

                        if n == "\"":
                            quoteCounter = quoteCounter + 1
                            if quoteCounter%2 == 1:
                                values3[-1] = values3[-1] + "("
                                isQuote = True
                            else:
                                values3[-1] = values3[-1] + ")"
                                interpreted = ""
                                isQuote = False
                        elif n == "{":
                            values3[-1] = values3[-1] + "("
                        elif n == "}":
                            values3[-1] = values3[-1] + ")*"
                        elif n == "|":
                            values3[-1] = values3[-1] + "|"
                        elif n == "." and  not isQuote:
                            isValue = False
                    else:
                        if indxcnt == len(word):
                            #If there is no key to refer, keep adding logic to last value[]
                            if len(values3) == len(keys3):
                                if interpreted in keys or interpreted in keys3:
                                    print("error, variable ya definida antes")
                                else:
                                    interpreted = interpreted + str(n)
                                    keys3.append(interpreted)
                            else:
                                print("error, mala sintaxis en variable definida")
                        else:
                            interpreted = interpreted + str(n)
        print("\n\n")
        for n in keys3:
            print(keys3[keys3.index(n)],": ", values3[keys3.index(n)])
            values3[keys3.index(n)] = '^' + values3[keys3.index(n)] + '$'
        
        print("\n\n")

        scannerFile = ''
        scannerFile = f""" 
import re
from functools import reduce
from itertools import accumulate
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

def scanner():
    chrline = chr(219)
    blank = ' '

    keywords = {dict(zip(values2, keys2))}
    tokens = {dict(zip(keys3, values3))}

    compiler_defines_blank = reduce(lambda cummulative, current : cummulative or bool(re.match(current[1], blank)), tokens.items(), False)
    start = 0
    forward = 0
    isConsulting = False
    output = ''

    print('Please enter the file to analize')
    text_file = askopenfilename()
    text_in_file = ''
    with open(text_file, 'r') as reader:
        for line in reader:
            for n in line:
                if n != '\\n':
                    text_in_file += n
                else:
                    text_in_file += chrline

    for index in range(len(text_in_file) + 1):
        if index == start: isConsulting = True
        temporary = text_in_file[start:forward]
        if temporary in keywords and (not reduce(lambda cummulative, current : cummulative or bool(re.match(current[1], text_in_file[start:forward + 1])), [*tokens.items(), *keywords.keys()], False)):
            output += f"{{keywords[temporary]}} "
            start = index
            isConsulting = False
        elif not compiler_defines_blank and temporary == blank:
            start = index
            isConsulting = False
        elif temporary == chrline:
            start = index
            isConsulting = False
        else:
            for key, value in tokens.items():
                if temporary and re.match(value, temporary):
                    temp = [character for character in text_in_file[forward:]]
                    res = list(accumulate(temp, lambda x, y: "".join([x, y])))
                    remainder_stream = [f"{{temporary}}{{element}}" for element in res]
                    strMatch = lambda string : reduce(lambda accumulator, current: accumulator or re.fullmatch(current[1], string), [*tokens.items(), *keywords.keys()], False)
                    stillMatching = reduce(lambda accumulator, current: accumulator or strMatch(current), remainder_stream, False)
                    
                    if not stillMatching:
                        print("<",temporary,">", ":", key)
                        output += '{{}} '.format(key)
                        start = index
                        isConsulting = False
                        break
        forward += 1

    if isConsulting:
        print('ERROR LEXICO')
        print(start)
        print(len(text_in_file))
        return {{
            'output': 'Error lexico'
        }}
    else:
        print(output, file=open('output.txt', 'a'))
        return {{
            'output': output,
            'residue': temporary
        }}
scanner()
        """
        file = open("./scanner.py", "x")
        file.write(scannerFile)
        file.close()

                        



print('Please enter the atg guide file')
Tk().withdraw()
atg_file = askopenfilename() 

with open(atg_file, 'r') as reader:
    atg_file =[]
    for line in reader:
        if line != '\n':
            atg_file.append(line.strip())

analisislexico = AnalisisLexico(atg_file)