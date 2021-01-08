# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import zinsstrukturkurve as zsk
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np


class KA_Renten(object):
        
    def __init__(self, f_dict):
        work_dir = f_dict.get('work_dir') + f_dict.get('sep_dir')
        self.work_dir = work_dir
        file_protokoll = work_dir + 'protokoll_ka_renten.txt'
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_renten_tabelle = work_dir + 'ka_renten.csv'
        self.LegeRentenTabelleAn()

        self.file_renten_sa_tabelle = work_dir + 'ka_sa_renten.csv'
        self.LegeRentenSaTabelleAn()
        
        self.ozsk = zsk.Zinsstrukturkurve(f_dict)
        
        self.file_renten_grafik = work_dir + 'grafik_renten.png'

        self.dtype_dic = { 'jahr':int, 'nr':int, 'von':int, 'bis':int, 'name':str, 'wert':str}
        self.dtype_sa_dic = { 'jahr':int, 'nr':int, 'von':int, 'bis':int, 'name':str, 'wert':str}

    def Init_SA(self, eintrag_dict):
        satz_dict={}

        jahr=eintrag_dict.get('jahr')
        von=str(jahr)+'0101'
        bis=str(jahr)+'1231'
        anzahl=eintrag_dict.get('anzahl')
        
        satz_dict.clear()
        satz_dict['jahr']=jahr
        satz_dict['nr']=999
        satz_dict['von']=von
        satz_dict['bis']=bis
        satz_dict['name']='anzahl'
        satz_dict['wert']=anzahl
        self.SchreibeInRentenSaCSV(satz_dict)

        satz_dict.clear()
        satz_dict['jahr']=jahr
        satz_dict['nr']=999
        satz_dict['von']=von
        satz_dict['bis']=bis
        satz_dict['name']='risiko'
        satz_dict['wert']=eintrag_dict.get('risiko')
        self.SchreibeInRentenSaCSV(satz_dict)
        
        i=0
        name='aufteilung'
        liste=eintrag_dict.get(name)
        for i in range(anzahl):
            wert=liste[i]
            
            satz_dict.clear()
            satz_dict['jahr']=jahr
            satz_dict['nr']=i+1
            satz_dict['von']=von
            satz_dict['bis']=bis
            satz_dict['name']=name
            satz_dict['wert']=wert
            self.SchreibeInRentenSaCSV(satz_dict)

        i=0
        name='laufzeit'
        liste=eintrag_dict.get(name)
        for i in range(anzahl):
            wert=liste[i]
            
            satz_dict.clear()
            satz_dict['jahr']=jahr
            satz_dict['nr']=i+1
            satz_dict['von']=von
            satz_dict['bis']=bis
            satz_dict['name']=name
            satz_dict['wert']=wert
            self.SchreibeInRentenSaCSV(satz_dict)
            
        satz_dict.clear()
        satz_dict['jahr']=jahr
        satz_dict['nr']=999
        satz_dict['von']=von
        satz_dict['bis']=bis
        satz_dict['name']='risiko'
        satz_dict['wert']=eintrag_dict.get('risiko')
        self.ozsk.Init_ZSK(satz_dict)
    
    def ZeichneRenten(self):
        datei=self.file_renten_tabelle
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
        nr=999
        df1=df[(df.nr == nr) & (df.name == 'anfang')]
        jahr=[]
        for i in range(len(df1.index)):
            index=df1.index[i]
            jjjj=int(df1.at[index, 'jahr'])
            jahr.append(jjjj)
            
        anfang=[]
        zugang=[]
        zins=[]
        abgang=[]
        ende=[]
        renten_dict={}

        for i in range(len(jahr)):
            jjjj=jahr[i]
            von=str(jjjj)+'01'+'01'
            bis=str(jjjj)+'12'+'31'
            
            renten_dict['jahr']=jjjj      
            renten_dict['nr']=nr        
            renten_dict['von']=von        
            renten_dict['bis']=bis        
            
            renten_dict['name']='anfang'
            wert = float(self.WertAusRentenTabelle(renten_dict))
            anfang.append(wert)

            renten_dict['name']='zugang'
            wert = float(self.WertAusRentenTabelle(renten_dict))
            zugang.append(wert)

            renten_dict['name']='zins'
            wert = float(self.WertAusRentenTabelle(renten_dict))
            zins.append(wert)

            renten_dict['name']='abgang'
            wert = float(self.WertAusRentenTabelle(renten_dict))
            abgang.append(-wert)
            
            renten_dict['name']='ende'
            wert = float(self.WertAusRentenTabelle(renten_dict))
            ende.append(wert)

        x = np.arange(len(jahr))
        breite_jahr = 1 
        epsilon = 0.1
        
        anzahl_bars=5
        breite_bar = (breite_jahr-epsilon)/anzahl_bars  # the width of the bars
        
        fig, ax = plt.subplots()
        ax.bar(x-(breite_jahr-epsilon)/2 , anfang, breite_bar,label='Anfang')
        ax.bar(x-(breite_jahr-epsilon)/2+breite_bar, zugang, breite_bar, label='Zugang')
        ax.bar(x-(breite_jahr-epsilon)/2+2*breite_bar, zins, breite_bar, label='Zins')
        ax.bar(x-(breite_jahr-epsilon)/2+3*breite_bar, abgang, breite_bar, label='Abgang')
        ax.bar(x-(breite_jahr-epsilon)/2+4*breite_bar, ende, breite_bar, label='Ende')
        
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Werte')
        y_formatter = tick.FormatStrFormatter('%.2f')
        ax.yaxis.set_major_formatter(y_formatter)
        ax.set_title('Entwicklung Renten')
        ax.set_xticks(x)
        ax.grid(color='b', linestyle='dotted')
        ax.set_xticklabels(jahr, rotation=45)
        ax.legend()
        
        fig.tight_layout()

        plt.show()
        file = self.file_renten_grafik
        fig.savefig(file)
    
    def KaufeRenten(self, jahr, betrag):
        renten_dict={}
        
        von=str(jahr)+'01'+'01'
        bis=str(jahr)+'12'+'31'
        
        renten_dict['jahr']=jahr        
        renten_dict['nr']=999        
        renten_dict['von']=von        
        renten_dict['bis']=bis        
        renten_dict['name']='zugang'
        renten_dict['wert']=betrag
        self.SchreibeInRentenCSV(renten_dict)
        
        renten_dict['name']='anzahl'
        anzahl=int(self.LeseRentenSaCSV(renten_dict))
        renten_dict['wert']=anzahl
        self.SchreibeInRentenCSV(renten_dict)

        renten_dict['name']='risiko'
        risiko=self.LeseRentenSaCSV(renten_dict)
        renten_dict['wert']=risiko
        self.SchreibeInRentenCSV(renten_dict)

        i=0
        for i in range(anzahl):
            renten_dict.clear()
            renten_dict['jahr']=jahr        
            renten_dict['nr']=i+1        
            renten_dict['von']=von        
            renten_dict['bis']=bis        
            renten_dict['name']='aufteilung'
            anteil=float(self.LeseRentenSaCSV(renten_dict))
            renten_dict['name']='anteil'
            renten_dict['wert']=anteil
            self.SchreibeInRentenCSV(renten_dict)
            
            betrag_anteil=betrag*anteil
            renten_dict['name']='zugang'
            renten_dict['wert']=betrag_anteil
            self.SchreibeInRentenCSV(renten_dict)
                    
            renten_dict['name']='laufzeit'
            laufzeit=int(self.LeseRentenSaCSV(renten_dict))
            renten_dict['wert']=laufzeit
            self.SchreibeInRentenCSV(renten_dict)

            renten_dict['name']='termin_beginn'
            termin_beginn=von
            renten_dict['wert']=termin_beginn
            self.SchreibeInRentenCSV(renten_dict)

            renten_dict['name']='termin_ende'
            termin_ende = str(jahr+laufzeit-1)+'12'+'31'
            renten_dict['wert']=termin_ende
            self.SchreibeInRentenCSV(renten_dict)
            
            renten_dict['name']='zinssatz'
            jahr_n = 'jahr_'+str(laufzeit)
            zinssatz = self.ozsk.LeseZinskurve(jahr, jahr_n)
            renten_dict['wert']=zinssatz
            self.SchreibeInRentenCSV(renten_dict)
            

    def Beginn(self, jahr):
        
        self.ozsk.Fortschreibung(jahr)
        
        key_dict = {}
        
        von_vj=str(int(jahr-1))+'0101'
        bis_vj=str(int(jahr-1))+'1231'

        von_gj=str(jahr)+'0101'
        bis_gj=str(jahr)+'1231'

        for vektor in self.AnzahlOffenenRenten(jahr-1):
            
            jjjj=int(vektor[0])
            nr = int(vektor[1])

            key_dict.clear()
            key_dict['jahr']=jjjj
            key_dict['nr']=nr
            key_dict['von']=von_vj
            key_dict['bis']=bis_vj
            key_dict['name']='ende'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['name']='anfang'
            key_dict['wert']=wert
            key_dict['von']=von_gj
            key_dict['bis']=bis_gj
            self.SchreibeInRentenCSV(key_dict)

            key_dict['name']='zinssatz'
            key_dict['von']=von_vj
            key_dict['bis']=bis_vj
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['wert']=wert
            key_dict['von']=von_gj
            key_dict['bis']=bis_gj
            self.SchreibeInRentenCSV(key_dict)

            key_dict['von']=von_vj
            key_dict['bis']=bis_vj
            key_dict['name']='termin_beginn'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['wert']=wert
            key_dict['von']=von_gj
            key_dict['bis']=bis_gj
            self.SchreibeInRentenCSV(key_dict)
           
            key_dict['name']='termin_ende'
            key_dict['von']=von_vj
            key_dict['bis']=bis_vj
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['wert']=wert
            key_dict['von']=von_gj
            key_dict['bis']=bis_gj
            self.SchreibeInRentenCSV(key_dict)

    def Fortschreibung(self, jahr):
        
        key_dict = {}
        
        von=int(str(jahr)+'0101')
        bis=int(str(jahr)+'1231')
        
        anfang=0
        zins=0
        zugang=0
        ablauf=0
        ende=0
        
        for vektor in self.AnzahlOffenenRenten(jahr):
            jjjj=int(vektor[0])
            nr = int(vektor[1])
            
            key_dict.clear()
            key_dict['jahr']=jjjj
            key_dict['nr']=nr
            key_dict['von']=von
            key_dict['bis']=bis
            key_dict['name']='zinssatz'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['zinssatz']=wert            

            key_dict['name']='termin_ende'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['termin_ende']=wert            

            key_dict['name']='anfang'
            wert=float(self.WertAusRentenTabelle(key_dict))
            anfang = anfang+wert
            key_dict['anfang']=wert            

            key_dict['name']='zugang'
            wert=float(self.WertAusRentenTabelle(key_dict))
            zugang=zugang+wert
            key_dict['zugang']=wert

            self.SchreibeRenteFort(key_dict)            

            key_dict['name']='zins'
            wert=float(key_dict['zins'])
            zins=zins + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

            key_dict['name']='ende'
            wert = float(key_dict['ende'])
            ende = ende + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

            key_dict['name']='ablauf'
            wert = float(key_dict['ablauf'])
            ablauf = ablauf + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

        for vektor in self.AnzahlAblaufendenRenten(jahr):
            jjjj=int(vektor[0])
            nr = int(vektor[1])
            
            key_dict.clear()
            key_dict['jahr']=jjjj
            key_dict['nr']=nr
            key_dict['von']=von
            key_dict['bis']=bis
            
            key_dict['name']='zinssatz'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['zinssatz']=wert            

            key_dict['name']='anfang'
            wert=float(self.WertAusRentenTabelle(key_dict))
            anfang = anfang+wert
            key_dict['anfang']=wert            

            key_dict['name']='laufzeit_ende'
            wert=self.WertAusRentenTabelle(key_dict)
            key_dict['laufzeit_ende']=wert            

            key_dict['name']='zugang'
            wert=float(self.WertAusRentenTabelle(key_dict))
            zugang=zugang+wert
            key_dict['zugang']=wert
            
            self.SchreibeRenteFort(key_dict)            

            key_dict['name']='zins'
            wert=float(key_dict['zins'])
            zins=zins + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

            key_dict['name']='ende'
            wert = float(key_dict['ende'])
            ende = ende + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

            key_dict['name']='ablauf'
            wert = float(key_dict['ablauf'])
            ablauf = ablauf + wert
            key_dict['wert']=wert
            self.SchreibeInRentenCSV(key_dict)

        key_dict.clear()
        key_dict['jahr']=jahr
        key_dict['nr']=999
        key_dict['von']=von
        key_dict['bis']=bis
            
        key_dict['name']='ablauf'
        key_dict['wert']=ablauf
        self.SchreibeInRentenCSV(key_dict)

        key_dict['name']='anfang'
        key_dict['wert']=anfang
        self.SchreibeInRentenCSV(key_dict)

        key_dict['name']='zugang'
        key_dict['wert']=zugang
        self.SchreibeInRentenCSV(key_dict)

        key_dict['name']='zins'
        key_dict['wert']=zins
        self.SchreibeInRentenCSV(key_dict)

        key_dict['name']='ende'
        key_dict['wert']=ende
        self.SchreibeInRentenCSV(key_dict)
    
    def SchreibeRenteFort(self, key_dict):
        anfang=float(key_dict.get('anfang'))
        zugang=float(key_dict.get('zugang'))
        zinssatz=float(key_dict.get('zinssatz'))
    
        zins=(anfang+zugang)*zinssatz
        
        ablaufdatum=key_dict.get('termin_ende')
        bis_gj=key_dict.get('bis')
        
        if ablaufdatum == bis_gj:
            ablauf=anfang+zugang+zins
        else:
            ablauf=0
        
        ende=anfang+zugang+zins-ablauf
    
        key_dict['zins']=zins            
        key_dict['ende']=ende            
        key_dict['ablauf']=ablauf            
        
        return
    
    def AnzahlOffenenRenten(self, jahr):
        datei=self.file_renten_tabelle
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)

        von = int(str(jahr)+'0101')  
        bis = int(str(jahr)+'1231')  

        datum = str(jahr)+'1231'        
        df1 = df[(df.name=='termin_ende') & (df.von == von) & (df.bis == bis) & (df.wert > datum)]    
    
        d={}
        for index in range(len(df1.index)):
            jahr=int(df1.iloc[index,0])
            nr=int(df1.iloc[index,1])
            d[jahr, nr]='ja'
    
        return d

    def AnzahlAblaufendenRenten(self, jahr):
        datei=self.file_renten_tabelle
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)

        von = int(str(jahr)+'0101')  
        bis = int(str(jahr)+'1231')  

        datum = str(jahr)+'1231'        
        df1 = df[(df.name=='termin_ende') & (df.von == von) & (df.bis == bis) & (df.wert == datum)]    
    
        d={}
        for index in range(len(df1.index)):
            jahr=int(df1.iloc[index,0])
            nr=int(df1.iloc[index,1])
            d[jahr, nr]='ja'
    
        return d
    
    def WertAusRentenTabelle(self, key_dict):
        datei=self.file_renten_tabelle
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
        
        jahr=int(key_dict.get('jahr'))
        nr=int(key_dict.get('nr'))
        von=int(key_dict.get('von'))
        bis=int(key_dict.get('bis'))
        name=str(key_dict.get('name'))
        
        df1 = df[(df.jahr == jahr) & (df.nr == nr) & (df.von == von) &(df.bis == bis) & (df.name == name)]    

        if df1.empty:
            wert=0
            text='ka_renten/WertAusRentenTabelle: Eintrag in der Tabelle fuer Renten nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert   

    
    def LegeRentenTabelleAn(self):
        datei=self.file_renten_tabelle
        ocsv=pd.DataFrame()
        ocsv['jahr']=None
        ocsv['nr']=None
        ocsv['von']=None
        ocsv['bis']=None
        ocsv['name']=None
        ocsv["wert"]=None
        ocsv[['jahr', 'nr', 'von', 'bis', 'name', 'wert']] = ocsv[['jahr', 'nr', 'von', 'bis', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='ka_renten/LegeRentenTabelleAn: Tabelle fuer die Renten wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    def LegeRentenSaTabelleAn(self):
        datei=self.file_renten_sa_tabelle
        ocsv=pd.DataFrame()
        ocsv['jahr']=None
        ocsv['nr']=None
        ocsv['von']=None
        ocsv['bis']=None
        ocsv['name']=None
        ocsv["wert"]=None
        ocsv[['jahr', 'nr', 'von', 'bis', 'name', 'wert']] = ocsv[['jahr', 'nr', 'von', 'bis', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='ka_renten_sa: Tabelle fuer die Renten_SA wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)
        
    def LeseRentenSaCSV(self, key_dict):
        datei=self.file_renten_sa_tabelle
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_sa_dic)
       
        jahr=int(key_dict.get('jahr'))
        nr=int(key_dict.get('nr'))
        von=int(key_dict.get('von'))
        bis=int(key_dict.get('bis'))
        name=str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.nr == nr) & (df.von==von) & (df.bis==bis) & (df.name==name)]
        
        if df1.empty:
            wert=0
            text='ka_renten/LeseRentenSaCSV: Eintrag in der Tabelle fuer Renten nicht gefunden. Es wurde null verwendet: nr='+str(nr)+' von='+str(von)+' bis='+str(bis)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert   

    def ZeileLoeschenInRentenCSV(self, key_dict):
        datei=self.file_renten_tabelle
        
        jahr=int(key_dict.get('jahr'))
        nr=int(key_dict.get('nr'))
        von=int(key_dict.get('von'))
        bis=int(key_dict.get('bis'))
        name=str(key_dict.get('name'))
        
        if self.WertAusRentenTabelle(key_dict) != 0:
            df = pd.read_csv(datei, sep=';', dtype=self.dtype_dic)
            index=df[((df['jahr'] == jahr) & (df['nr'] == nr) & (df['von'] == von) & (df['bis'] == bis) & (df['name'] == name))].index[0]
            df1=df.drop([index], inplace=False)
            df1.to_csv(datei, ';', index=False)
            
            text='ka_renten/ZeileLoeschenInRentenCSV: Eintrag in der Tabelle fuer Renten geloescht: nr='+str(nr)+' von='+str(von)+' bis='+str(bis)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)

    def SchreibeInRentenCSV(self, eintrag_dict):
        datei=self.file_renten_tabelle
        
        jahr=int(eintrag_dict.get('jahr'))
        nr=int(eintrag_dict.get('nr'))
        von=int(eintrag_dict.get('von'))
        bis=int(eintrag_dict.get('bis'))
        
        name=str(eintrag_dict.get('name'))
        wert=str(eintrag_dict.get('wert'))
        
        if self.WertAusRentenTabelle(eintrag_dict) != 0:
            self.ZeileLoeschenInRentenCSV(eintrag_dict)
        
        text=str(jahr)+';'+str(nr)+';'+str(von)+';'+str(bis)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       

    def ZeileLoeschenInRentenSaCSV(self, key_dict):
        datei=self.file_renten_sa_tabelle
        
        jahr=int(key_dict.get('jahr'))
        nr=int(key_dict.get('nr'))
        von=int(key_dict.get('von'))
        bis=int(key_dict.get('bis'))
        name=str(key_dict.get('name'))
        
        if self.LeseRentenSaCSV(key_dict) != 0:
            df = pd.read_csv(datei, sep=';', dtype=self.dtype_sa_dic)
            df1=df[(df['jahr'] != jahr) & (df['nr'] != nr) & (df['von']!=von) & (df['bis']!=bis) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='ka_renten_sa/ZeileLoeschenInRentenSaCSV: Eintrag in der Tabelle fuer Renten_Sa geloescht: jahr='+ str(jahr)+' nr='+str(nr)+' von='+str(von)+' bis='+str(bis)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)


    def SchreibeInRentenSaCSV(self, eintrag_dict):
        datei=self.file_renten_sa_tabelle
        
        jahr=eintrag_dict.get('jahr')
        nr=eintrag_dict.get('nr')
        von=eintrag_dict.get('von')
        bis=eintrag_dict.get('bis')
        
        name=eintrag_dict.get('name')
        wert=eintrag_dict.get('wert')
        
        if self.LeseRentenSaCSV(eintrag_dict) != 0:
            self.ZeileLoeschenInRentenSaCSV(eintrag_dict)
        
        text=str(jahr)+';'+str(nr)+';'+str(von)+';'+str(bis)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       

