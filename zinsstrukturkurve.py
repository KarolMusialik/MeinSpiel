#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import hilfe_statistik as hstat

class Zinsstrukturkurve(object):
        
    def __init__(self, f_dict):
        work_dir=f_dict.get('work_dir')+f_dict.get('sep_dir')
        self.work_dir = work_dir
        file_protokoll=work_dir+'protokoll_zinsstrukturkurve.txt'
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_zinskurve_tabelle=work_dir+'ka_zinskurve.csv'
        self.file_zinskurve_start_tabelle=work_dir+'ka_zinskurve_start.csv'
        self.file_zinskurve_grafik=work_dir+'grafik_zsk.png'
        self.file_zsk_verschiebung_grafik=work_dir+'grafik_zsk_verschiebung.png'
        self.file_zsk_infos=work_dir+'zsk_infos.csv'
        self.satz_zsk_dict={}
        
        self.startjahr_Simulation = f_dict.get('Startjahr_Simulation')
        self.anzahl_jahre_in_zinsstrukturkurve = 5
        
        self.LegeZinskurveTabelleAn()
        
        self.LegeZskInfosAn()
        
        self.LeseZinskurveStart()

    def Init_ZSK(self, satz_dict):
        self.renten_sa_risiko=satz_dict.get('risiko')

    def ZeichneZSK(self):
        self.ZeichneZSK_Zinsen()
        self.ZeichneZSK_Verschiebung()
        
    def ZeichneZSK_Verschiebung(self):
        datei=self.file_zsk_infos
        df=pd.read_csv(datei, sep=";")
        
        fig, axis = plt.subplots(1,1)

        x = []
        y = []

        df1=df[(df['name'] == 'verschiebung')]
        
        for index in range(len(df1.index)):
            x.append(int(df1.at[index, 'jahr']))
            y.append(float(df1.at[index, 'wert']))

        axis.plot(x, y)
        axis.set_title('Zinsstrukturkurve/Verschiebung ')
        axis.set_xlabel('Jahr', rotation=45)

        file = self.file_zsk_verschiebung_grafik
        fig.savefig(file)
        
        
    def ZeichneZSK_Zinsen(self):
        
        datei=self.file_zinskurve_tabelle
        table=pd.read_csv(datei, sep=";")

        A4 = 8.27 , 11.69
        
        fig, axis = plt.subplots(1,1)

        fig.suptitle('Zinsstrukturkurve', fontsize=15, fontweight='bold')
        
        jahre = []
        ywerte = []

        for index in range(len(table.index)):
            jahre.append(int(table.loc[index][0]))
            ywerte.append(table.loc[index][2:len(table.columns)].to_list())

        xwerte = []
        x = table.columns.to_list()[2:len(table.columns)]
        
        for x1 in x:
            text=str(x1)
            stelle=text.find('_')
            laenge=len(text)
            jjjj=text[stelle+1:laenge]
            xwerte.append(jjjj)
        
        
        axis.set_title('Zinsstrukturkurve')
        axis.set_ylabel('Wert')
        axis.set_xlabel('Jahr')

        for y in ywerte:
            axis.plot(xwerte, y)
        
        axis.legend(jahre,framealpha=1,loc='lower right')
        
        fig.set_size_inches(A4[0],A4[1])
        
        file = self.file_zinskurve_grafik
        fig.savefig(file)

    
    def Fortschreibung(self, jahr):
        #die Zinsstrukturkurve wird um ein Jahr fortgeschrieben
        stat_dict={}
        
        #Erwartungswert aus den letzten Jahren:
        #ex=self.RechneErwartungswert(jahr)
        #stat_dict['ex']=ex
        
        stat_dict['risiko']=self.renten_sa_risiko

        ohstat = hstat.Hilfe_Statistik(stat_dict)
        verschiebung=ohstat.NeuerWert()/100 # /100, da es sich um eine Prozetzahl handelt
        
        zsk_info_dict={}
        zsk_info_dict['jahr']=str(jahr)
        zsk_info_dict['name']='verschiebung'
        zsk_info_dict['wert']=str(verschiebung)
        self.SchreibeInInfos(zsk_info_dict)
        
        self.TrageNeuesJahrEin(jahr, verschiebung)
        
        self.ZeichneZSK()

    def TrageNeuesJahrEin(self, aktuellesJahr, verschiebung):

        datei=self.file_zinskurve_tabelle
        df=pd.read_csv(datei, sep=";")
       
        jahr_1 = int(aktuellesJahr)-1
        row = df[(df['jahr']==jahr_1)]
        
        for key in self.satz_zsk_dict:
            
            if key=='datum':
                wert=str(aktuellesJahr)+'-12'
            elif key=='jahr':
                wert=str(aktuellesJahr)
            else:
                index=row[key].index[0]
                wert = row.at[index, key]
                wert = float(wert)+verschiebung
            
            self.satz_zsk_dict[key]=wert
            
        self.SchreibeSatzDictInCSV()

    def RechneErwartungswert(self, jjjj):
        
        start=int(jjjj)
        
        datei=self.file_zinskurve_tabelle
        df=pd.read_csv(datei, sep=";")
        
        f_dict={'jahr_1':0, 'jahr_2':0, 'jahr_3':0, 'jahr_4':0, 'jahr_5':0, 'jahr_6':0, 'jahr_7':0, 'jahr_8':0, 'jahr_9':0, 'jahr_10':0}
        for jahr in range(start-self.anzahl_jahre_in_zinsstrukturkurve, start):

            row=df[(df.jahr==jahr)] #eine Zeile aus der ZSK fuer ein Jahr
    
            for key in f_dict: #es werden alle werte fuer ein Jahr der ZSK addiert
                wert=row[key].get_values()[0]
                f_dict[key]=float(f_dict.get(key))+float(wert)
                
        for key in f_dict:
            wert=f_dict.get(key)
            wert=float(wert)/self.anzahl_jahre_in_zinsstrukturkurve
            f_dict[key]=float(wert)

        wert=0
        anzahl=0
        for key in f_dict:
            anzahl=anzahl+1
            wert=wert+float(f_dict.get(key))

        ex=wert/anzahl
        return ex
            
    def LeseZinskurve(self, jahr, name_laufzeit):
        datei=self.file_zinskurve_tabelle
        typen = {'jahr':np.int64}
        df=pd.read_csv(datei, sep=";", dtype=typen)
       
        sd='jahr'
        sl=name_laufzeit
 
        df1 = df[[sd, sl]]
        df2 = df1[(df1['jahr']==jahr)]
        if df2.__len__() == 0:
            wert=''
        else:
            index=df2[sl].index[0]
            wert=df2.at[index, sl]
       
        return wert   
    
    def LegeZskInfosAn(self):
        datei=self.file_zsk_infos
        ocsv=pd.DataFrame()

        satz=[]
        satz.append('jahr')
        satz.append('name')
        satz.append('wert')
        
        index=0
        for s in satz:
            text=satz[index]
            ocsv[text]=None
            index=index+1

        ocsv[satz] = ocsv[satz].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
    
    def LegeZinskurveTabelleAn(self):
        datei=self.file_zinskurve_tabelle
        ocsv=pd.DataFrame()

        self.satz_zsk_dict.clear()
        satz=[]
        satz.append('datum')
        self.satz_zsk_dict['datum']=None

        satz.append('jahr')
        self.satz_zsk_dict['jahr']=None
        
        #lege die Ueberschiften an:
        for i in range(1,21):
            text='jahr_'+str(i)
            satz.append(text)
            self.satz_zsk_dict[text]=None
        
        for i in range(25, 51, 5):
            text='jahr_'+str(i)
            satz.append(text)
            self.satz_zsk_dict[text]=None
        
        index=0
        for s in satz:
            text=satz[index]
            ocsv[text]=None
            index=index+1
        
        ocsv[satz] = ocsv[satz].astype(str)
        ocsv.to_csv(datei, ';', index=False)

    def LeseZinskurveStart(self):
        #aus der Zisnstrukturkurvetabelle (quelle) werden die relevanten Werte der letzten Jahre ausgelesen
            
        quelle = self.file_zinskurve_start_tabelle

        df_quelle=pd.read_csv(quelle, sep=";")
        df_quelle=df_quelle.sort_values(by='Restlaufzeit', ascending=False)
        row=df_quelle.iloc[0]
        datum_0=row['Restlaufzeit']
        datum_0_jjjj=datum_0[0:4]
        datum_0_mm=datum_0[5:7]
        
        datum_dict={}
        
        datum_index='datum_0'
        datum_wert=datum_0
        
        datum_dict[datum_index]=datum_wert
        
        for i in range(1, self.anzahl_jahre_in_zinsstrukturkurve):
            datum_index='datum_' + str(i)
            
            datum_jjjj=int(datum_0_jjjj)-i
            datum_mm=datum_0_mm
            datum_wert=str(datum_jjjj)+'-'+str(datum_mm)
        
            datum_dict[datum_index]=datum_wert
            
        df_quelle.set_index('Restlaufzeit', inplace=True)
        
        i=0
        for key in datum_dict:
            datum_wert=datum_dict[key]
            row=df_quelle.loc[[datum_wert],:]
            
            datum_jahr_wert = str(int(self.startjahr_Simulation-i-1))
            row['jahr']=datum_jahr_wert

            self.SchreibeRowInSatzDict(row)
            
            i=i+1
            
        self.UmsortierenZinsstrukturKurveStart()

    def UmsortierenZinsstrukturKurveStart(self):
        datei = self.file_zinskurve_tabelle

        df = pd.read_csv(datei, sep=";")
        df = df.sort_values(by='jahr', ascending=True)
        df.set_index('jahr', inplace=True)
        
        df.to_csv(datei, sep=';')
            
    def SchreibeInInfos(self, infos_dict):
        #Es wird in die Tabelle Info reingeschrieben:
        datei = self.file_zsk_infos

        text=''
        index=0
        for key in infos_dict:
            if index==0:
                sep=''
            else:
                sep=';'

            wert = infos_dict.get(key)                
            text=text+sep+str(wert)
            index=index+1
    
        file = open(datei, 'a+')
        file.write(text+'\n')
        file.close()
        
    
    def SchreibeRowInSatzDict(self, row):
        #eine Zeile=row wird in das SatzDict reingeschrieben
        for key in self.satz_zsk_dict:
            
            if key=='datum':
                wert=row.iloc[0].name
            elif key=='jahr':
                wert=row['jahr'][0]
            else:
                name=key
                jahr=name[5:7]
                if jahr == str(1):
                    name=str(jahr) + ' Jahr'
                else:
                    name=str(jahr) + ' Jahre'
                
                wert=row[name][0]
                wert=str(wert).replace(",", ".")
                wert = float(wert)/100    
            
            self.satz_zsk_dict[key]=wert
        
        self.SchreibeSatzDictInCSV()
        
    def SchreibeSatzDictInCSV(self):
        #eine Zeile wird in die (Ziel-)Tabelle reingeschrieben
        ziel = self.file_zinskurve_tabelle
        df = pd.read_csv(ziel, sep=";")
    
        text=''
        index=0
        for key in df:
            if index==0:
                sep=''
            else:
                sep=';'
                
            text=text+sep+str(self.satz_zsk_dict.get(key))
            index=index+1
    
        file = open(ziel, 'a+')
        file.write(text+'\n')
        file.close()
            