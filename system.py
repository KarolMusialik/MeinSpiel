# -*- coding: utf-8 -*-
import protokoll as prot
import pandas as pd
import datetime
import random 
import produktmanager as pm
import statistik as stat 
import fortschreibung as fort
import os
import shutil
import hilfe_system as hs


class System(object):

    def __init__(self, f_dict):
        
        work_dir = f_dict.get('work_dir')+f_dict.get('sep_dir')
        self.file_protokoll = work_dir+'protokoll_system.csv'
        
        self.file_system_bestand = work_dir+'system_bestand.csv'
        f_dict['system_bestand'] = self.file_system_bestand
        
        self.file_system_fortschreibung = f_dict.get('file_system_fortschreibung')
        self.dtype_fortschreibung = f_dict.get('file_system_fortschreibung_struktur')
        
        self.file_system_statistik = work_dir+'system_statistik.csv'
        self.file_system_statistik_beschreibung = work_dir+'system_statistik_beschreibung.txt'
        
        self.LegeBestand()
        self.LegeFortschreibung()
        self.LegeStatistik()
        
        self.files_dict = f_dict
        self.files_dict['wSchreibeInBilanzCSVork_dir'] = work_dir
        self.files_dict['file_system_bestand'] = self.file_system_bestand
        self.files_dict['file_system_fortschreibung'] = self.file_system_fortschreibung

        self.files_dict['file_system_statistik'] = self.file_system_statistik
        self.files_dict['file_system_statistik_beschreibung'] = self.file_system_statistik_beschreibung
        
        work_dir_pm = work_dir+'pm' + f_dict.get('sep_dir')
        if os.path.isdir(work_dir_pm) == False:
            os.makedirs(work_dir_pm)
        else:
            shutil.rmtree(work_dir_pm, ignore_errors=True)
            os.makedirs(work_dir_pm)            

        self.files_dict['woSchreibeInBilanzCSVrk_dir_pm'] = work_dir_pm

        self.ostat = stat.Statistik(self.files_dict)
        
        self.listeOffenerVertraege = None
        
        self.hilfe = hs.Hilfe_System()
        
        self.ofort=fort.Fortschreibung(self.files_dict)
        
    def LegeStatistik(self):
        #Hier wird lediglich die Tabelle "system_statistik.csv" angelegt
        datei=self.file_system_statistik
        ocsv=pd.DataFrame()
        ocsv["von"]=None
        ocsv["bis"]=None
        ocsv["produkt"]=None
        ocsv["position"]=None
        ocsv["vsnr"]=None
        ocsv["histnr"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv.to_csv(datei, ';', index=False)

    def LegeBestand(self):
        #Hier wird lediglich die Tabelle "system_bestand.csv" nur angelegt

        datei=self.file_system_bestand
        ocsv=pd.DataFrame()
        ocsv["vsnr"]=None
        ocsv["histnr"]=None
        ocsv["von"]=None
        ocsv["bis"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv.to_csv(datei, ';', index=False)

    def LegeFortschreibung(self):
        #Hier wird lediglich die Tabelle "system_fortschreibung.csv" nur angelegt

        datei=self.file_system_fortschreibung
        ocsv=pd.DataFrame()
        ocsv["vsnr"]=None
        ocsv["histnr"]=None
        ocsv["von"]=None
        ocsv["bis"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv.to_csv(datei, ';', index=False)

    def LegeAntragstabelleFest(self, file_system_antrag):
            self.file_system_antrag = file_system_antrag
        
    def ListeOffenerAntraege(self, jahr):
        datei=self.file_system_antrag
        df=pd.read_csv(datei, sep=";", dtype=object)
        df1=df[df.name == 'antragsnummer']['wert']
       
        liste=[]
        for antragsnummer in df1:
            df2=df[(df.antragsnummer==antragsnummer) & (df.name == 'status')]['wert']
            
            if df2.empty:
                wert=0
                text='system/ListeOffenerAntraege: kein Eintrag in der Tabelle. Es wurde null verwendet'
                self.oprot.SchreibeInProtokoll(text)
            else:
                index=df2.index[0]
                wert=df2[index]
            
            status=wert
            
            
            df2=df[(df.antragsnummer==antragsnummer) & (df.name == 'jahr')]['wert']
            if df2.empty:
                wert=0
                text='system/ListeOffenerAntraege: kein Eintrag in der Tabelle. Es wurde null verwendet'
                self.oprot.SchreibeInProtokoll(text)
            else:
                index=df2.index[0]
                wert=df2[index]
            
            jjjj=wert
            
            if status=='offen' and int(jjjj) <= int(jahr):
                liste.append(antragsnummer)
                
        return liste
    
    def LeseAntragInDict(self, antragsnummer):
        datei=self.file_system_antrag
        df=pd.read_csv(datei, sep=";")
        df[['antragsnummer', 'name', 'wert']] = df[['antragsnummer', 'name', 'wert']].astype(str)
        
        df1 = df[(df.antragsnummer == antragsnummer)]['name']
        
        antrag={}
        antrag.clear()
        
        if df1.__len__() == 0:
            text = 'In der Antragstabelle: ' +datei+ ' mit der antragsnummer: ' +antragsnummer+ ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            for name in df1:
                df2 = df[(df.name == str(name)) & (df.antragsnummer == antragsnummer)]['wert']
                ind=df2.index[0]
                wert = df2[ind]
                antrag[name]=wert
                
        return antrag
        
    def LeseAusAntragCSV(self, antragsnummer, name):
        datei=self.file_system_antrag
        df=pd.read_csv(datei, sep=";")
        df[['antragsnummer', 'name', 'wert']] = df[['antragsnummer', 'name', 'wert']].astype(str)
        
        df1 = df[(df.antragsnummer == antragsnummer) & (df.name == name)]
        if df1.__len__() == 0:
            wert=0
            text = 'In der Antragstabelle: ' +datei+ ' mit der antragsnummer: ' +antragsnummer+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            ind=df1['wert'].index[0]
            wert=df1.at[ind, 'wert']
       
        return wert        

    def ZeileLoeschenInAntragCSV(self, antragsnummer, name):
        datei=self.file_system_antrag
        if self.LeseAusAntragCSV(antragsnummer, name) != 0:
            df = pd.read_csv(datei, sep=';')
            df[['antragsnummer', 'name', 'wert']] = df[['antragsnummer', 'name', 'wert']].astype(str)
            df1=df.drop(df[(df['antragsnummer'] == antragsnummer) & (df['name']==name)].index)
            df1.to_csv(datei, ';', index=False)
            print("Zeile " +name+ " geloescht")
        else:
            print("zu der antragsnummer="+antragsnummer+ " existierte keine Zeile. Daher wurde auch nichts geloescht")
    
    def SchreibeInAntragCSV(self, antragsnummer, name, wert):
        datei=self.file_system_antrag
        if self.LeseAusAntragCSV(antragsnummer, name) != 0:
            self.ZeileLoeschenInAntragCSV(antragsnummer, name)
        
        text=str(antragsnummer) + ";" + str(name) + ";" + str(wert) + "\n"
        f=open(datei, "a")
        f.write(text)    
        f.close()           
    
    def LeseWertAusBestandCSV(self, key, name):
        datei=self.file_system_bestand
        df=pd.read_csv(datei, sep=";")
        
        vsnr = key.get('vsnr')
        histnr = key.get('histnr')
        von = key.get('von')
        bis = key.get('bis')
        
        df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']] = df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']].astype(str)
        
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis) & (df.name == name)]
        
        if df1.__len__() == 0:
            wert=0
            text = 'In der Bestandstabelle: ' +datei+ ' mit der vsnr: ' +vsnr+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            wert=df1['wert'].get_values()[0]
        
        return wert        


    def SchreibeInBestandCSV(self, key, eintrag):
        datei=self.file_system_bestand
        
        vsnr = key.get('vsnr')
        histnr = key.get('histnr')
        von = key.get('von')
        bis = key.get('bis')

        name=eintrag.get('name')
        wert=eintrag.get('wert')
        
        text=str(vsnr) + ";" + str(histnr) + ";" + str(von) + ";" + str(bis) + ";" + str(name) + ";" + str(wert) + "\n"
        
        f=open(datei, "a")
        f.write(text)    
        f.close()           
    
    
    def Policiere(self, jahr):
        listeAntraege=self.ListeOffenerAntraege(jahr)
        
        vertrag_neu={}
        vertrag_alt={}
        
        for nummer in listeAntraege:
            antragsnummer=self.LeseAusAntragCSV(nummer, 'antragsnummer')
            
            vertrag_neu.clear()
            vertrag_neu=self.LeseAntragInDict(antragsnummer)
            
            vsnr=self.NeueVertragsnummer()
            while self.PruefeObVSNRExistiert(vsnr) == False:
                vsnr=self.NeueVertragsnummer()
            
            gevo='Neuzugang'
            histnr=str(1)
            von=vertrag_neu.get('beginn')
            bis = vertrag_neu.get('ende')
            
            vertrag_neu['vsnr']=vsnr
            vertrag_neu['histnr']=histnr
            vertrag_neu['von']=von
            vertrag_neu['bis']=bis
            vertrag_neu['gevo']=gevo

            opm = pm.Produktmanager(self.files_dict, vertrag_neu)
            vertrag_neu=opm.Rechne(vertrag_alt, vertrag_neu)
            
            self.LeseDict(vertrag_neu)
            self.SchreibeInAntragCSV(antragsnummer, 'status', 'policiert')
            
            beginn = self.hilfe.DictAusDatum(vertrag_neu.get('beginn'))
            von=beginn            
            bis_jjjj=beginn.get('jahr')
            bis=self.hilfe.DictAusDatum(str(bis_jjjj)+'1231')
            
            ofort=fort.Fortschreibung(self.files_dict)
            ofort.SchreibeVertragFort(vertrag_neu, von, bis)
            
    def SchreibeDictInBilanz(self, vertrag):
        key={}
        eintrag={}
        
        key.clear()
        key['vsnr']=vertrag.get('vsnr')
        key['histnr']=vertrag.get('histnr')
        key['von']=vertrag.get('von')
        key['bis']=vertrag.get('bis')
        
        for index in vertrag:
            eintrag['name']=str(index)
            eintrag['wert']=vertrag.get(str(index))

            self.SchreibeInBilanzCSV(key, eintrag)

    def SchreibeInBilanzCSV(self, key, eintrag):
        datei=self.file_system_bestand
        
        vsnr = key.get('vsnr')
        histnr = key.get('histnr')
        von = key.get('von')
        bis = key.get('bis')

        name=eintrag.get('name')
        wert=eintrag.get('wert')
        
        text=str(vsnr) + ";" + str(histnr) + ";" + str(von) + ";" + str(bis) + ";" + str(name) + ";" + str(wert) + "\n"
        
        f=open(datei, "a")
        f.write(text)    
        f.close()       
                
    def LeseDict(self, vertrag):
        key={}
        eintrag={}
        
        key.clear()
        key['vsnr']=vertrag.get('vsnr')
        key['histnr']=vertrag.get('histnr')
        key['von']=vertrag.get('von')
        key['bis']=vertrag.get('bis')

        for index in vertrag:
            eintrag['name']=str(index)
            eintrag['wert']=vertrag.get(str(index))

            self.SchreibeInBestandCSV(key, eintrag)

    def NeueVertragsnummer(self):
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
            
    def PruefeObVSNRExistiert(self, vsnr):
        datei=self.file_system_bestand
        df=pd.read_csv(datei, sep=";", dtype=object)
        df1 = df[(df.vsnr == str(vsnr))]
        if df1.__len__() == 0:
            wert=True
        else:
            wert=False
       
        return wert        
            
    def ErstelleStatistik(self, von, bis):
        self.ostat.ErstelleStatistik(von, bis)
    
    def LeseVertragAusBestand(self, key):
        vsnr = str(key.get('vsnr'))
        histnr = str(key.get('histnr'))
        von = str(key.get('von'))
        bis = str(key.get('bis'))
        
        vertrag={}
        
        datei=self.file_system_bestand
        df=pd.read_csv(datei, sep=";")
        df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']] = df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']].astype(str)
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis)]['name']
        for name in df1:
            wert=self.LeseWertAusBestandCSV(key,name)
            vertrag[name]=wert
            
        return vertrag
  
    def Fortschreibung(self, von_int, bis_int):
        self.ofort.FortschreibungVonBis(von_int, bis_int)
        self.ofort.RegulaereAblaeufe(von_int, bis_int)

             
    

                

