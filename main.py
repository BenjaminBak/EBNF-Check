# Opening/Reading a text file content
# Test 123
# Test 456
ntcharlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
                    'F',
                    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    "-",
                    "_"]


class Orgroup:
    pass
class Recgroup:
    pass
class Optgroup:
    pass


class Nichtterminal:
    def __init__(self, name, ableitung):
        self.name = name
        self.ableitungtxt = ableitung
        self.absableitung = []
    def Updatetoabs(self, ableitungstxt, nichtterminalarray):
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
            elif status == 1 and self.ableitungtxt[i+1] not in ntcharlist:
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
                raw.append(self.ableitungtxt[l:r])
                if self.ableitungtxt[l:r] not in terminale:
                    terminale.append(self.ableitungtxt[l:r])

        self.absableitung = self.absbuilder(raw)

        return terminale

    def absbuilder(self, raw):
        absableitung = []
        j = 0
        while j < len(raw):
            if isinstance(raw[j], Nichtterminal):
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
                absableitung.append(self.absbuilder(raw2))
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
                absableitung.append(self.absbuilder(raw2))
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
                absableitung.append(Optgroup())
                absableitung.append(self.absbuilder(raw2))
                j = end
            elif isinstance(raw[j], str):
                absableitung.append(raw[j])

            j += 1
        return absableitung



class Ebnfpruefer:

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
                else:
                    continue
            Abltext = line[pointerleft:pointerright]

            self.nichtterminalarray.append(Nichtterminal(ntname, Abltext))

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
            terminale = nt.Updatetoabs(nt.ableitungtxt, self.nichtterminalarray)
            print(nt.absableitung)
            for t in terminale:
                if t not in self.terminalalphabet:
                    self.terminalalphabet.append(t)


grammarcheck1 = Ebnfpruefer()

