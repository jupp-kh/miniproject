"""
Name:
Matrikelnummer:
"""

# Notwendige Bibliotiken

from geodist import geodist

# wenn nich installiert, informiert die benutzer die matplotlib zuinstallieren
# und schließ das programm ab
# https://docs.python.org/3/tutorial/errors.html
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Die Bibliothek matplotlib fehlt! Bitte installieren Sie sie")
    exit()


def csv_lesen(csv_file):
    """
    diese funktion liest die csv Datei und gibt die date im form Wörterbuch Züruck
    wir lesen die Datei Zeile für Zeile und schreiben die verwendeten Informationen in das Wörterbuch,
    außerdem werden die mit einem Komma gespeicherten Werte mit einem Punkt getauscht
    und am Ende schreiben wir die Werte numerisch zur weiteren Berechnung
    """
    # das worterbuch
    data = {"ol": [], "nb": [], "zn": [], "oben": [], "unten": []}

    with open(csv_file, "r", encoding="utf-8") as csv_data:
        # skip the header
        next(csv_data)
        for zeile in csv_data:
            row = zeile.split("\t")
            # replace tauscht kommer mit punkt und float macht den wert numerisch
            ol = float(row[11].replace(",", "."))
            nb = float(row[10].replace(",", "."))
            if ol > 0 and nb > 0:
                data["ol"].append(ol)
                data["nb"].append(nb)
                data["zn"].append(float(row[6].replace(",", ".")))
                # strip wandelt die daten von dem form ['"aa"',...] -> ['a',...] damit die vergleichbar später sind
                data["oben"].append(row[4].strip('"'))
                data["unten"].append(row[5].strip('"'))
    csv_data.close()
    return data


def karte_lesen(txt_file):
    """
    Diese Funktion dient zum Laden der Geokorrdinate der Grenzen Deutschlands
    """
    data = []
    with open(txt_file, "r", encoding="utf-8") as txt_data:
        for zeile in txt_data:
            # strip loescht die linebrecher \n
            row = zeile.strip().split("\t")
            data.append([float(row[0]), float(row[1])])
    txt_data.close()
    return data


def graph(data, karte):
    """
    Diese funktion dient zum darstellung der daten
    data: die gewünschten brücken
    karte: die Geokorrdinate der Grenzen Deutschlands
    """
    try:
        # Geokoordinaten aus der Liste in zwei Listen packen
        # https://www.programiz.com/python-programming/methods/built-in/zip
        # [[ol,nb],[ol,nb],....] -> [ol1,ol2,...] , [nb1,nb2,...]
        x, y = zip(*karte)
        plt.plot(x, y)
    except ValueError:
        print("Geokoordinaten sind nicht vorhand ")

    # unpack die data in drei listen
    x, y, zustand_note = zip(*data)

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
    plt.scatter(x, y, c=list(map(get_farbe, zustand_note)))
    plt.show()


def filter_nach_zn(data, zn):
    """
    Diese funktion schaut nach welche brueken haben den gleichen eingegeben zustandnote
    """

    data_zn = []
    for i, zustand in enumerate(data["zn"]):
        if zustand == zn:
            data_zn.append([data["ol"][i], data["nb"][i], data["zn"][i]])
    return data_zn


def filter_nach_Geokoord(data, p1, umkreis):
    """
    Diese funktion schaut nach welche brueken
    liegen im ein bestimmten umkreis um einen beliebten geokoordinaten
    sei berechnet den Abstand mittles geodist und speicert die im kreis ligende bruecken
    """
    umkreis_bruecken = []
    for i, p2 in enumerate(zip(data["nb"], data["ol"])):
        if geodist(p1, p2) <= umkreis:
            umkreis_bruecken.append([data["ol"][i], data["nb"][i], data["zn"][i]])
    return umkreis_bruecken


def filter_nach_str(data, strasse):
    """
    Diese funktion schaut nach welche brueken liegen auf einem bestimmten strasse
    sie wergleicht ob der brücke ueber oder unter der eingegeben Strasse
    """
    str_bruecken = []
    for i, s in enumerate(zip(data["oben"], data["unten"])):
        if s[0] == strasse or s[1] == strasse:
            str_bruecken.append([data["ol"][i], data["nb"][i], data["zn"][i]])
    return str_bruecken


def farben():
    """
    Dieser funktion erstellt ein dictionary mit key: die zustandnote
    und value das farbe in form RGB hex color
    """
    # https://stackoverflow.com/questions/2974022
    # https://matplotlib.org/stable/tutorials/colors/colors.html
    colors = {}
    for i in range(10, 41):
        # https://stackoverflow.com/questions/19986662/
        x = round(i * 0.1, 1)
        # gruen
        if x <= 1.4:
            colors[x] = "#008000"
        # gelbgruen
        elif x <= 1.9:
            colors[x] = "#00FF00"
        # gelb
        elif x <= 2.4:
            colors[x] = "#FFFF00"
        # orange
        elif x <= 2.9:
            colors[x] = "#FFA500"
        # orangrot
        elif x <= 3.4:
            colors[x] = "#FF4500"
        # rot
        else:
            colors[x] = "#FF0000"
    return colors


def zustand_tostring(zn):
    """
    funktion zum beschreiben die zustand wörtlich
    """
    if zn <= 1.4:
        return "sehr guter Zustand"
    elif zn <= 1.9:
        return "guter Zustand"
    elif zn <= 2.4:
        return "befriedigender Zustand"
    elif zn <= 2.9:
        return "ausreichender Zustand"
    elif zn <= 3.4:
        return "nicht ausreichender Zustand"
    else:
        return "ungenügender Zustand"


def nach_zustandnote(data, grenzen):
    """
    In dem funktion wird der buntzer um die benötigten info gefragt damit die berechnung begint
    außer dem wird Falsche Eingaben abgefangen. es wird auch die daten vorbereitet und zum
    darstllen weitergegeben
    """
    try:
        zn = float(input("Geben sie einen Zustandnote in form 2.4: "))
        if zn >= 1 and zn <= 4:
            data = filter_nach_zn(data, zn)
            plt.title(
                "Karte der {zahl} deutschen Fernstraßenbrücken \n mit der zustandnote {zn} ({zn_str})".format(
                    zahl=len(data), zn=zn, zn_str=zustand_tostring(zn)
                )
            )
            graph(data, grenzen)
        else:
            print("Falshe Eingabe! Zustandnote muss in dem bereich 1 - 4")
    except ValueError:
        print("Falshe Eingabe! Zustandnote muss ein zahl sein")


def nach_umkreis(data, grenzen):
    """
    in dem funktion wird der buntzer um die benötigten info gefragt damit die berechnung begint
    außer dem wird Falsche Eingaben abgefangen. es wird auch die daten vorbereitet und zum
    darstllen weitergegeben
    """
    try:
        geokoord = input("Geben sie die geokoordinaten in form  50.0 , 13.0: ").split(
            ","
        )
        p1 = float(geokoord[0]), float(geokoord[1])
        umkreis = int(input("Geben sie den gewunschten Umkries in Km z. B. 25: "))
        data = filter_nach_Geokoord(data, p1, umkreis)
        if len(data) == 0:
            print("In dem gegeben Umkreis findet keine Bruecken ")
        else:
            plt.title(
                "Karte der {zahl} deutsche Fernstraßenbrücken \n in einem umkreis von {umkreis} km".format(
                    zahl=len(data), umkreis=umkreis
                )
            )
            graph(data, grenzen)
    except:
        print("Falshe Eingabe! Geokoord oder Umkreis hält nicht an den gegebene form!")


def nach_strasse(data, grenzen):
    """
    in dem funktion wird der buntzer um die benötigten info gefragt damit die berechnung begint
    außer dem wird Falsche Eingaben abgefangen. es wird auch die daten vorbereitet und zum
    darstllen weitergegeben
    """
    try:
        strasse = input("Geben sie die straßen name z. B. (A 45): ")
        data = filter_nach_str(data, strasse)
        if len(data) == 0:
            print("Auf dem {strasse} findet keine bruecken".format(strasse=strasse))
        else:
            plt.title(
                "Karte der {zahl} deutsche Fernstraßenbrücken, die auf die strasse {strasse} liegen ".format(
                    zahl=len(data), strasse=strasse
                )
            )
            graph(data, grenzen)
    except ValueError:
        print("Falshe Eingabe!")


def alle_bruecken(data, grenzen):
    # Die gesamten Daten auf die drei notwendigen Daten zu kürzen und sie an die erhaltene Struktur_[nb,ol,zn]_ anpassen der Methode anzupassen.
    min_data = zip(data["ol"], data["nb"], data["zn"])
    plt.title(
        "Karte aller deutsche Fernstraßenbrücken, farblich nach Zustandsnotenbereichen unterschieden\n"
        " rot -> ograng -> gelb ->hellgruen -> gruen "
    )
    graph(min_data, grenzen)


def get_farbe(x):
    """
    erhält ein zustandnote und gibt die ansprechende farbe zurueck
    """
    return FARBEN_DIC[x]


# main
def main():
    # daten auslesen
    data = csv_lesen("data.csv")
    # [[nb,ol],[]]
    grenzen = karte_lesen("Deutschlandkarte.txt")
    print(
        "Dieses Programm ermittelt den Zustand der deutschen Fernstraßenbrücken\n"
        "und stellt die Ergebnisse grafisch dar.\n"
        "***********************************************************************"
    )
    # infinity loop wird duch benuzer abgebrochen
    while True:
        try:
            wahl = int(
                input(
                    "Wählen Sie eine der folgenden Funktionent:\n"
                    "1 - Darstellung aller Brücken, mit bestimmet Zustandsnoten\n"
                    "2 - Darstellung aller Brücken innerhalb eines definierten Umkreis nach Geokoordinaten \n"
                    "3 - Darstellung aller brücken die unter bzw ober ein bestimmte strasse\n"
                    "4 - Darstellung aller Brücken, farblich nach Zustandsnoten\n"
                    "Ihre Whal: "
                )
            )
            while wahl > 4 or wahl < 1:
                wahl = int(input("Falsche Eingabe! zahl muss zwischen 1 - 4 sein: "))
        except ValueError:
            print("Falsche Eingabe! muss ein zahl zwischen 1 - 4 sein!")
            wahl = 0

        if wahl == 1:
            nach_zustandnote(data, grenzen)
        elif wahl == 2:
            nach_umkreis(data, grenzen)
        elif wahl == 3:
            nach_strasse(data, grenzen)
        elif wahl == 4:
            alle_bruecken(data, grenzen)

        print("*************************************************")


if __name__ == "__main__":
    # dictionary für farben wird instaliert und global geblieben
    FARBEN_DIC = farben()
    main()
