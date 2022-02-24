## Simple Berechnung der Distanz zweier Punkte anhand ihrer
## Geokoordinaten.
from math import radians, sin, cos, acos


def geodist(P1, P2):
    """Berechnet die Entfernung in [km] zweier Punkte auf der Erdoberfläche.
    Die Punkte P1 und P2 müssen als Tupel zweier Geokoordinaten vorliegen,
    also beispielsweise (52.1234, 7.8901)."""
    L1, B1 = map(radians, P1)
    L2, B2 = map(radians, P2)
    return 6378.388 * acos(sin(L1) * sin(L2)
                           + cos(L1) * cos(L2) * cos(B2-B1))

if __name__=="__main__":
    Dortmund = 51.447918 ,7.27069 
    Berlin = 51.45903, 7.28047
    Entfernung = geodist(Dortmund, Berlin)
    print(f"Entfernung Dortmund-Berlin: {Entfernung:.2f} km")
    

