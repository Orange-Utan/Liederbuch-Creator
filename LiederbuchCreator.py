#######################################################################
#                                                                     #
#   Liederbuch Creator Ver 1.0.0                                      #
#   von Frowin                                                        #
#                                                                     #
#   ------ How-To: ------                                             #
#                                                                     #
#   1. Python Package "odfpy" installieren                            #
#                                                                     #
#   2. Die Input Datei (standardmäßig data.txt) mit dem Text          #
#   und den Akkorden bereitstellen. Die Akkorde sollen direkt         #
#   vor die Silbe auf der sie angeschlagen werden in eckige           #
#   Klammern gesetzt werden (zB [a]Roter Mond, [G]überm               #
#   Silbersee). Die Erste Zeile ist die Überschrift.                  #
#   Beispielhaft ist die Datei data.txt auch schon beschrieben        #
#                                                                     #
#   3. Das Skript ausführen                                           #
#                                                                     #
#   4. In der Textdatei alle Dollarzeichen ($) mit Leerzeichen        #
#   ersetzen und die Anzahl der Absätze anpassen, dass alles auf      #
#   maximal 2 Seiten passt, aber trotzdem gut zu lesen ist.           #
#   Dabei auf eventuelle Fehler prüfen                                #
#                                                                     #
#   5. Fertig :)                                                      #
#                                                                     #
#######################################################################

LiederOutputName = "neues_lied" # Name der Output-Datei
LiederInputName = "data.txt" # Pfad von der Input-Datei


#################### Ab hier nichts mehr ändern ######################

try:
    from odf.opendocument import OpenDocumentText
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           ListLevelProperties, TabStop, TabStops)
    from odf.text import (H, P, Span, List, ListItem, ListStyle, ListLevelStyleNumber,
                          ListLevelStyleBullet)
except:
    print("Fehler: odfpy wurde nicht korrekt installiert")

charWidth = {
    " ": 4.4453125,
    "!": 4.4453125,
    '"': 5.6796875,
    "#": 8.8984375,
    "$": 8.8984375,
    "%": 14.2265625,
    "&": 10.671875,
    "'": 3.0546875,
    "(": 5.328125,
    ")": 5.328125,
    "*": 6.2265625,
    "+": 9.34375,
    ",": 4.4453125,
    "-": 5.328125,
    ".": 4.4453125,
    "/": 4.4453125,
    "0": 8.8984375,
    "1": 7.7228125,
    "2": 8.8984375,
    "3": 8.8984375,
    "4": 8.8984375,
    "5": 8.8984375,
    "6": 8.8984375,
    "7": 8.8984375,
    "8": 8.8984375,
    "9": 8.8984375,
    ":": 4.4453125,
    ";": 4.4453125,
    "<": 9.34375,
    "=": 9.34375,
    ">": 9.34375,
    "?": 8.8984375,
    "@": 16.2421875,
    "A": 10.671875,
    "Ä": 10.671875,
    "B": 10.671875,
    "C": 11.5546875,
    "D": 11.5546875,
    "E": 10.671875,
    "F": 9.7734375,
    "G": 12.4453125,
    "H": 11.5546875,
    "I": 4.4453125,
    "J": 8,
    "K": 10.671875,
    "L": 8.8984375,
    "M": 13.328125,
    "N": 11.5546875,
    "O": 12.4453125,
    "Ö": 12.4453125,
    "P": 10.671875,
    "Q": 12.4453125,
    "R": 11.5546875,
    "S": 10.671875,
    "T": 9.7734375,
    "U": 11.5546875,
    "Ü": 11.5546875,
    "V": 10.671875,
    "W": 15.1015625,
    "X": 10.671875,
    "Y": 10.671875,
    "Z": 9.7734375,
    "[": 4.4453125,
    #"\": 4.4453125,
    "]": 4.4453125,
    "^": 7.5078125,
    "_": 8.8984375,
    "`": 5.328125,
    "a": 8.8984375,
    "ä": 8.8984375,
    "b": 8.8984375,
    "c": 8,
    "d": 8.8984375,
    "e": 8.8984375,
    "f": 4.15921875,
    "g": 8.8984375,
    "h": 8.8984375,
    "i": 3.5546875,
    "j": 3.5546875,
    "k": 8,
    "l": 3.5546875,
    "m": 13.328125,
    "n": 8.8984375,
    "o": 8.8984375,
    "ö": 8.8984375,
    "p": 8.8984375,
    "q": 8.8984375,
    "r": 5.328125,
    "s": 8,
    "t": 4.4453125,
    "u": 8.8984375,
    "ü": 8.8984375,
    "v": 8,
    "w": 11.5546875,
    "x": 8,
    "y": 8,
    "z": 8,
    "{": 5.34375,
    "|": 4.15625,
    "}": 5.34375,
    "~": 9.34375,
    "ß": 9.9788961039,
}
lineFromDataDoc = []
lines = []
chords = []
dollarsRemoved = 0

# List 'line' with every line as an item
with open(LiederInputName) as file:
    for i, l in enumerate(file):
        lineFromDataDoc.append(l)
def removeAbsatz(line):
    for i in range(0,len(line)):
        line[i] = line[i][:-1]
removeAbsatz(lineFromDataDoc)


# Line List Correct splitting

def checkChordPosition(li):
    #print(li)
    l = li
    chord = [[],[]]


    for klammer in range(0, l.count('[')):
        #print(l.count('['))
        #print(l)

        # getting length of chords to subtract from final length
        klammermount = l.count('[')
        #print("klammermount: " + str(klammermount))
        klammerlen = 0
        pos = [[-1],[-1]]
        for k in range(0,klammermount):
            #print("K = " + str(k))
            posTemp = pos
            pos[0].append(l.index('[', posTemp[0][k]+1))
            pos[1].append(l.index(']', posTemp[1][k]+1))

            #print(pos[0][k+1])
            #print(pos[1][k+1])

            klammerlen += (pos[1][k+1] - pos[0][k+1]) + 1

        #print("klammerlen: " + str(klammerlen))
        #print(len(l)-klammerlen)

        for i in range(0,len(l)-klammerlen):
            chordlen = 0

            #print(l)
            #print(i + chordlen)

            if (l[i] == "["):
                while True:
                    if l[i+chordlen] != ']':
                        chord[0].append(l[i+chordlen+1])
                        #chord[1].append(i+chordlen+1)
                        chord[1].append(i + 1)
                        chordlen += 1
                    else:
                        chord[0].pop()
                        chord[1].pop()
                        l = l[:i] + l[i+chordlen+1:]
                        break
        klammerlen = 0

    return l, chord

def createChordAndLineLists():
    for i in range(0,len(lineFromDataDoc)):
        lin, cho = checkChordPosition(lineFromDataDoc[i])
        #print(lineFromDataDoc[i])
        lines.append(lin)
        chords.append(cho)
createChordAndLineLists()

def getLineLength(l):
    _len = 0
    for x in l:
        _len += charWidth[x]
    return _len

def getLeftPositionFromMiddlePosition(p, l):
    _p = 0
    lengthLine = getLineLength(l)
    #print(lengthLine)
    #print("RoundLenghtLine " + str(round(lengthLine / 2)))
    firstDigit = int(round(72.5 * charWidth[" "] - float(lengthLine) / 2))
    for i in range(p):
        _p += charWidth[l[i]]
    return firstDigit + _p - 2 * charWidth[" "]


### ------------ ###
### odt Document ###
### ------------ ###

textdoc = OpenDocumentText()

# Styles
s = textdoc.styles
h1style = Style(name="Default H Style", family="paragraph")
h1style.addElement(ParagraphProperties(attributes={"textalign": "center"}))
h1style.addElement(TextProperties(attributes={'fontsize':"16pt",'fontweight':"bold", 'fontname':"Arial", 'fontfamily':"Arial"}))

t1style = Style(name="Default Style", family="paragraph")
t1style.addElement(ParagraphProperties(attributes={"textalign": "center"}))
t1style.addElement(TextProperties(attributes={'fontsize':"12pt", 'fontname':'Arial', 'fontfamily':"Arial"}))

c1style = Style(name="Default C Style", family="paragraph")
c1style.addElement(ParagraphProperties(attributes={"textalign": "left"}))
c1style.addElement(TextProperties(attributes={'fontsize':"12pt", 'fontweight':"bold", 'fontname':'Arial', 'fontfamily':"Arial"}))

s.addElement(h1style)
s.addElement(t1style)
s.addElement(c1style)


# An automatic style
boldstyle = Style(name="Bold", family="text")
boldprop = TextProperties(fontweight="bold")
boldstyle.addElement(boldprop)
textdoc.automaticstyles.addElement(boldstyle)

# Ueberschrift
h = H(outlinelevel=1, stylename=h1style, text=lines[0])
textdoc.text.addElement(h)
t = H(outlinelevel=0, stylename=t1style, text="")
textdoc.text.addElement(t)


def liedzeilen():

    currentChordPos = 0 #3*charWidth[" "]

    for i in range(1,len(lines)):
        chordLine = ""
        for y in range(0,len(chords[i][0])):
            #print(chords[i])
            #print("y: " + str(y))
            if not chords[i][1]:
                print("chordsEmpty")
                chordPos = 0
            else:
                chordPos = getLeftPositionFromMiddlePosition(chords[i][1][y], lines[i])

            while currentChordPos <= chordPos:
                #print("chordPos: " + str(chordPos))
                chordLine += "$"
                currentChordPos += charWidth[" "]

            if not chords[i][0]:
                chordLine = ""
            else:
                #print(chords[i])
                #print(y)
                chordLine += chords[i][0][y]
                currentChordPos += charWidth[chords[i][0][y]]



        #print("chordLine: " + chordLine)
        currentChordPos = 0
        c = H(outlinelevel=0, stylename=c1style, text=chordLine)
        t = H(outlinelevel=0, stylename=t1style, text=lines[i])
        textdoc.text.addElement(c)
        textdoc.text.addElement(t)
liedzeilen()

def printDebug():
    print("Lied wurde erfolgreich erstellt mit dem Namen \"" + LiederOutputName + "\"")
printDebug()

textdoc.save("neues_lied.odt")
