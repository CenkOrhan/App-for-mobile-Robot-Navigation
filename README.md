# App-for-mobile-Robot-Navigation
Das ist eine Applikation zur autonomen Navigation des humanoiden mobilen Roboters Pepper. 
Das Ziel besteht darin mit Hilfe der vom Hersteller bereigetsellten Methoden zur "Self localization and Mapping"(SLAM) eine
Applikation zu autonomen Navigation zu enwtickeln. 
## Hinweis
1. Für das Lokalisieren wird ein Partikelfilter verwendet.
2. Für das Kartieren nutzt der Roboter das GMapping.
3. Die Datenstruktur des GMapping's ist eine Matrix und kein Binärbaum.
4. Matixdaten: 0 = kein Hindernis, 100 = Hindernis, 50 = nicht gemessen.
5. Die Erste Zeile der Matrixdaten geben die Koordinatentransformationen der Mapdaten von Pixelkoordinaten in Realkoodinaten an.
6. Während der Fahrt seiner Trajektorie steigt der Lokalsierungsfehler mit zunehmender Codegröße, da während der Fahrt der Arbeitsspeicher durch den Algorithmusses des Partikelfilters zur jeder zeit x=pmax(m/y) versucht zu bestimmen. 
