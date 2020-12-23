#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd

class Optionen:
    
    def __init__(self, f):
        self.file_optionen = f
        datei= Path(self.file_optionen)
        if datei.is_file():
            print("Datei " + self.file_optionen+ " existiert.")
            #self.SchreibeInOptionen('file_optionen', self.file_optionen)
        else:
            print("Datei " + self.file_optionen + " existiert nicht!!!")   
            return
        
    def PruefeObDateiExistiert(self, f):
        datei= Path(f)
        if datei.is_file():
            print("Datei " +f+ " existiert.")
            return True
        else:
            print("Datei " +f + " existiert nicht!!!")
            return False
        
    def SchreibeInOptionen(self, key, text):
        if self.LeseInhaltOptionen(key) != "":
            self.ZeileLoeschenInOptionen(key)
        
        text=key + ";" + text + "\n"
        f=open(self.file_optionen, "a")
        f.write(text)    
        f.close()     
        
    def LeseOptionen(self):
        self.file_protokoll=self.LeseInhaltOptionen("file_protokoll")
    
    def LeseInhaltOptionen(self, key):
        wert = " "
        df=pd.read_csv(self.file_optionen, sep=";")
        df1 = df[df.key == key]
        
        if df1.empty:
            wert=0
            text='Optionen/LeseInhaltOptionen: Kein Eintrag gefunden. Es wurde null verwendet: key='+str(print(key))
            print(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert       
    
    def ZeileLoeschenInOptionen(self, key):
        if self.LeseInhaltOptionen(key) != "":
            df = pd.read_csv(self.file_optionen, sep=';')
            print (df)
            index=df[df['key'] == key].index[0]
            dff = df.drop(index)
            print(dff)
            dff.to_csv(self.file_optionen, ';', index=False)
            print("Zeile " +key+ " geloescht")
        else:
            print("zu dem key="+key+ " existierte keine Zeile. Daher wurde auch nichts geloescht")
   


