#Name:
#Matrikelnummer:
import webbrowser as wb
import math
from math import degrees, radians, atan2
from geodist import geodist
import csv
try:
    import matplotlib.pyplot as plt
except ImportError:
   (input("Auf diesem Rechner fehlt die Bibliothek 'matplotlib'!"))
line = "----------------------------------------------------------\n"
def read_csv(csv_file):
    """	
    funktion zu lesen von die csv Datei
    und gibt die date in form list Züruck
    """ 
    with open(csv_file,'r',encoding="utf-8") as csv_data:
        data = []
        next(csv_data)
        reader = list(csv.reader(csv_data, delimiter='\t'))
        for row in reader:
            data.append(row) 
    csv_data.close()
    return data
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
#https://stackoverflow.com/questions/17411940/matplotlib-scatter-plot-legend
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
def graph(sieben_brucken,geokoord):
    """
    Die Funktion erzeugt ein graph für die sieben nächstleigende Brücken
    erhalt eine list in dem finden die sieben Brücken und die eingegeben Geokoordinatpaar 
    """
    colors = ['b', 'c', 'y', 'm', 'r','g','k']
    name = []
    g = []
    # erstehlen dei Brücken punktweise(x,y) anhand die Breiten- und Längengrad
    # addiere zu jede punkt eine unterschidliche farbe 
    # speichere die name der brücken in list namen  
    for i, bruecke in enumerate(sieben_brucken):
        nb = bruecke[10]
        ol = bruecke[11]
        g.append(plt.scatter(nb,ol,marker='o',color= colors[i]))
        name.append(bruecke[2])
    g.append(plt.scatter(geokoord[0],geokoord[1],marker = 'x',color = 'lime'))
    name.append('location')
    plt.legend(g,
            name,
            loc= 0,
           fontsize=8)
    plt.title("Sieben Brücken")
    plt.ylabel("Östliche Länge")
    plt.xlabel("Nördliche Breite")
    plt.grid()
    plt.show()
    

def webbrowser(url):
    """funktion zu offenen von die nächstliegende Brücke in webbrowser"""
    wb.open(url,new=1,autoraise=True)

def bewertung(sieben_bruecken):
    """funktion zu Beschreibung die zustand der Brücken in wörter"""
    for bruecke in sieben_bruecken:
        zn = float(bruecke[6].replace(",","."))
        if zn <=  1.4: 
            bruecke.append("sehr guter Zustand")
            continue
        if zn <= 1.9: 
            bruecke.append("guter Zustand")
            continue
        if zn <= 2.4: 
            bruecke.append("befriedigender Zustand")
            continue
        if zn <= 2.9:
            bruecke.append("ausreichender Zustand")
            continue
        if zn <= 3.4: 
            bruecke.append("nicht ausreichender Zustand")
            continue 
        if zn <= 4.0:
            bruecke.append("ungenügender Zustand")
        bruecke.append("Brücke hat keine Bewertung")


def ergebnis(sieben_brucken):
    """Funktion gibt die informationen über die nächstliegende Brücken"""
    #https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    for i, bruecke in enumerate(sieben_brucken):
        print("Rang: "+str(i+1))
        print(f"Entfernung: {bruecke[13]:.2f} km")
        print("Name: "+ bruecke[2])
        print("Ort: "+ bruecke[3])
        print("Zustandnote: "+ bruecke[6])
        print("Bewertung: "+ bruecke[14])
        print("Geokoordinate: " '{:.5f}'.format(bruecke[10]),",",'{:.5f}'.format(bruecke[11]) )
        print(f"Himmelrichtung: {bruecke[15]:.0f} ° der brücke befindet sich in Richtun "+bruecke[16])
        print("Link: "+ bruecke[12])
        print(line)
#https://www.matheboard.de/archive/591020/thread.html


def peilwinkel(ps,pz):
    """Funktion zu berechnen von peilwinkel für die sieben Brücken von gegeben geokoordinatpaar"""
    lons, lats = map(radians,ps)
    lonz, latz = map(radians,pz)
    dlon = lonz - lons
    dlat = latz - lats
    winkel = atan2(dlon,dlat)
    winkel = degrees(winkel)
    if (winkel < 0):
        winkel+= 360
    
    return winkel

#https://rechneronline.de/geo-koordinaten/himmelsrichtungen.php
def himmelrichtung(sieben_bruecken,ps):
    """Funktion zu Berechnug die winkel der sieben Brücken und umwandel die in Hemmelrichtung  """
    for bruecke in sieben_bruecken:
        nb = bruecke[10]
        ol = bruecke[11]
        geokood = nb,ol
        winkel = round(peilwinkel(ps,geokood),1)
        bruecke.append(winkel)
        if winkel < 10:
            bruecke.append("Norden")
            continue
        if winkel < 80:
            bruecke.append("Nordost")
            continue
        if winkel < 100:
            bruecke.append("Osten")
            continue
        if winkel < 170:
            bruecke.append("Südost")
            continue
        if winkel < 190:
            bruecke.append("Süden")
            continue
        if winkel < 260:
            bruecke.append("Südwest")
            continue
        if winkel < 280:
            bruecke.append("Westen")
            continue
        if winkel < 350:
            bruecke.append("Nordwest")
            continue
        bruecke.append("Norden")

def begruessung():
    """begrüßung wird in funktion geschriebn to refaktor main Funktion"""
    print("Diese Programm ermittelt zu einem Geokoordinatenpaar innerhalb\n"
    "Deutschland. (z.B. 51.83743, 7.34073) die sieben nächstliegenden\n"
    "Fernstraßenbrücken und gibt ihre Position, ihren Zustand und einen\n"
    "Link auf ein onlinekarte aus.")
    print(line)


def get_option():
    """Funktion zu erfragen die Nuzter für optionale Funktionalität  """
    try:
        option = int(input("wälen sie aus die folgende optionen\n "
        +line+
        "0 - Programm schließen\n"
        "1 - offen Webbrowser für die nähreste Brücke\n"
        "2 - Grafische Darstellung der sieben Brücken\n"
        "3 - option 1 + 2\n"
        ))
    except ValueError:
        option = int(input("opps! sie haben keine zahl gegeben, versuchen sie erneut:"))    
    return option

def get_geokoordpaar():
    """Funktion zu erfragen die Nuzer über die geokoordinatenpaar"""
    #https://docs.python.org/3/tutorial/errors.html
    try:
        eingab = input("geben sie ein Geokoordinatenpar ein:").split(",")
        print(line)
        eingab_geokoord = float(eingab[0]), float(eingab[1])
    except ValueError:
        eingab = input("Ihre eingabe muss in Form: 51.83743, 7.34073 \n"
        "Geben Sei eine gültige Eingabe ").split(",")
        print(line)
        eingab_geokoord = float(eingab[0]), float(eingab[1])
    return eingab_geokoord

def main():
    begruessung()
    eingab_geokoord = get_geokoordpaar()
    bruecken = read_csv("data.csv")
    # laufen durch alle Brücken und berechnen die abstand zu eingegebene geokoordinatenpaar 
    # danach wird die abstand zu Jeden frücke eingefügt
    for bruecke in bruecken:
        nb = float(bruecke[10].replace(",","."))
        ol = float(bruecke[11].replace(",","."))
        bruecke[10] = nb
        bruecke[11] = ol
        geokoord = nb , ol
        abstand = geodist(geokoord,eingab_geokoord)
        bruecke.append(abstand)
#https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list
    # sortieen die datei anhand die Abstand zu den gegeben eokoordinaten 
    bruecken.sort(key=lambda x: x[13])
    # speichere die erste 7 element in brücken mit den minmalen Abstand zu den geokoordiantenpaar
    sieben_bruecken = bruecken[:7] 
    bewertung(sieben_bruecken)
    himmelrichtung(sieben_bruecken,eingab_geokoord)
    ergebnis(sieben_bruecken)
    option = get_option() 
    if option != 0:
        if option == 1 or option == 3: 
            webbrowser(sieben_bruecken[0][12])
        if option  > 1:
            graph(sieben_bruecken,eingab_geokoord)
            

if __name__=="__main__":
    main()