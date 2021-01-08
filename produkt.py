# -*- coding: utf-8 -*-
import protokoll as prot
import pandas as pd


class Produkt(object):
    
    def __init__(self, f_dict):
        
        work_dir = f_dict.get('work_dir')+f_dict.get('sep_dir')
        file_protokoll = work_dir + 'protokoll_system_pm_produkt.txt'
        self.oprot = prot.Protokoll(file_protokoll)
        
        self.file_produkt = work_dir+'produkt.csv'
    
    def LeseProduktDaten(self, d):
        datei=self.file_produkt
        tkz=d.get('tkz')
        termin=d.get('von')
        
        df=pd.read_csv(datei, sep=";", dtype=object)
        df1 = df[(df.tkz == tkz) & (df.von <= termin) & (df.bis > termin)]['name']
        
        proddic={}
        proddic.clear()
        
        if df1.__len__() == 0:
            text = 'Produkt: In der Produkttabelle: ' +str(datei)+ ' mit der tkz: ' +str(tkz)+ ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            for name in df1:
                df2 = df[(df.tkz == tkz) & (df.von <= termin) & (df.bis > termin) & (df.name == name)]['wert']
                
                if df2.empty:
                    wert=0
                    text='produkt/LeseProduktDaten: kein Eintrag in der Tabelle gefunden. Es wurde null verwendet'
                    self.oprot.SchreibeInProtokoll(text)
                else:
                    index=df2.index[0]
                    wert=df2[index]

                proddic[name]=wert
                
        return proddic