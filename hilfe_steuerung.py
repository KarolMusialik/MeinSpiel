#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class HilfeSteuerung:
                     
    def formatter(self, number, format="%0.1f", comma=",", thousand=".", grouplength=3):
        #Formatierung für Zahlen:
            
        if abs(number) < 10**grouplength:
            return (format % (number)).replace(".", comma)
        if format[-1]=="f":
            vor_komma,hinter_komma=(format % number).split(".",-1)
        else:
            vor_komma=format % number
            comma=""
            hinter_komma=""
        #Schneide leere Zeichen vor der Zahl ab:
        anz_leer=0
        for i in vor_komma:
            if i==" ":
                anz_leer+=1
            else:
                break
        vor_komma=vor_komma[anz_leer:]
        #bis hier

        vor_komma=self.SetzePunktInZahl(vor_komma,punktgruppe=grouplength, tausend=thousand)        
        
        return vor_komma+comma+hinter_komma       

    def SetzePunktInZahl(self, zahl_alt, punktgruppe=3, tausend="."):
        len_vor_komma=len(zahl_alt)
        igruppe=0
        zahl_neu=''
        for i in range(len_vor_komma):
            zahl_neu = zahl_alt[len_vor_komma-1-i]+zahl_neu
            igruppe+=1
            if igruppe==punktgruppe and i<(len_vor_komma-1):
                igruppe=0
                zahl_neu = tausend+zahl_neu
                
        return zahl_neu
                     

