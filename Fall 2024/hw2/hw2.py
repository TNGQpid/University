import sys
import math
import string


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    with open (filename,encoding='utf-8') as f:
        data = f.read()

    data = data.upper()
    UpAlpha = set(string.ascii_uppercase)

    for character in UpAlpha:
        X[character] = 0
        
    for character in data:
        if character in UpAlpha:
            X[character] += 1

    return X

#Q1 output
print("Q1")
X = shred(sys.argv[1])
X = sorted(X.items())
for character, count in X:
    print(f"{character} {count}")


#Q2
e,s = get_parameter_vectors()
a = X[0][1] * math.log(e[0])
b = X[0][1] * math.log(s[0])
print("Q2")
print(float("{:.4f}".format(a)))
print(float("{:.4f}".format(b)))


#Q3
PYE = float(sys.argv[2])
PYS = float(sys.argv[3])
if PYE == 0:
    logPYE = -100000
else:
    logPYE = math.log(PYE)
if PYS == 0:
    logPYS = -100000
else:
    logPYS = math.log(PYS)
FYE = logPYE + sum(X[i][1] * math.log(e[i]) if e[i] != 0 else X[i][1] * -100000 for i in range(26))
FYS = logPYS + sum(X[i][1] * math.log(s[i]) if s[i] != 0 else X[i][1] * -100000 for i in range(26))
print("Q3")
print(float("{:.4f}".format(FYE)))
print(float("{:.4f}".format(FYS)))


#Q4
def get_prob(FYE, FYS):
    if FYS - FYE >= 100:
        return 0
    elif FYS - FYE <= -100:
        return 1
    else:
        return 1 / (1 + math.exp(FYS - FYE))
print("Q4")
prob = get_prob(FYE, FYS)
print(float("{:.4f}".format(prob)))
