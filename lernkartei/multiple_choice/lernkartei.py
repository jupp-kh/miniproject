
import csv 
import random
try:
    import matplotlib.pyplot as plt
except Exception:
    print("Installieren Sie die Bibliothek matplotlib, um fortzufahren!")


# global variable 
line = "______________________________________________" 
# class zu erstellen jedes card als opject 
class kartei:   

    def __init__(self,frage,antworten, richtig, kastenummer):
        self.frage = frage
        self.richtig = richtig 
        self.antworten = antworten 
        self.kastenummer = kastenummer 

# Funktion zu erstellen von kartie datei als objekte 
# return wert ist eine liste von karteien  
def erstellkarteien():
    with open('Lernkarteien.csv','r',encoding = 'utf-8') as file:
        next(file)
        cards = []
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            cards.append(kartei(row[0],row[1],row[2],row[3])) 
    file.close()
    return cards

#Funktion zu evaluieren die antwort
#paramieter: antwort -> gewälte antwort, richtig 
#                    -> richtige gespeichert antwort in kastencards
#return wert : evaluation Ergebniss 
def  pruefantwort(antworten,eingabe, richtig):
    if(int(richtig) == eingabe):
        print("Richtig!")
        return True 
    print("Falsche, die richtige antwort ist: "+ antworten[int(richtig)- 1])
    return False 

# Funktion zu zahlen wie viele fragen in jedem kaste sind 
# parameter: list von kartie 
# return wert : liste größe 5 in der stehten die zahelen 
def kasten(cards):
    kastenummer = []
    for card in cards: 
        kastenummer.append(int(card.kastenummer)) 
    temp=set(kastenummer)
    zaeler=[0,0,0,0,0]
    for i in temp:
        zaeler[i]=kastenummer.count(i)
    return zaeler

# Funktion zu abfrgae welche kaste will der Benutzer lernen 
# parameter: list von card 
# return wert: gewählte Kastennummer 
def wahlkasten(cards):
    kasten_stand = kasten(cards)
    print("Aktuelle Kasten Stand: ")
    for i in range(0,5):
        print(str(i+1) + " -> " + str(kasten_stand[i]))

    eingabe = int(input("im welchen kasten wollen sie lernen? "))
    while (eingabe not in range(1,6) or kasten_stand[eingabe-1] == 0):
        eingabe = int(input("falscher kaste! wählen sie ein andere kaste?"))
    return eingabe

# Funktion zu filter die cards in bestimmten kaste 
# parameter : eingabe -> gewählte kastenummer,
#             cards -> komplete list von kartei
# returen wert : kartei in die gewälten kaste 
def kasten_cards(eingabe , cards):
    kastencards = []
    for card in cards: 
        if(int(card.kastenummer) == eingabe - 1 ):
            kastencards.append(card)
    return kastencards

# Funktion zu suchen vor the index from schon bearbeitet frage
# paramete : cards -> list vom cards
#            frage -> schon gestellte frage 
# returen wert : index der bearbeitete card
def card_index(cards, frage):  
    for index in range(0,len(cards)):
        if (cards[index].frage == frage):
            return index

# Funktion zu get input and pruf it auf richtigkeit
# parameter : x -> anzahl der moglischen antwortern 
# return wert : zahl im rang von (1 - x)
def getinput(x):
    try:
        eingabe = int(input("Geben sie die Antwortnummer: "))
    except Exception:
        print("falsche eingabe versuchen sie erneut")
        print(line)
        eingabe = getinput(x)
    if(eingabe not in range (1, x+1)):
        print("falsche eingabe versuchen sie erneut")
        eingabe = getinput(x)
    return eingabe


# Funktion zu erstellen von fragen und evaluier die antworten 
# parameter : kasten_cards -> cards im konkerten kasten
#             cards -> orginal cards zu modifizier die kastennummer
# return wert : tracker -> liste fon [gestelten fragen, richtig, falsch]
#               cards -> modifiziert cards  
def sitzung(kasten_cards,cards, tracker):
    
    while (1):
        tracker[0] += 1 
        zufallindex = random.randint(0,len(kasten_cards)-1)
        print(kasten_cards[zufallindex].frage)
        antworten  = kasten_cards[zufallindex].antworten.split(" | ")
        i = 1
        for antwort in antworten:
            print(str(i) +") "+ antwort)
            i += 1
        print(line)
        eingabe = getinput(len(antworten))
        evaluation = pruefantwort(antworten,eingabe, 
        	kasten_cards[zufallindex].richtig)
        cardindex = card_index(cards, kasten_cards[zufallindex].frage)
        if(evaluation):
            tracker[1] += 1
            if (int(cards[cardindex].kastenummer) < 4 ):
                cards[cardindex].kastenummer= 1+int(cards[cardindex].kastenummer)
        else: 
            tracker[2] += 1
            cards[cardindex].kastenummer = 0
        del(kasten_cards[zufallindex])
        print(line)
        endsitzung = input ("Enter drücken : weiterlernen \t  N : beenden \n")
        if(endsitzung.lower() == 'n' or not kasten_cards ):
            break
        

    return cards, tracker    

# Funktion zu save die modifizierte kasten nummeren
# parameter : cards -> modifiziert cards nach dem leran sitzung 
def save_modifidedcards(cards): 
    with open('Lernkarteien.csv','w', newline='',encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Frage', 'Antworten' ,'richtig', 'kastenummer'])
        for card in cards:
            writer.writerow([card.frage, card.antworten, card.richtig, 
            	card.kastenummer])
    file.close()     


# Funktion zu zeichen die sitzungergebniss als 
# kuchendiagram für kasten stand und balkendiagram für bearbeitete fragen
def sitzunggraph(cards,tracker):
    label1 = ['kaste 1','kaste 2','kaste 3','kaste 4','kaste 5']
    label2 = ['bearbeitet', 'richtig', 'falsch']
    color2 = ['gray', 'green','red']
    data = kasten(cards)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Sitzung Ergebniss')
    ax1.pie(data, shadow = True, startangle = 140, autopct=
    	lambda p : ('{:,.0f}'.format(p * sum(data)/100)) if p != 0  else None)
    ax1.legend(label1,bbox_to_anchor= (-0.25,0.75),loc = "lower left")
    ax2.bar([0,1,2],tick_label = label2, color = color2, height= tracker)
    plt.show()

# Funktion zu speichen von heutigen sizung ergebniss 
# parameter : tracker -> list von zaheln [bearbeitet, richtig, falsche] 
def save_sitzungergibniss(tracker):
        with open('sitzungergebniss.csv','a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tracker)
        file.close()

# Funktion zu erstellen von graph, der die lernerfolg pro versuch darstellt    
def versuche_graph():
    with open('sitzungergebniss.csv','r',encoding = 'utf-8') as file:
        data_richtig =[]
        data_falsch = []
        csv_reader =list(csv.reader(file, delimiter=','))
        x = range(1, len(csv_reader)+1)
        for row in csv_reader:
            data_richtig.append(int(row[1]))
            data_falsch.append(int(row[2]))
        file.close
    p1 = plt.bar(x,height = data_richtig,color= 'green')
    p2 = plt.bar(x, height = data_falsch,
             bottom=data_richtig,color= 'red')
    plt.ylabel('bearbeitete Fragen')
    plt.xlabel('versuchs')
    plt.title('Lernerfolg pro versuch ')
    plt.legend((p1[0], p2[0]), ('richtig', 'falsch'))
    plt.show()

def run():
    print("\nDies Program ahmt die funktion einer lernkarteien app nach")
    print("Die Fragen sind in 5 kasten eingeordnet")
    print(line)
    cards = erstellkarteien()
    eingabe = wahlkasten(cards)
    kastencards = kasten_cards(eingabe, cards)
    modifiycards, tracker = sitzung(kastencards,cards,[0,0,0])
    save_modifidedcards(modifiycards) 
    sitzunggraph(modifiycards,tracker)
    save_sitzungergibniss(tracker)
    showgraph = input("Wollen sie ein graphische Darstellung für " 
    	"ihre lernsitzungen Y/N?")
    if (showgraph.lower()  != 'n' ):
        versuche_graph()

run()