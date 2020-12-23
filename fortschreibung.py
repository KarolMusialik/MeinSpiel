#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import protokoll as prot
import pandas as pd
import datetime
import hilfe_system as hs
import produktmanager as pm

class Fortschreibung:

    def __init__(self, f_dict):
        work_dir=f_dict.get('work_dir')
        file_protokoll=work_dir+'protokoll_system_fortschreibung.txt'
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_system_bestand=f_dict.get('file_system_bestand')
        self.file_system_fortschreibung=f_dict.get('file_system_fortschreibung')
        self.file_system_bestand_struktur_dict=f_dict.get('file_system_bestand_struktur')
        self.file_system_fortschreibung_struktur_dict=f_dict.get('file_system_fortschreibung_struktur')

        self.files_dict=f_dict
        
        self.hilfe = hs.Hilfe_System()
    
    def LeseWertAusBestandCSV(self, key, name):
        datei=self.file_system_bestand
        struktur = self.file_system_bestand_struktur_dict
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        
        vsnr = key.get('vsnr')
        histnr = int(key.get('histnr'))
        von = int(key.get('von'))
        bis = int(key.get('bis'))
        
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis) & (df.name == name)]
        
        if df1.empty:
            wert=0
            text='In der Bestandstabelle: ' +datei+ ' mit der vsnr: ' +vsnr+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']

        return wert        

    def LeseWertAusFortschreibungCSV(self, key_dict, name):
        datei=self.file_system_fortschreibung
        df=pd.read_csv(datei, sep=";")
        
        vsnr = key_dict.get('vsnr')
        histnr = key_dict.get('histnr')
        von = key_dict.get('von')
        bis = key_dict.get('bis')
        
        df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']] = df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']].astype(str)
        
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis) & (df.name == name)]
        
        if df1.empty:
            wert=0
            text = 'Fortschreibung: in der Fortschreibungstabelle: ' +datei+ ' mit der vsnr: ' +vsnr+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1['wert'][index]
        
        return wert        

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
    
    def SchreibeDictInFortschreibung(self, von_dict, bis_dict, vertrag):
        key={}
        eintrag={}
            
        key.clear()
        key['vsnr']=vertrag.get('vsnr')
        key['histnr']=vertrag.get('histnr')
        key['von']=von_dict.get('jjjjmmtt')
        key['bis']=bis_dict.get('jjjjmmtt')
            
        for index in vertrag:
            eintrag['name']=str(index)
            eintrag['wert']=vertrag.get(str(index))
            self.SchreibeInFortschreibungCSV(key, eintrag)

    def SchreibeInFortschreibungCSV(self, key, eintrag):
        datei=self.file_system_fortschreibung
        
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
    
    def BestimmeKeyInFortschreibung(self, key_dict):
        datei=self.file_system_fortschreibung
        df=pd.read_csv(datei, sep=";", dtype=object)
        
        vsnr=key_dict.get('vsnr')
        histnr=key_dict.get('histnr')
        bis=key_dict.get('bis')
        von=''
        
        df1 = df[(df.vsnr == str(vsnr)) & (df.histnr == str(histnr)) & (df.bis == str(bis))]    

        if df1.__len__() == 0:
            text='System: kein key in der Fortschreibung gefunden vsnr='+str(vsnr)+', histnr='+str(histnr)+', bis='+str(bis)
            self.oprot.SchreibeInProtokoll(text)
        else:
            df2 = df1[df1.name=='von']['von']
            if df2.__len__() == 0:
                text='System: Eigentlich muesste es einen key.von in der Fortschreibung geben. vsnr='+str(vsnr)+', histnr='+str(histnr)+', bis='+str(bis)
                self.oprot.SchreibeInProtokoll(text)
            else:
                if df2.__len__() == 1:
                    # alles okay, es soll nur einen satz geben
                    index=df2.index[0]
                    wert=df2[index]
                    von=wert
                else:
                    text='System: Es wurden mehrere key.von in der Fortschreibung gefunden. Keine Eindeutige Zuordnung möglich!. vsnr='+str(vsnr)+', histnr='+str(histnr)+', bis='+str(bis)
                    self.oprot.SchreibeInProtokoll(text)
                    
        key_dict['von']=str(von)    
            
        return key_dict
    
    def ListeOffenerVertraege(self, von_dict, bis_dict):
        #Ermittlung einer Liste aller aktiven Verträge, die fortgeschrieben werden sollen
        
        datei=self.file_system_bestand
        struktur=self.file_system_bestand_struktur_dict
        
        bis=int(bis_dict.get('jjjjmmtt'))
        von=int(von_dict.get('jjjjmmtt'))
        
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        df1=df[df.name == 'vsnr']['wert']
        
        self.listeOffenerVertraege=None
        
        alle_daten_dict={}
        
        for vsnr in df1:    
            vertrag_vorhanden=False            
            
            alle_daten_dict.clear
            alle_daten_dict=df[(df.vsnr==vsnr)].groupby(['vsnr', 'histnr', 'von', 'bis']).groups

            for satz in alle_daten_dict:
                vsnr_histnr = satz[1]
                vsnr_von = satz[2]
                vsnr_bis = satz[3]
                if (vsnr_bis >= bis & vsnr_von <= von):
                    vertrag_vorhanden=True
                    bis_vertrag=vsnr_bis
                    von_vertrag=vsnr_von
                    histnr_vertrag=vsnr_histnr
            
            if vertrag_vorhanden == True:
                self.listeOffenerVertraege=hs.VerketteteListe(vsnr, histnr_vertrag, von_vertrag, bis_vertrag, self.listeOffenerVertraege)
    
    def FortschreibungVonBis(self, von_int, bis_int):
        
        von_dict=self.hilfe.DictAusDatum(str(von_int))
        bis_dict=self.hilfe.DictAusDatum(str(bis_int))

        self.ListeOffenerVertraege(von_dict, bis_dict)
        liste = self.listeOffenerVertraege
        if liste == None:
            text='System: Es wurden keine Vertraege zur Fortschreibung gefunden: von='+str(von_int)+' bis='+str(bis_int)
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            return
        
        key={}
        key_alt={}
        vertrag_bestand={}
        vertrag_fort_alt={}
        vertrag_fort_neu={}
        while liste is not None:
            key.clear()
            key['vsnr']=liste.vsnr
            key['histnr']=liste.histnr
            key['von']=liste.von
            key['bis']=liste.bis
            
            vertrag_bestand.clear()
            vertrag_bestand=self.LeseVertragAusBestand(key)
            
            vertrag_fort_neu.clear()
            vertrag_fort_alt.clear()
            key_alt.clear()
            
            bis_alt_str=self.RechneDatum(von_dict.get('jjjjmmtt'), -1)
            
            key_alt['vsnr']=liste.vsnr
            key_alt['histnr']=liste.histnr
            key_alt['bis']=bis_alt_str

            key_alt=self.BestimmeKeyInFortschreibung(key_alt)
            vertrag_fort_alt=self.LeseVertragAusFortschreibung(key_alt)
            
            vertrag_fort_neu=vertrag_bestand
            vertrag_fort_neu=self.AnfangswerteFestlegen(vertrag_fort_alt, vertrag_fort_neu)
            
            self.SchreibeVertragFort(vertrag_fort_neu, von_dict, bis_dict)

            liste=liste.nxt
        else:
            text='Fortschreibung/FortschreibungVonBis: Es wurden alle Vertraege fortgeschrieben: von='+str(von_int)+' bis='+str(bis_int)
            print(text)
            self.oprot.SchreibeInProtokoll(text)    
    
    
    
    def AnfangswerteFestlegen(self, vertrag_alt, vertrag_neu):
        
        vertrag_neu['bil_derue1_anfang'] = vertrag_alt['bil_derue1_ende']
        vertrag_neu['bil_derue2_anfang'] = vertrag_alt['bil_derue2_ende']
        vertrag_neu['bil_derue3_anfang'] = vertrag_alt['bil_derue3_ende']
        vertrag_neu['bil_derue5_anfang'] = vertrag_alt['bil_derue5_ende']
        vertrag_neu['bil_derue7_anfang'] = vertrag_alt['bil_derue7_ende']
        
        vertrag_neu['bil_bio_nachreservierung_anfang'] = vertrag_alt['bil_bio_nachreservierung_ende']
        vertrag_neu['bil_zzr_nachreservierung_anfang'] = vertrag_alt['bil_zzr_nachreservierung_ende']
        vertrag_neu['bil_unisex_nachreservierung_anfang'] = vertrag_alt['bil_unisex_nachreservierung_ende']

        return vertrag_neu
    
    def RechneDatum(self, datum_int, tage):
        datum_dict=self.hilfe.DictAusDatum(str(datum_int))
        tt_int=datum_dict.get('tt_int')
        mm_int=datum_dict.get('mm_int')
        jjjj_int=datum_dict.get('jjjj_int')
        datum=datetime.datetime(jjjj_int,mm_int,tt_int)
        
        d = datum + datetime.timedelta(tage)
        jjjj_neu=str(d.year)
        mm_neu=str(d.month).zfill(2)
        tt_neu=str(d.day).zfill(2)
        s=str(jjjj_neu)+str(mm_neu)+str(tt_neu)
        
        return s        
    
    def LeseVertragAusFortschreibung(self, key_dict):
        vsnr = str(key_dict.get('vsnr'))
        histnr = str(key_dict.get('histnr'))
        von = str(key_dict.get('von'))
        bis = str(key_dict.get('bis'))
        
        vertrag={}
        
        datei=self.file_system_fortschreibung
        df=pd.read_csv(datei, sep=";")
        df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']] = df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']].astype(str)
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis)]['name']
        for name in df1:
            wert=self.LeseWertAusFortschreibungCSV(key_dict,name)
            vertrag[name]=wert
            
        return vertrag

    def IstVertragInFortschreibung(self, vertrag):
        datei=self.file_system_fortschreibung
        
        df=pd.read_csv(datei, sep=";", dtype=object)
        
        vsnr=vertrag.get('vsnr')
        
        df1 = df[(df.vsnr == str(vsnr))]    

        dic={}
        if df1.__len__() == 0:
            dic['fortgeschieben']='nein'
        else:
            dic['fortgeschieben']='nein'
       
        return dic
  
    def SchreibeVertragFort(self, vertrag, von_dict, bis_dict):
        opm = pm.Produktmanager(self.files_dict, vertrag)
        opm.FortschreibungVonBis(von_dict, bis_dict, vertrag)
        self.SchreibeDictInFortschreibung(von_dict, bis_dict, vertrag)
