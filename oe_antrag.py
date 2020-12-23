#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import optionen as opt
import protokoll as prot
import pandas as pd

class OE_Antarg(object):

    def __init__(self, f_dict):
        
        self.oopt = opt.Optionen(f_dict.get('optionen_file_antrag_oe'))  
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_antrag_oe'))
        
    def BearbeiteAntraege(self, jahr):
        
        #Anzahl der verkauften Produkte in einem Jahr = anzahl_produkte
        df=pd.read_csv(self.file_vertrieb, sep=";")
        df1 = df[df.jahr==jahr]
        df1 = df1.groupby(['produkt']).count()
        df1 = df1.reset_index()
        df1=df1['produkt']
        anzahl_produkte=df1.__len__()
        
        if anzahl_produkte == 0:
            print("keine Produkte in der Vertriebstabelle gefunden!")
            return
        
        anzahl_antraege=0

        for i in range(0, anzahl_produkte):
            produkt=str(df1[i]).zfill(6)
            anzahl=self.overtrieb.LeseAusCSV(jahr, produkt, 'anzahl')
            beginn=self.overtrieb.LeseAusCSV(jahr, produkt, 'beginn')
        
            if jahr <= int(self.maximales_jahr):
                anzahl_antraege += int(anzahl)
            else:
                anzahl_antraege = 0
                
            antragsnummer=self.oantrag.NeueAntragsnummer()
            
            self.oantrag.SchreibeInCSV(antragsnummer, 'antragsnummer', antragsnummer)
            self.oantrag.SchreibeInCSV(antragsnummer, 'produkt', produkt)
            self.oantrag.SchreibeInCSV(antragsnummer, 'anzahl', anzahl)
            self.oantrag.SchreibeInCSV(antragsnummer, 'beginn', beginn)
            self.oantrag.SchreibeInCSV(antragsnummer, 'status', 'offen')

        
        if jahr <= int(self.maximales_jahr):
            kosten_pro_antrag=self.ocsv.LeseCSV(self.file_oe_antrag, "kosten_pro_antrag", jahr)
        else:
            kosten_pro_antrag=self.ocsv.LeseCSV(self.file_oe_antrag, "kosten_pro_antrag", self.maximales_jahr)
            
        kosten_oe=anzahl_antraege*kosten_pro_antrag
        
        self.ocsv.SchreibeInCSV(self.file_oe_antrag, "kosten_oe", jahr, kosten_oe)
        
