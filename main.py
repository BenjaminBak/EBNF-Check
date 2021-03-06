# Opening/Reading a text file content
# Test 123
# Test 456
ntcharlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
    'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "-", "_"]


class Orgroup:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Or/'


class Recgroup:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Rec/'





class Recurse:
    def __init__(self, index):
        self.pointerindex = index
        self.representation = 'r/'+str(self.pointerindex)

    def __repr__(self):
        return self.representation

class Terminal:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '#T:'+self.content



class Nonterminal:
    def __init__(self, name, ableitung):
        self.name = name
        self.ableitungtxt = ableitung
        self.absableitung = []

    def __repr__(self):
        return self.name

    def parse1(self, nichtterminalarray):
        l = 0
        r = 0
        status = 0
        raw = []
        terminale = []
        i = -1
        for i in range(len(self.ableitungtxt)):
            if status == 0 and self.ableitungtxt[i] == ' ':
                continue
            elif status == 0 and self.ableitungtxt[i] == ',':
                continue
            elif status == 0 and self.ableitungtxt[i] == '|':
                raw.append('|')
            elif status == 0 and self.ableitungtxt[i] == '(':
                raw.append('(')
            elif status == 0 and self.ableitungtxt[i] == ')':
                raw.append(')')
            elif status == 0 and self.ableitungtxt[i] == '{':
                raw.append('{')
            elif status == 0 and self.ableitungtxt[i] == '}':
                raw.append('}')
            elif status == 0 and self.ableitungtxt[i] == '[':
                raw.append('[')
            elif status == 0 and self.ableitungtxt[i] == ']':
                raw.append(']')
            elif status == 0 and self.ableitungtxt[i] in ntcharlist:
                status = 1
                l = i
                continue
            elif status == 1 and (i == len(self.ableitungtxt) - 1 or self.ableitungtxt[i+1] not in ntcharlist):
                status = 0
                r = i+1
                valid = False
                for nt in nichtterminalarray:
                    if self.ableitungtxt[l:r] == nt.name:
                        raw.append(nt)
                        valid = True
                        break
                if not valid:
                    print("Error: Nichtterminal ohne Ableitung wurde gefunden ({})".format(self.ableitungtxt[l:r]))
                    exit(0)
            elif status == 0 and self.ableitungtxt[i] == '"':
                status = 2
                l = i+1
            elif status == 2 and self.ableitungtxt[i] == '"':
                status = 0
                r = i
                raw.append(Terminal(self.ableitungtxt[l:r]))
                if self.ableitungtxt[l:r] not in terminale:
                    terminale.append(self.ableitungtxt[l:r])

        self.absableitung = self.OrGroupFinder(self.parse2(raw))
        return terminale

    def parse2(self, raw):
        absableitung = []
        j = 0
        while j < len(raw):
            if isinstance(raw[j], Nonterminal):
                absableitung.append(raw[j])
            elif raw[j] == '|':
                absableitung.append('|')
            elif raw[j] == "(":
                depth = 0
                end = 0
                for k in range(j + 1, len(raw)):
                    if depth == 0 and raw[k] == ')':
                        end = k
                    elif raw[k] == '(':
                        depth += 1
                    elif raw[k] == ')':
                        depth -= 1
                raw2 = raw[j+1:end]
                absableitung.append(self.parse2(raw2))
                j = end
            elif raw[j] == "{":
                depth = 0
                end = 0
                for k in range(j + 1, len(raw)):
                    if depth == 0 and raw[k] == '}':
                        end = k
                    elif raw[k] == '{':
                        depth += 1
                    elif raw[k] == '}':
                        depth -= 1
                raw2 = raw[j + 1:end]
                absableitung.append(Recgroup())
                absableitung.append(self.parse2(raw2))
                j = end
            elif raw[j] == "[":
                depth = 0
                end = 0
                for k in range(j + 1, len(raw)):
                    if depth == 0 and raw[k] == ']':
                        end = k
                    elif raw[k] == '[':
                        depth += 1
                    elif raw[k] == ']':
                        depth -= 1
                raw2 = raw[j + 1:end]
                absableitung.append(Orgroup())
                absableitung.append([Terminal(""), self.parse2(raw2)])
                j = end
            elif isinstance(raw[j], Terminal):
                absableitung.append(raw[j])

            j += 1
        return absableitung

    def OrGroupFinder(self, raw):
        ableitung = raw
        ableitung2 = []

        for e in range(len(ableitung)):
            if isinstance(ableitung[e], Recgroup):
                ableitung[e + 1] = self.OrGroupFinder(ableitung[e + 1])
            elif isinstance(ableitung[e], list):
                ableitung[e] = self.OrGroupFinder(ableitung[e])

        templist = []  # list that holds temporarily the objects of a orgroup
        status = 0
        f = 0
        while f < len(ableitung):
            if isinstance(ableitung[f], Recgroup) or isinstance(ableitung[f], Orgroup):
                if status == 0 and f + 2 == len(ableitung):
                    ableitung2.extend(ableitung[f:f + 1])
                elif status == 1 and f + 2 == len(ableitung):
                    templist.extend(ableitung[f:f + 1])
                    ableitung2.append(Orgroup)
                    ableitung2.extend(templist)
                    templist = []
                    status = 0
                elif status == 0 and ableitung[f + 2] != "|":
                    ableitung2.extend(ableitung[f:f+1])
                elif status == 1 and ableitung[f + 2] != "|":
                    templist.extend(ableitung[f:f+1])
                    ableitung2.append(Orgroup)
                    ableitung2.extend(templist)
                    templist = []
                    status = 0
                else:
                    templist.extend(ableitung[f:f + 1])
                    f += 1
                    status = 1
            elif ableitung[f] == "|":
                pass
            else:
                if status == 0 and f + 1 == len(ableitung):
                    ableitung2.append(ableitung[f])
                elif status == 1 and f + 1 == len(ableitung):
                    templist.append(ableitung[f])
                    ableitung2.append(Orgroup)
                    ableitung2.append(templist)
                    templist = []
                    status = 0
                elif status == 0 and ableitung[f + 1] != "|":
                    ableitung2.append(ableitung[f])
                elif status == 1 and ableitung[f + 1] != "|":
                    templist.append(ableitung[f])
                    ableitung2.append(Orgroup)
                    ableitung2.append(templist)
                    templist = []
                    status = 0
                else:
                    templist.append(ableitung[f])
                    status = 1
            if f + 1 != len(ableitung):
                f += 1
            else:
                break
        return ableitung2


class Ebnfpruefer:
    def __init__(self, grammarfilename="txtfile.txt"):
        print("Überprüfe eingegebene Grammatik auf Fehler...\n")
        if self.texteingabecheck(grammarfilename):
            print("Die Überprüfung der Grammatik verlief erfolgreich.")
        else:
            print("\nBei der Überprüfung der Grammatik sind Fehler aufgetreten. \nÜberprüfen sie die Grammatik erneut, nachdem sie versucht haben diese zu beheben.")
            exit(0)
        self.grammartextarray = self.txtreadwithextra(grammarfilename)
        self.nichtterminalarray = []
        self.terminalalphabet = []
        self.grammatikbuilder(self.grammartextarray)

        for nt in self.nichtterminalarray:
            terminale = nt.parse1(self.nichtterminalarray)
            for t in terminale:
                if t not in self.terminalalphabet:
                    self.terminalalphabet.append(t)
        self.ugly = None
        self.tree = []
        self.branchconnect()
        self.word = None
        while True:
            print('\nGeben Sie nun das Wort an, dessen Konformität geprüft werden soll.\n')
            self.word = input('Zu prüfendes Wort:  ')
            print('\n')
            self.passed = False
            self.literalcheck()
            affiliation = None
            if self.passed:
                affiliation = True

            if affiliation:
                print(' ✔ Das angegebene Wort ist der Grammatik zugehörig.')
            else:
                print(' ✖ Das angegebene Wort ist der Grammatik nicht zugehörig.')
            print('\nWollen Sie mit der aktuellen Grammatik weitere Wörter prüfen? \n')
            exit_choice = input('(drücke y/n):  ')
            if exit_choice != 'y':
                break
        exit(0)


    def txtread(self, grammarfilename):
        txtarray = []  # Textarray
        with open(grammarfilename, "r") as raw:  # Öffnen der Textfile und Speichern in txtarray
            for line in raw:
                line = line.rstrip()
                txtarray.append(line)
        return txtarray

    def txtreadwithextra(self, grammarfilename):
        txtarray = []  # Textarray
        with open(grammarfilename, "r") as raw:  # Öffnen der Textfile und Speichern in txtarray
            for line in raw:
                line = line.rstrip()
                kommentar = False
                for x in line:
                    if x == " ":
                        continue
                    elif x == "#":
                        kommentar = True
                    else:
                        break
                if not kommentar:
                    txtarray.append(line)
        return txtarray

    def texteingabecheck(self, dokumentenname):
        # Funktion zur Überprüfung von zulässigen Nichtterminalen
        def wordcheck(wort):
            for i in wort:
                if i not in ntcharlist:
                    return False
            return True

        textareal = self.txtread(dokumentenname)  # Textarray

        errorstatus = True  # Variable zur Angabe der Richtigkeit der EBNF

        # Schleife, die die Zeilen durchgeht
        for i in range(0, len(textareal)):

            # Definition der Zeilenvariablen
            p1 = 0
            p2 = 0
            status = 0
            rangliste = ["Inhalt", ";"]
            history = []
            semikolonindex = 0
            j = 0
            error = 0
            schleifensprung = False

            # Kommentarzeilenüberprüfung
            for n in textareal[i]:
                if n == " ":
                    continue
                elif n == "#":
                    schleifensprung = True
                else:
                    break
            if schleifensprung:
                continue

            # Schleife, die den Index des Semikolons definiert
            for k in range(len(textareal[i]) - 1, -1, -1):
                if textareal[i][k] == ";":
                    semikolonindex = k
                    break

            # Schleife, die die Zeichen durchgeht
            while j < len(textareal[i]):

                # Überprüfung des ersten Zeichen des  ersten Nichtterminals
                if status == 0:
                    if textareal[i][j] != " " and textareal[i][j] != "=":
                        p1 = j
                        status = 1
                # Überprüfung des Endes des  ersten Nichtterminals
                if status == 1:
                    if textareal[i][j] == " ":
                        p2 = j
                        status = 2
                        if not wordcheck(textareal[i][p1:p2]):
                            status = 10
                            error = 1
                    elif textareal[i][j] == "=":
                        p2 = j
                        status = 20
                        if not wordcheck(textareal[i][p1:p2]):
                            status = 10
                            error = 1

                # Überprüfung des "="
                if status == 2:
                    if textareal[i][j] == "=":
                        status = 20
                    elif textareal[i][j] == " ":
                        j = j + 1
                        continue
                    else:
                        status = 10
                        error = 2

                # Überprüfung der Anführungszeichen
                if status == 20:
                    nAnfuerungs = 0
                    for l in range(0, len(textareal[i])):
                        if textareal[i][l] == '"':
                            nAnfuerungs = nAnfuerungs + 1
                    if nAnfuerungs % 2 == 0:
                        status = 3
                    else:
                        status = 10
                        error = 4

                # Überprüfung des Inhalts
                if status == 3:
                    # Überprüfung der Klammern
                    if textareal[i][j] == "(":
                        if rangliste[0] == "Inhalt":
                            rangliste.pop(0)
                            rangliste.insert(0, ")")
                            history.append("(")
                            rangliste.insert(0, "Inhalt")
                        else:
                            status = 10
                            error = 5
                    if textareal[i][j] == ")":
                        if rangliste[0] == ")":
                            rangliste.pop(0)
                            history.append(")")
                        else:
                            status = 10
                            error = 6

                    if textareal[i][j] == "{":
                        if rangliste[0] == "Inhalt":
                            rangliste.pop(0)
                            rangliste.insert(0, "}")
                            history.append("{")
                            rangliste.insert(0, "Inhalt")
                        else:
                            status = 10
                            error = 7
                    if textareal[i][j] == "}":
                        if rangliste[0] == "}":
                            rangliste.pop(0)
                            history.append("}")
                        else:
                            status = 10
                            error = 8

                    if textareal[i][j] == "[":
                        if rangliste[0] == "Inhalt":
                            rangliste.pop(0)
                            rangliste.insert(0, "]")
                            history.append("[")
                            rangliste.insert(0, "Inhalt")
                        else:
                            status = 10
                            error = 9
                    if textareal[i][j] == "]":
                        if rangliste[0] == "]":
                            rangliste.pop(0)
                            history.append("]")
                        else:
                            status = 10
                            error = 10

                    # Überprüfung der Terminale
                    if textareal[i][j] == '"':
                        status = 5
                        p1 = j
                        j = j + 1
                        continue

                    # Überprüfung der Nichtterminale
                    if wordcheck(textareal[i][j]):
                        if rangliste[0] == "Inhalt":
                            status = 4
                            p1 = j
                        else:
                            status = 10
                            error = 11

                    # Überprüfung der Konkationationen
                    if textareal[i][j] == ",":
                        if history[-1] == "Inhalt" or history[-1] == ")" or history[-1] == "}" or history[-1] == "]":
                            rangliste.insert(0, "Inhalt")
                            history.append(",")
                        else:
                            status = 10
                            error = 12

                    # Überprüfung der Oder-Zeichen
                    if textareal[i][j] == "|":
                        if history[-1] == "Inhalt" or history[-1] == ")" or history[-1] == "}" or history[-1] == "]":
                            rangliste.insert(0, "Inhalt")
                            history.append("|")
                        else:
                            status = 10
                            error = 13

                    # Überprüfung des Semikonlons
                    if rangliste == [";"] and textareal[i][j] == ";":
                        rangliste.pop(0)
                        history.append(";")
                        break

                    # Fehlermeldung bei fehlenden Zeichen
                    if rangliste != [";"] and textareal[i][j] == ";":
                        zeichennamen = {
                            ")": "Geschlossene Klammer",
                            "}": "Geschlossene Rekursionsklammer",
                            "]": "Geschlossene Optionalsklammer",
                            "Inhalt": "Ableitungsausdruck"
                        }
                        meldung = "Error in Zeile " + str(i + 1) + ": Folgende Zeichen/Ausdrücke werden noch erwartet: "
                        for m in range(0, len(rangliste) - 1):
                            meldung += zeichennamen[rangliste[m]]
                            if m <= len(rangliste) - 3:
                                meldung += ","
                        meldung += ". Fehler wurde bei Zeichen " + str(j) + " bemerkt"
                        print(meldung)
                        status = 10
                        break

                # Teil der Nichtterminalüberprüfung
                if status == 4:
                    if not wordcheck(textareal[i][j]):
                        status = 3
                        p2 = j
                        j = j - 1
                        if rangliste[0] == "Inhalt":
                            rangliste.pop(0)
                        else:
                            status = 10
                            error = 11
                        history.append("Inhalt")

                # Teil der Terminalüberprüfung
                if status == 5:
                    if textareal[i][j] == '"':
                        p2 = j
                        if rangliste[0] == "Inhalt":
                            rangliste.pop(0)
                            history.append("Inhalt")
                            status = 3
                        else:
                            status = 10
                            error = 16
                    elif textareal[i][j] != '"' and j > semikolonindex:
                        status = 10
                        error = 17

                # Fehlerausgabe
                if status == 10:
                    errordict = {
                        1: "Das abzuleitende Nichtterminal ist ungültig.",
                        2: "Das Ableitungszeichen (=) wurde nicht gefunden.",
                        4: "Es gab einen Fehler bei der Definition der Terminale.",
                        5: "Klammer wurde an falscher Stelle geöffnet.",
                        6: "Es wurde versucht eine Klammer zu schließen, obwohl diese nicht geöffnet wurde.",
                        7: "Rekursionsklammer wurde an falscher Stelle geöffnet.",
                        8: "Es wurde versucht eine Rekursionsklammer zu schließen, obwohl diese nicht geöffnet wurde.",
                        9: "Otionalsklammer wurde an falscher Stelle geöffnet.",
                        10: "Es wurde versucht eine Optionalsklammer zu schließen, obwohl diese nicht geöffnet wurde.",
                        11: "Unerwartetes Nichtterminal. Es könnte eine Konkatination fehlen.",
                        12: "Es wurde eine unerwartete Konkatination gefunden.",
                        13: "Es wurde ein unerwartetes Oderzeichen gefunden.",
                        14: "Ein Nichtterminal enthält ein ungültiges Zeichen.",
                        16: "Unerwartetes Terminal. Es könnte eine Konkatination fehlen.",
                        17: "Erwartetes Semikolon wurde nicht gefunden.",
                    }
                    print("Error in Zeile", i, ": ", errordict[error], "(Fehler bei Zeichen", j, "bemerkt.)")
                    break

                j = j + 1  # Erhöhung der Schleifenvariable

            # Überprüfung des Fehlerstandes
            if status == 10:
                errorstatus = False

        return errorstatus

    def grammatikbuilder(self, grammartext):
        for line in grammartext:
            pointerleft = 0
            pointerright = 0
            ntname = ''
            Abltext = ''
            for index in range(0, len(line)):
                if line[index] != ' ':
                    pointerleft = index
                    break
                else:
                    continue
            for index in range(pointerleft, len(line)):
                if line[index] == ' ' or line[index] == '=':
                    pointerright = index
                    break
                else:
                    continue
            ntname = line[pointerleft:pointerright]
            for index in range(pointerright, len(line)):
                if line[index] == '=':
                    pointerleft = index+1
                    break
                else:
                    continue
            for index in range(len(line)-1, 0, -1):
                if line[index] == ';':
                    pointerright = index
                    break
            Abltext = line[pointerleft:pointerright]

            self.nichtterminalarray.append(Nonterminal(ntname, Abltext))

    def uglyoverwrite(self, indexlist, obj, array, poping=False):
        if not indexlist:
            array = obj
        else:
            indexstr = ''
            if poping:
                for i in range(len(indexlist)-1):
                    indexstr += '[' + str(indexlist[i]) + ']'
                exec('array' + indexstr + '.pop(indexlist[-1])')
            else:
                for i in indexlist:
                    indexstr += '[' + str(i) + ']'
                exec('array' + indexstr + ' = obj')

    def uglypull(self, indexlist, array):
        if not indexlist:
            return array
        indexstr = ''
        for i in indexlist:
            indexstr += '[' + str(i) + ']'
        exec('self.ugly = array' + indexstr)
        return self.ugly

    def branchconnect(self):
        self.tree = [self.nichtterminalarray[0]]

        def reboy(section, origin=[], path=[0]):
            if isinstance(section, list):
                personal_origin = origin[:]
                personal_origin.append(None)
                i = 0
                end = len(section)
                while i < end:
                    personal_path = path[:]
                    personal_path.append(i)
                    if self.uglypull(personal_path, self.tree) in origin:
                        pointer = None
                        for j in range(len(origin)):
                            if self.uglypull(personal_path, self.tree) == origin[j]:
                                pointer = j
                                break
                        self.uglyoverwrite(personal_path, Recurse(personal_path[0:pointer + 1]), self.tree)
                    elif isinstance(self.uglypull(personal_path, self.tree), Recgroup):
                        hold_path = personal_path[:]
                        hold_path[-1] += 1
                        personal_origin.append(None)
                        self.uglyoverwrite(personal_path, [Orgroup, [Terminal(""), self.uglypull(hold_path, self.tree), Recurse(personal_path)]], self.tree)
                        personal_path.append(1)
                        personal_path.append(1)
                        reboy(self.uglypull(personal_path, self.tree), personal_origin, personal_path)
                        self.uglyoverwrite(hold_path, None, self.tree, True)
                        end -= 1
                    else:
                        reboy(self.uglypull(personal_path, self.tree), personal_origin, personal_path)
                    i += 1
            elif isinstance(section, Nonterminal):
                personal_origin = origin[:]
                personal_origin.append(section)
                self.uglyoverwrite(path, section.absableitung, self.tree)
                i = 0
                end = len(self.uglypull(path, self.tree))
                while i < end:
                    personal_path = path[:]
                    personal_path.append(i)
                    if self.uglypull(personal_path, self.tree) in origin:
                        pointer = None
                        for j in range(len(origin)):
                            if self.uglypull(personal_path, self.tree) == origin[j]:
                                pointer = j
                                break
                        self.uglyoverwrite(personal_path, Recurse(personal_path[0:pointer + 1]), self.tree)
                    elif isinstance(self.uglypull(personal_path, self.tree), Recgroup):
                        hold_path = personal_path[:]
                        hold_path[-1] += 1
                        personal_origin.append(None)
                        self.uglyoverwrite(personal_path, [Orgroup, [Terminal(""), self.uglypull(hold_path, self.tree), Recurse(personal_path)]], self.tree)
                        personal_path.append(1)
                        personal_path.append(1)
                        reboy(self.uglypull(personal_path, self.tree), personal_origin, personal_path)
                        self.uglyoverwrite(hold_path, None, self.tree, True)
                        end -= 1
                    else:
                        reboy(self.uglypull(personal_path, self.tree), personal_origin, personal_path)
                    i += 1
        reboy(self.tree[0])

    def literalcheck(self):
        coverage = []
        for i in range(len(self.word)):
            coverage.append(False)
        def alternate_reality(versionofcoverage, index=0):
            new_versionofcoverage = versionofcoverage[:]
            for j in range(index, len(self.word)):
                for k in range(j+1, len(self.word)+1):
                    if self.word[j:k] in self.terminalalphabet:
                        for l in range(j, k):
                            new_versionofcoverage[l] = True
                        if False in new_versionofcoverage:
                            alternate_reality(new_versionofcoverage, k)
                        else:
                            self.passed = True
                            return True
                if j == len(self.word) - 1 and not self.passed:
                    return False
        alternate_reality(coverage)


grammarcheck1 = Ebnfpruefer()

