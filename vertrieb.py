#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import optionen as opt
import protokoll as prot
from pathlib import Path
import os
import pandas as pd

class Vertrieb():

    def __init__(self, f_dict):
        
        file_protokoll=f_dict.get('protokoll_file_vertrieb')
        self.oprot = prot.Protokoll(file_protokoll)
        
        self.file_vertrieb=f_dict.get('file_vertrieb')
        text ='Vertrieb/__Init__: File für die Angaben zum Neugeschäft festgelegt: '+self.file_vertrieb
        self.oprot.SchreibeInProtokoll(text)
        
        self.dtype_dic= { 'nr':int, 'jahr':int, 'tkz':int, 'name':str, 'wert':str}

        
        self.LegeFileVertrieb()

    def LegeTabelleVertriebAn(self):
        datei=self.file_vertrieb
        ocsv=pd.DataFrame()
        ocsv['nr']=None
        ocsv['jahr']=None
        ocsv['tkz']=None
        ocsv['name']=None
        ocsv["wert"]=None
        
        ocsv[['nr', 'jahr', 'tkz', 'name', 'wert']] = ocsv[['nr', 'jahr', 'tkz', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Vertrieb/LegeTabelleVertriebAn: Tabelle fuer Vertrieb/Neugeschäft wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    
    def LegeFileVertrieb(self):
        datei= Path(self.file_vertrieb)
        if datei.is_file():
            text="Vertrieb/LegeFileVertrieb " +str(datei)+ " existiert bereits. Daher muss sie zuerst entfernt werden."
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            os.remove(datei)
        else:
            print("Vertrieb/LegeFileVertrieb: " +str(datei)+ " existiert nicht!!!")   
            
        self.LegeTabelleVertriebAn()
        
    def LeseNummer(self):
        datei=self.file_vertrieb
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
        df1 = df.nr

        if df1.__len__() == 0 :
            nr=0
            text="Vertrieb/LeseNummer: Kein Eintrag in der Datei gefunden: " +str(datei)
            self.oprot.SchreibeInProtokoll(text)

        else:
            try:
                nr=df1.max()
            except:
                nr=0
                text="Vertrieb/LeseNummer: die maximale Nummer konnte nicht ermittelt werden: " +str(df1)
                self.oprot.SchreibeInProtokoll(text)
        
        return nr
    
    def LeseAusCSV(self, key_dict):
        datei=self.file_vertrieb
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
       
        nr=key_dict.get('nr')
        jahr=key_dict.get('jahr')
        tkz=key_dict.get('tkz')
        name=key_dict.get('name')
 
        df1 = df[(df.nr == str(nr)) & (df.jahr == str(jahr)) & (df.tkz == str(tkz)) & (df.name==str(name))]
        
        if df1.__len__() == 0:
            wert=''
            text='Vertrieb/LeseAusCSV: kein Eintrag in der Tabelle gefunden. Es wurde null verwendet. Key: '+str(key_dict)
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1['wert'][index]

        return wert
    
    def ZeileLoeschenInCSV(self, eintrag_dict):
        datei=self.file_vertrieb
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
       
        nr=eintrag_dict.get('nr')
        jahr=eintrag_dict.get('jahr')
        tkz=eintrag_dict.get('tkz')
        name=eintrag_dict.get('name')
        
        if self.LeseAusCSV(eintrag_dict) != '':
            df = pd.read_csv(datei, sep=';')
            df1 = df[(df.nr != str(nr)) & (df.jahr != str(jahr)) & (df.tkz != str(tkz)) & (df.name != str(name))]
            df1.to_csv(datei, ';', index=False)
            
            text='Vertrieb/ZeileLoeschenInCSV: Eintrag in der Tabelle geloescht: nr='+str(nr)+'jahr='+str(jahr)+' tkz='+str(tkz) +' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)

    
    def SchreibeInTabelleVertrieb(self, eintrag_dict):
        datei=self.file_vertrieb
        
        nr=eintrag_dict.get('nr')
        jahr=eintrag_dict.get('jahr')
        tkz=eintrag_dict.get('tkz')
        name=eintrag_dict.get('name')
        wert=eintrag_dict.get('wert')
        
        if self.LeseAusCSV(eintrag_dict) != '':
            self.ZeileLoeschenInSACSV(eintrag_dict)
        
        text=str(nr)+';'+str(jahr)+';'+str(tkz)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       
    
    def SchreibeNeugeschaeft(self, vertrieb_dict):
        satz_dict={}
        jahr=int(vertrieb_dict.get('jahr'))
        nr=int(self.LeseNummer())

        anzahl_renten = int(vertrieb_dict.get('anzahl_renten'))
        if anzahl_renten > 0:
            tkz='20200101767'
            sra='N'
            beginn = str(jahr)+'0701'
            vertriebsnummer='007'
            zw=12
            nr=nr+1
            satz_dict['nr']=nr
            satz_dict['jahr']=jahr
            satz_dict['tkz']=tkz
            
            satz_dict['name']='tkz'
            satz_dict['wert']=tkz
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='sra'
            satz_dict['wert']=sra
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='beginn'
            satz_dict['wert']=beginn
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='anzahl'
            satz_dict['wert']=anzahl_renten
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='lauftzeit'
            laufzeit = int(vertrieb_dict.get('laufzeit_renten'))
            satz_dict['wert']=laufzeit
            self.SchreibeInTabelleVertrieb(satz_dict)

            ende = str(jahr+laufzeit)+'0631'
            satz_dict['name']='ende'
            satz_dict['wert']=ende
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='vertriebsnummer'
            satz_dict['wert']=vertriebsnummer
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='zw'
            satz_dict['wert']=zw
            self.SchreibeInTabelleVertrieb(satz_dict)

        anzahl_bu = int(vertrieb_dict.get('anzahl_bu'))
        if anzahl_bu > 0:
            tkz='20200101709'
            sra='N'
            beginn = str(jahr)+'0701'
            vertriebsnummer='007'
            zw=12
            nr=nr+1
            
            satz_dict['nr']=nr
            satz_dict['jahr']=jahr
            satz_dict['tkz']=tkz
            
            satz_dict['name']='tkz'
            satz_dict['wert']=tkz
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='sra'
            satz_dict['wert']=sra
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='beginn'
            satz_dict['wert']=beginn
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='anzahl'
            satz_dict['wert']=anzahl_bu
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='lauftzeit'
            laufzeit = int(vertrieb_dict.get('laufzeit_bu'))
            satz_dict['wert']=laufzeit
            self.SchreibeInTabelleVertrieb(satz_dict)

            ende = str(jahr+laufzeit)+'0631'
            satz_dict['name']='ende'
            satz_dict['wert']=ende
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='vertriebsnummer'
            satz_dict['wert']=vertriebsnummer
            self.SchreibeInTabelleVertrieb(satz_dict)

            satz_dict['name']='zw'
            satz_dict['wert']=zw
            self.SchreibeInTabelleVertrieb(satz_dict)

            


            
            
