#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import optionen as opt
import protokoll as prot
import pandas as pd
import datetime
import random 
import os
import csv

class Antrag(object):

    def __init__(self, f_dict):
        self.oopt = opt.Optionen(f_dict.get('optionen_file_antrag'))  
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_antrag'))
        
        self.file_system_antrag=f_dict.get('file_system_antrag')
        
        self.LegeAntrag()
        
        self.pfad=os.path.dirname(self.file_system_antrag)
        self.temp=self.pfad+'/temp.csv'
        
        
        
    def LegeAntrag(self):
        datei=self.file_system_antrag
        ocsv=pd.DataFrame()
        ocsv["antragsnummer"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv[['antragsnummer', 'name', 'wert']] = ocsv[['antragsnummer', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
    
    def LegeVerriebstabelleFest(self, file_vertrieb):
        self.file_vertrieb = file_vertrieb
        
    def LeseVertrieb(self, jahr):
        jahr=str(jahr).zfill(4)
        datei=self.file_vertrieb
        df=pd.read_csv(datei, sep=";", dtype=object)
        df1 = df[(df.jahr == str(jahr))]
        df1.to_csv(self.temp, ';', index=False)
        self.LeseDatensaetzteAusCSV()
        os.remove(self.temp)
        
    def PruefeObAntargsnummerExistiert(self, antragsnummer):
        datei=self.file_system_antrag
        df=pd.read_csv(datei, sep=";", dtype=object)
        df1 = df[(df.antragsnummer == str(antragsnummer))]
        if df1.__len__() == 0:
            wert=True
        else:
            wert=False
       
        return wert        
        
    def LeseDatensaetzteAusCSV(self):
        file = open(self.temp, "r")
        csv_reader = csv.reader(file, delimiter=";")
        
        #Beschreibung(Position der Felder) des Datensatzes in der CSV:
        index=0
        jahr=1
        tkz=2
        name=3
        wert=4

        index_alt=0        
        daten_dict={}
        antragsnummer=0
        
        next(csv_reader)
        for row in csv_reader:

            index=row[0]
            jahr=row[1]
            tkz=row[2]
            name=str(row[3])
            wert=row[4]

            #neuer Index?
            if index != index_alt:
                
                if index_alt != 0: #index_alt=0 würde heissen, dass es sich um alle ersten satz handelt. Diese wollen wir überspringen
                    self.ladeDictZuCSVAus(daten_dict)
                
                antragsnummer=self.NeueAntragsnummer()
                while self.PruefeObAntargsnummerExistiert(antragsnummer) == False:
                    antragsnummer=self.NeueAntragsnummer()
                
                index_alt = index
                
                daten_dict.clear()
                
                daten_dict['antragsnummer']=antragsnummer
                daten_dict['jahr']=jahr
                daten_dict['tkz']=tkz
                daten_dict['status']='offen'
                
            
            if name in (None, ''):
                satzinfos = 'index= '+index+ ' jahr: '+jahr+ ' tkz: '+tkz
                text = 'Feld '+str(name)+ ' wurde nicht verarbeitet: ' + satzinfos
                self.oprot.SchreibeInProtokoll(text)
            else:
                daten_dict[name]=wert

                
        if index_alt != 0:
            self.ladeDictZuCSVAus(daten_dict)
            
                
    def ladeDictZuCSVAus(self, d):
        
        if bool(d) == True:
            antragsnummer=d.get('antragsnummer')
            for key in d:
                name=key
                wert=d[key]
                self.SchreibeInCSV(antragsnummer, name, wert)            
        else:
            text='der Dictionary scheint leer zu sein '
            self.oprot.SchreibeInProtokoll(text)
    
    def LeseAusCSV(self, antragsnummer, name):
        datei=self.file_system_antrag
        df=pd.read_csv(datei, sep=";")
        df[['antragsnummer', 'name', 'wert']] = df[['antragsnummer', 'name', 'wert']].astype(str)
        
        df1 = df[(df.antragsnummer == antragsnummer) & (df.name == name)]
        if df1.__len__() == 0:
            wert=0
        else:
            wert=df1['wert'].get_values()[0]
       
        return wert        

    def ZeileLoeschenInCSV(self, antragsnummer, name):
        datei=self.file_system_antrag
        if self.LeseAusCSV(antragsnummer, name) != 0:
            df = pd.read_csv(datei, sep=';')
            df1=df[(df['antragsnummer'] != antragsnummer) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            print("Zeile " +name+ " geloescht")
        else:
            print("zu der antragsnummer="+antragsnummer+ " existierte keine Zeile. Daher wurde auch nichts geloescht")

    def SchreibeInCSV(self, antragsnummer, name, wert):
        datei=self.file_system_antrag
        if self.LeseAusCSV(antragsnummer, name) != 0:
            self.ZeileLoeschenInCSV(antragsnummer, name)
        
        text=str(antragsnummer) + ";" + str(name) + ";" + str(wert) + "\n"
        f=open(datei, "a")
        f.write(text)    
        f.close()             

    def NeueAntragsnummer(self):
        datum=datetime.date.today()
        jahr=str(datum.year).zfill(4)
        monat=str(datum.month).zfill(2)
        tag=str(datum.day).zfill(2)
        
        zeit=datetime.datetime.now()
        stunde=str(zeit.hour).zfill(2)
        minute=str(zeit.minute).zfill(2)
        sekunde=str(zeit.second).zfill(2)
        
        zufallszahl=self.EineZufallszahl()
        zufallszahl=str(zufallszahl).zfill(3)
        
        neuenummer=jahr+monat+tag+stunde+minute+sekunde+zufallszahl
        return neuenummer
    
    def EineZufallszahl(self):
        random.seed()
        return random.randint(1,999)


