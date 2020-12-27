#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import protokoll as prot
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy

class Statistik(object):

    def __init__(self, f_dict):
        
        work_dir=f_dict.get('work_dir')
        file_protokoll=work_dir+'protokoll_system_statistik.txt'
        self.oprot = prot.Protokoll(file_protokoll)
        
        self.file_system_bestand=f_dict.get('file_system_bestand')
        self.file_system_bestand_struktur=f_dict.get('file_system_bestand_struktur')

        self.file_statistik=f_dict.get('file_system_statistik')
        self.file_statistik_beschreibung=f_dict.get('file_system_statistik_beschreibung')
        
        self.grafik_file_statistik_anzahl = f_dict.get('grafik_file_statistik_anzahl')
        self.grafik_file_statistik_jsb = f_dict.get('grafik_file_statistik_jsb')
        
        self.dtype_statistik_dict= { 'von':int, 'bis':int, 'produkt':int, 'position':str, 'vsnr':int, 'histnr':int, 'name':str, 'wert':float}

    def ErstelleStatistik(self, von, bis):
        self.Anfang(von, bis)
        self.Zugang(von, bis)
        self.Abgang(von, bis)
        self.Ende(von, bis)
        self.CheckeStatistik(von, bis)
        self.ZeichneStatistik('anzahl', self.grafik_file_statistik_anzahl)
        self.ZeichneStatistik('jsb', self.grafik_file_statistik_jsb)
        
    def ZeichneStatistik(self, opt, file_picture):
        #es werden Übersichten für die Statistik erstellt:
        datei=self.file_statistik
        
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_statistik_dict)

        col_labels = []
        row_labels = ['Anfang', 'Zugang', 'Abgang', 'Ende']

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        #es werden nur anzahlen betrachtet
        df1=df[(df.name==opt)].groupby('bis', as_index=False).count()
        df2=df1[['bis']]
    
        for index, row in df2.iterrows():
            bis=str(row['bis'])
            jahr=bis[0:4]
            col_labels.append(jahr)
    
        value={}
        value_dict={}
        name=opt
        for jahr in col_labels:
            value_dict.clear()
            value_dict['jahr']=jahr
            value_dict['von']=jahr+'0101'
            value_dict['bis']=jahr+'1231'
            
            for position in row_labels:
                value_dict['position']=position.lower()
    
                von=int(value_dict.get('von'))
                bis=int(value_dict.get('bis'))
                pos=value_dict.get('position')
                
                df1=df[((df.name==name) & (df.von==von) & (df.bis==bis) & (df.position==pos))]
                df2=df1[['von', 'bis', 'position', 'name', 'wert']].groupby(['von', 'bis', 'position', 'name'], as_index=False).sum()
                
                if df2.__len__() == 0:
                    #keine Werte gefunden. Es ist nicht schlim. Es kann schon sein:
                    wert=0
                else:
                    if df2.__len__() > 1:
                        #es dürfen nicht mehr als ein wert sein. Also fehler:
                        text = 'Statistik/ZeichneStatistik: es wurde mehr als nur ein Wert gefunden. das kein nicht sein!: ' + str(value_dict)
                        self.oprot.SchreibeInProtokoll(text)
                    else:
                        index=df2['wert'].index[0]
                        wert=df2.at[index, 'wert']

                value_dict[position]=wert
            
            value[jahr]=deepcopy(value_dict)
        
        #Tabelleneinträge:
        table_vals = []
        row = []
        spalte=-1
        zeile=-1
        for position in row_labels:
            zeile +=1
            row.clear()
            for jahr in col_labels:
                spalte +=1
                wert=value.get(jahr).get(position)
                row.append(wert)

            table_vals.append(deepcopy(row))
        
        # Zeichne Tabelle:
        fig, ax = plt.subplots(1,1)        
        
        ax.axis('off')
        #the_table = plt.table(cellText=table_vals,rowLabels=row_labels,colLabels=col_labels,loc='center')
        tabelle = ax.table(cellText=table_vals,
                           rowLabels=row_labels,
                           colLabels=col_labels,
                           loc='center')
        tabelle.scale(1,2.0)
        #the_table.auto_set_font_size(False)
        
        # Removing ticks and spines enables you to get the figure only with table
        #plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        #plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
        #for pos in ['right','top','bottom','left']:
            #plt.gca().spines[pos].set_visible(False)

        
        #plt.savefig(file_picture, bbox_inches='tight', pad_inches=0.05)
        plt.savefig(file_picture)
        
    def CheckeStatistik(self, von, bis):
        datei=self.file_statistik
        
        df=pd.read_csv(datei, sep=";")
        
        df1 = df[(df.von == int(von)) & (df.bis == int(bis))]
        
        #list = df1.values.tolist()

    def Ende(self, von, bis):
        bestand=self.file_system_bestand        
        struktur_dict=self.file_system_bestand_struktur

        df=pd.read_csv(bestand, sep=";", dtype=struktur_dict)
        
        df1 = df[(df.von <= int(bis)) & (df.bis >= int(bis))][['vsnr', 'histnr', 'von', 'bis']]
        
        df2=df1.groupby(['vsnr', 'histnr', 'von', 'bis'])

        key={}
        eintrag={}
        for index in df2.groups:
            
            key.clear()
            key['vsnr']=index[0]
            key['histnr']=index[1]
            key['von']=index[2]
            key['bis']=index[3]
            
            produkt = self.LeseWertAusBestandCSV(key, 'tkz')
            anzahl = self.LeseWertAusBestandCSV(key, 'anzahl')
            jsb = self.LeseWertAusBestandCSV(key, 'bruttojahresbeitrag')
            vs = self.LeseWertAusBestandCSV(key, 'versicherungssumme')
            
            eintrag.clear()
            eintrag['von']=von
            eintrag['bis']=bis
            eintrag['produkt']=produkt
            eintrag['position']='ende'
            eintrag['vsnr']=key.get('vsnr')
            eintrag['histnr']=key.get('histnr')
            
            eintrag['name']='anzahl'
            eintrag['wert']=anzahl
            self.SchreibeInStatistikCSV(eintrag)

            eintrag['name']='jsb'
            eintrag['wert']=jsb
            self.SchreibeInStatistikCSV(eintrag)
            
            eintrag['name']='vs'
            eintrag['wert']=vs
            self.SchreibeInStatistikCSV(eintrag)

    def Abgang(self, von, bis):
        bestand=self.file_system_bestand        
        struktur_dict=self.file_system_bestand_struktur

        df=pd.read_csv(bestand, sep=";", dtype=struktur_dict)
        
        df1=df.groupby(['vsnr'])

        bis_jjjj=str(bis)
        bis_jjjj=bis_jjjj[:4]
        bis_jjjj=int(bis_jjjj)        
        
        key={}
        eintrag={}
        
        alle_daten_dict={}

        for vsnr in df1.groups:
            vertrag_ablauf=False
            alle_daten_dict.clear
            alle_daten_dict=df[(df.vsnr==vsnr)].groupby(['vsnr', 'histnr', 'von', 'bis']).groups

            for satz in alle_daten_dict:
                vsnr_histnr = satz[1]
                vsnr_von = satz[2]
                vsnr_bis = satz[3]
                vsnr_bis_jjjj=str(vsnr_bis)
                vsnr_bis_jjjj=vsnr_bis_jjjj[:4]
                vsnr_bis_jjjj=int(vsnr_bis_jjjj)               
                if (vsnr_bis_jjjj == bis_jjjj):
                    vertrag_ablauf=True
                    bis_vertrag=vsnr_bis
                    von_vertrag=vsnr_von
                    histnr_vertrag=vsnr_histnr

            
            if vertrag_ablauf == True:
                key.clear()
                key['vsnr']=vsnr
                key['histnr']=histnr_vertrag
                key['von']=von_vertrag
                key['bis']=bis_vertrag
            
                produkt = self.LeseWertAusBestandCSV(key, 'tkz')
                anzahl = self.LeseWertAusBestandCSV(key, 'anzahl')
                jsb = self.LeseWertAusBestandCSV(key, 'bruttojahresbeitrag')
                vs = self.LeseWertAusBestandCSV(key, 'versicherungssumme')
                
                eintrag.clear()
                eintrag['von']=von
                eintrag['bis']=bis
                eintrag['produkt']=produkt
                eintrag['position']='abgang'
                eintrag['vsnr']=key.get('vsnr')
                eintrag['histnr']=key.get('histnr')
                
                eintrag['name']='anzahl'
                eintrag['wert']=anzahl
                self.SchreibeInStatistikCSV(eintrag)
    
                eintrag['name']='jsb'
                eintrag['wert']=jsb
                self.SchreibeInStatistikCSV(eintrag)
                
                eintrag['name']='vs'
                eintrag['wert']=vs
                self.SchreibeInStatistikCSV(eintrag)
    
    def Zugang(self, von, bis):
        bestand=self.file_system_bestand        

        df=pd.read_csv(bestand, sep=";")
        
        df1 = df[(df.von >= int(von)) & (df.name == 'gevo')& (df.wert == 'Neuzugang')][['vsnr', 'histnr', 'von', 'bis']]
        daten_list = df1.values.tolist()
        
        key={}
        eintrag={}
        for index in daten_list:
            
            key.clear()
            key['vsnr']=index[0]
            key['histnr']=index[1]
            key['von']=index[2]
            key['bis']=index[3]
            
            produkt = self.LeseWertAusBestandCSV(key, 'tkz')
            anzahl = self.LeseWertAusBestandCSV(key, 'anzahl')
            jsb = self.LeseWertAusBestandCSV(key, 'bruttojahresbeitrag')
            vs = self.LeseWertAusBestandCSV(key, 'versicherungssumme')
            
            eintrag.clear()
            eintrag['von']=von
            eintrag['bis']=bis
            eintrag['produkt']=produkt
            eintrag['position']='zugang'
            eintrag['vsnr']=key.get('vsnr')
            eintrag['histnr']=key.get('histnr')
            
            eintrag['name']='anzahl'
            eintrag['wert']=anzahl
            self.SchreibeInStatistikCSV(eintrag)

            eintrag['name']='jsb'
            eintrag['wert']=jsb
            self.SchreibeInStatistikCSV(eintrag)
            
            eintrag['name']='vs'
            eintrag['wert']=vs
            self.SchreibeInStatistikCSV(eintrag)

    def SchreibeInStatistikCSV(self, eintrag):
        datei=self.file_statistik
        
        vsnr = eintrag.get('vsnr')
        histnr = eintrag.get('histnr')
        von = eintrag.get('von')
        bis = eintrag.get('bis')
        produkt = eintrag.get('produkt')
        position = eintrag.get('position')
    
        name=eintrag.get('name')
        wert=eintrag.get('wert')
        
        text=str(von) + ";" + str(bis) + ";" + str(produkt) + ";" + str(position) + ";" + str(vsnr)+ ";" + str(histnr)+ ";" + str(name) + ";" + str(wert) + "\n"
        
        f=open(datei, "a")
        f.write(text)    
        f.close()           
    
    def Anfang(self, von, bis):
        statistik=self.file_statistik
        
        von_dict=self.DictAusDatum(str(von))
        jahr_vj=int(von_dict.get('jahr'))-1
        bis_vj=str(jahr_vj)+'12'+'31'
        
        df=pd.read_csv(statistik, sep=";")
        
        df1 = df[(df.bis == int(bis_vj)) & (df.position == 'ende')]
        
        daten_list = df1.values.tolist()

        if df1.__len__() == 0:
            text = 'System/StatistikAnfangsbestand: in der Statistik ' +statistik+ ' zum Termin: ' +bis_vj+ ' wurden keine Daten gefunden. Das muss aber kein Fefler sein. Vielleicht gibt es keine Vorjahresdaten.'
            self.oprot.SchreibeInProtokoll(text)
        else:
            key={}            
            eintrag={}
            for index in daten_list:
            
                key.clear()
                key['von']=index[0]
                key['bis']=index[1]
                key['produkt']=index[2]
                key['position']=index[3]
                key['vsnr']=index[4]
                key['histnr']=index[5]
                key['name']=index[6]
                key['wert']=index[7]
                
                eintrag.clear()
                eintrag['von']=von
                eintrag['bis']=bis
                eintrag['produkt']=key.get('produkt')
                eintrag['position']='anfang'
                eintrag['vsnr']=key.get('vsnr')
                eintrag['histnr']=key.get('histnr')
                
                eintrag['name']=key.get('name')
                eintrag['wert']=key.get('wert')
                self.SchreibeInStatistikCSV(eintrag)
       
    def LeseWertAusBestandCSV(self, key, name):
        datei=self.file_system_bestand
        df=pd.read_csv(datei, sep=";")
        
        vsnr = str(key.get('vsnr'))
        histnr = str(key.get('histnr'))
        von = str(key.get('von'))
        bis = str(key.get('bis'))
        
        df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']] = df[['vsnr', 'histnr', 'von', 'bis', 'name', 'wert']].astype(str)
        
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis) & (df.name == name)]
        
        if df1.empty:
            wert=0
            text = 'Statistik/LeseWertAusBestandCSV: in der Bestandstabelle: ' +datei+ ' mit der vsnr: ' +vsnr+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert       
    
    def LeseWertAusStatistikCSV(self, key, name):
        datei=self.file_statistik
        df=pd.read_csv(datei, sep=";")
        
        produkt = str(key.get('produkt'))
        position = str(key.get('position'))
        vsnr = str(key.get('vsnr'))
        histnr = str(key.get('histnr'))
        von = str(key.get('von'))
        bis = str(key.get('bis'))
        
        df1 = df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis)& (df.produkt == produkt)& (df.position == position) & (df.name == name)]
        
        if df1.empty:
            wert=0
            text = 'Statistik/LeseWertAusStatistikCSV: in der Bestandstabelle: ' +datei+ ' mit der vsnr: ' +vsnr+ ' wurden für den namen: '+name+ 'keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert       
    
    
    def DictAusDatum(self, datum):
        jahr=datum[0:4]
        monat=datum[4:6]
        tag=datum[6:8]
        dic={}
        dic['jahr']=jahr
        dic['monat']=monat
        dic['tag']=tag
        return dic