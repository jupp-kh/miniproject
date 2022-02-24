
import csv
import random
import matplotlib.pyplot as plt



class Card:   
    """ Die Klasse Card speichert die Daten der CSV Datei 
    	Für jeweils ein Card gibt es 3 Werte
    	frage: enthält die Frage der Karte
    	antwort: enthält die richtige Antwort der Frage
    	fachnummer: gibt an, in welcher Fach die Frage steht
    """
    def __init__(self,frage, antwort, fachnummer):
        self.frage = frage
        self.antwort = antwort 
        self.fachnummer = fachnummer 


def cards(csv_file):
    """	Die Funktion cards initialisiert die Liste der Karteikarten
    	Erst wird von der CSV Datei "Data" gelesen und dies dann in einer passen-
    	der Datenstruktur "Card" gespeichert
    	Die Funktion bekommt als Parameter ein Datei csv_file 
    """ 
    kartei = []
    next(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        kartei.append(Card(row[0],row[1],row[2])) 
    return list(kartei)



def aktuellestand(lernkartei):
    """ 
        Gibt die Anzahl der Fragen in jeweils einen Fachnummer
    """
    counter = [0,0,0,0,0] 
    for x in lernkartei:
    	# finde Fachnummer und inkrementiere 
        counter[int(x.fachnummer)] += 1   
    return counter 




def getindex(frage,lernkartei): 
    """ liefert die Index der gegebenen Parameter Frage in die 
    	csv Datei
    """
    for x in range(0,len(lernkartei)): 
        if lernkartei[x].frage == frage:   
            return int(x)




def update_csv(lernkartei):
    """ Nach Änderungen im Fachnummer der Karten sollten 
    	die auch in der CSV Datei geändert
    """
    with open('Data.csv','w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Frage', 'Antwort' , 'Fachnummer'])
        for i in range(0, len(lernkartei)):
            writer.writerow([lernkartei[i].frage, lernkartei[i].antwort,
             lernkartei[i].fachnummer])
    csv_file.close()
    
    

    
def lernerfolg( lernkartei, counter):
    """ Beim Aufruf wird der Lernerfolg des Benutzers 
    	in der aktuellen Lernsitzung grafisch dargestellt.
    """
    labels = ['gestellt', 'richtig', 'falsche', 'fach 1',
    						'fach 2','fach 3','fach 4','fach 5']
    sizes = [counter[0], counter[1],counter[2]]+ aktuellestand(lernkartei)
    colors = ['gray','green', 'red', 'blue','blue','blue','blue','blue']
    plt.barh(labels, sizes, color = colors, edgecolor = 'black')
    plt.title("Heutigen Lernerfolg")
    plt.show()



# die Funktion LCS ist von geeksforgeeks importiert.
# dies berechnet der längste gemeinsame Teilsequenz
def lcs(X, Y): 
    # find the length of the strings 
    m = len(X) 
    n = len(Y) 
  
    # declaring the array for storing the dp values 
    L = [[None]*(n + 1) for i in range(m + 1)] 
  
    """Following steps build L[m + 1][n + 1] in bottom up fashion 
    Note: L[i][j] contains length of LCS of X[0..i-1] 
    and Y[0..j-1]"""
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 
  
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
    return L[m][n] 


def pruefantwort(eingabe, antwort):
    """
    	Die Funktion wird verwendet, um die Eingabe des Benutzers zu 
    	kontrollieren.
        * eingabe ist die vom Benutzer eingegebene Zeichenkette.
        * answer ist die richtige Antwort auf die gestellte Frage 
    """
    modeingabe = eingabe.replace(" ","").lower()
    modantwort = antwort.replace(" ","").lower()
 	# wir nehmen keine Rücksicht auf die leeren Zeichen
    if(lcs(modantwort,modeingabe) >= len(modantwort)-2):
        return True
    # hiermit dürfen dann maximal ein Fehler gemacht werden. 
    # der longest common subsequence darf um 1 Zeichen von der antwort abweichen.
    return False



def  zeitlicher_erfolg(counter):
    """ Gibt das Erfolg über die Zeit an.
    	Dies wird mithilfe Matplotlib dargestellt.
    """
    with open('erfolg.csv','a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(counter)
    csv_file.close()
    # Daten in Datei erfolg.csv werden zur Nachverfolgung des Erfolgs verwendet
    with open('erfolg.csv') as csv_file:
        next(csv_file)
        reader = list(csv.reader(csv_file, delimiter=','))
        richtig = []
        falsch = []
        versuchs = len(reader)+ 1
        # zähle richtig bwz. falsch beantwortete Fragen
        for row in reader:
            richtig.append(int(row[1]))
            falsch.append(int (row[2]))
        plt.xlabel('Versuchsnummer')
        plt.ylabel('Fragen')
        plt.plot(range(1,versuchs),richtig, 'g')
        plt.plot(range(1,versuchs),falsch, 'r')
        plt.legend(['Richtig','Falsch'])
        plt.title("Lernerfolg über Zeit")
        plt.show()

def getfach(faecher):
    try:
        fach = int(input("welches fach wollen sie lernen? "))
        while (fach not in range(1,6) or faecher[fach-1] == 0):
           fach =int  (input("Falsche eingabe versuchen sie erneut: "))
        return fach 
    except:
        print("Error! Bitte eine Ziffer geben!")
        return getfach(faecher)

# frage ob der Nutzer weiterlernen möchte
def weiterlernen(lernkartei,counter):
    weiter = input("wollen sie weiter lernen Y/N?")
    if (weiter.lower() == 'n'):
        update_csv(lernkartei)
        lernerfolg(lernkartei, counter)
        darstellung = input("Wollen sie eine Grafische" + 
                    "Darstellung ihres Lernerfolgs über die Zeit Y/N?")
        if (darstellung.lower() == 'y'):
            zeitlicher_erfolg(counter)
        return True
    return False


# unserer Hauptprogramm wird mithilfe lern() aufgerufen
def lern():
    with open('Data.csv','r') as csv_file:
        # lernkarteien erstellen 
        lernkartei = cards(csv_file)
    csv_file.close()

    # speichere der aktuelle Zustand aller Fragen 
    # bzw. in welchem Fach sie sich befinden
    faecher = aktuellestand(lernkartei)
    for x in range(1,6):
        print("In Fach " + str(x)+ " sind " + str(faecher[x-1])+ " Fragen." )

    # starte den Lernprozess
    run_learning([0,0,0], getfach(faecher), lernkartei)




def run_learning(counter, fach, lernkartei):
    # Nach Eingabe der gewünschter Lernfach speichere die Liste aller Fragen 
    lernfach =  list(filter(lambda x : int (x.fachnummer) == fach-1 , 
    	lernkartei ))
    # ab hier wird gelernt
    while(True):
        counter[0] += 1
        
        # generiere ein Zufallsummer, um eine Frage auszuwählen.
        zufallnummer = random.randint(0,len(lernfach)-1)
        antwort = input(lernfach[zufallnummer].frage +" ")
        
        # liefere den Index zur Frage
        index = getindex(lernfach[zufallnummer].frage, lernkartei)
        if (pruefantwort(antwort,lernfach[zufallnummer].antwort) ):
            counter[1] += 1
            if(int(lernkartei[index].fachnummer) < 4):
                lernkartei[index].fachnummer= 1+int(lernkartei[index].fachnummer)
            print("Richtig!: "+ str(lernfach[zufallnummer].antwort) )
            del (lernfach[zufallnummer]) 
        else: 
            counter[2] += 1
            print("Falsch! Richtige wäre: "+ str(lernfach[zufallnummer].antwort))
            if lernfach[zufallnummer].fachnummer  != 0:
                del(lernfach[zufallnummer])
            lernkartei[index].fachnummer = 0

        # frage ob der Nutzer weiterlernen möchte
        if(weiterlernen(lernkartei,counter)):
            break
        # wenn das Fach leer ist, wähle ein neues aus
        if(not lernfach):
            print("Sie haben alle lernkartei in diesem" +
            			"Fach bearbeitet, wählen sie ein neues Fach aus ?")
            lernerfolg(lernkartei, counter)
            neufach = getfach(aktuellestand(lernkartei))
            run_learning(counter, neufach, lernkartei)
            break

print("Die folgende Zeilen geben an wie viele Fragen " +
             "in der Datenbank gespeichert sind")
print("Die Fragen sind in 5 Kasten/Faecher aufgeteilt.")
lern()