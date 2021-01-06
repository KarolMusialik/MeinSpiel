#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
import pandas as pd
import protokoll as prot

class SystemDialogVertrag(QtWidgets.QDialog):

    def __init__(self, f_dict, parent=None):
        super().__init__(parent)
        
        work_dir=f_dict.get('work_dir')
        file_protokoll=work_dir+'protokoll_system_dialig_vertrag.txt'
        self.oprot = prot.Protokoll(file_protokoll)
       
        self.file_ui=work_dir+'dialog_vertraege.ui'
        
        self.file_system_bestand=f_dict.get('file_system_bestand')
        self.file_system_fortschreibung=f_dict.get('file_system_fortschreibung')
        self.file_system_bestand_struktur_dict=f_dict.get('file_system_bestand_struktur')
        self.file_system_fortschreibung_struktur_dict=f_dict.get('file_system_fortschreibung_struktur')

    def ZeigeAlleVertraege(self):
        self.ui = uic.loadUi(self.file_ui, self)

        self.treeWidget_Liste_Vertraege.setHeaderLabels(['Vertragsnummer', 'Wert'])
        
        liste = self.BestimmeListeDerVertraege()
        
        self.treeWidget_Liste_Vertraege.itemClicked.connect(self.LadeFortschreibungenZumVertrag)
        
        for vsnr in liste:
            wert=[]
            wert.append(vsnr)
            t=QtWidgets.QTreeWidgetItem(self.treeWidget_Liste_Vertraege, wert)
            
            eintraege = self.LeseVertargAusBestand(vsnr)
            for key, value in eintraege.items():
                ver=[key, value]
                w=QtWidgets.QTreeWidgetItem(t, ver)
        
        self.exec_()
        
    def BestiemmeDieFortschreibungen(self, vsnr):
        #hier werden die keys aus der Fortschreibung für die übergebende vsnr ermittelt:
        
        datei=self.file_system_fortschreibung
        struktur = self.file_system_fortschreibung_struktur_dict

        fort_dict={} #darin werden die keys aus der Fortschreibung abgelegt       
        anzahl=0
        
        #lese Fortschreibung:
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        if df.__len__() == 0:
            text='System_Dialog_Vertrag/BestiemmeAnzahlDerFortschreibungen: keine Verträge in der Fortschreibung vorhanden'
            self.oprot.SchreibeInProtokoll(text)
            return fort_dict
        
        df1=df[df.vsnr == vsnr]
        df2=df1[['vsnr','histnr', 'von', 'bis']].groupby(by=['vsnr','histnr']).first()    
        df3=df2.reset_index()
        
        for i in df3.index:
                ii=df3.index[0]
                histnr=df3.at[ii,'histnr']
                von=df3.at[ii,'von']
                bis=df3.at[ii,'bis']
                anzahl += 1
                histnr_str='histnr_'+str(anzahl)
                von_str='von_'+str(anzahl)
                bis_str='bis_'+str(anzahl)
                fort_dict[histnr_str]=histnr
                fort_dict[von_str]=von
                fort_dict[bis_str]=bis
        
        fort_dict['anzahl']=anzahl
        fort_dict['vsnr']=vsnr
        
        return fort_dict

    def LeseVertargAusFortschreibung(self, f_dict):
        datei=self.file_system_fortschreibung
        struktur = self.file_system_fortschreibung_struktur_dict
        vsnr=f_dict.get('vsnr')
        histnr=f_dict.get('histnr')
        von=f_dict.get('von')
        bis=f_dict.get('bis')
        
        eintraege = {}

        #lese Fortschreibung:
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        if df.__len__() == 0:
            text='System_Dialog_Verrtrag/LeseVertargAusFortschreibung: keine Daten in der Fortschreibung vorhanden'
            self.oprot.SchreibeInProtokoll(text)
            return eintraege 
    
        df1=df[(df.vsnr == vsnr) & (df.histnr == histnr) & (df.von == von) & (df.bis == bis)]
            
        for i in df1.index:
            df2= df1[df1.index==i]
            ii=df2.index[0]
            name=df2.at[ii,'name']
            wert=df2.at[ii,'wert']
                
            eintraege[name]=wert

        return eintraege

    def LegeDenBaumDerFortschreibung(self, fort_dict):
        # hier wird der Baum aus der Fortschreibung aufgestellt:
        
        anzahl=fort_dict.get('anzahl') #Anzahl der Fortschreibungen für den Vertrag
        vsnr=fort_dict.get('vsnr') #Vertragsnummen
        
        self.treeWidget_Liste_Fortschreibungen.setHeaderLabels(['Fortschreigung', 'Wert'])
        
        if anzahl==0:
            return
        
        vertrag_dict ={} #hier wird der Key für einen Vertrag abgelegt, mit dem in der Fortschreibung ausgelesen wird
        
        for i in range(anzahl):
            
            vertrag_dict.clear()
            histnr_str='histnr_'+str(i+1)
            von_str='von_'+str(i+1)
            bis_str='bis_'+str(i+1)

            text=histnr_str+'/'+von_str+'/'+bis_str
            knotenname=[]
            knotenname.append(text)
            
            histnr = fort_dict.get(histnr_str)
            von = fort_dict.get(von_str)
            bis = fort_dict.get(bis_str)

            vertrag_dict['vsnr']=vsnr
            vertrag_dict['histnr']=histnr
            vertrag_dict['von']=von
            vertrag_dict['bis']=bis

            ebene_1=QtWidgets.QTreeWidgetItem(self.treeWidget_Liste_Fortschreibungen, knotenname) #Name in dem Baumknoten

            eintraege = self.LeseVertargAusFortschreibung(vertrag_dict) #Alle Einträge zu dem Key, die unter dem Baumknoten dargestellt werden sollen:
            for key, value in eintraege.items():
                ver=[key, value]
                w=QtWidgets.QTreeWidgetItem(ebene_1, ver)            


    def LadeFortschreibungenZumVertrag(self, it, col):
        vsnr=it.text(col) 
        
        self.treeWidget_Liste_Fortschreibungen.clear() #lösche alle Einträge im Baum der Fortschreibungen
        fort_dict={} #keys in der Fortschreibung für eine vorgegebene vsnr
        fort_dict = self.BestiemmeDieFortschreibungen(vsnr) #hier werden die keys ermittelt
        
        self.LegeDenBaumDerFortschreibung(fort_dict)
    
    def LeseVertargAusBestand(self, vsnr):
        datei=self.file_system_bestand
        struktur = self.file_system_bestand_struktur_dict
        
        eintraege = {}

        #lese Bestand:
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        if df.__len__() == 0:
            text='System_Dialog_Verrtrag/LeseVertargAusBestand: keine Verträge in der Bestandsdatei vorhanden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            df1=df[df.vsnr == vsnr]
            
            for i in df1.index:
                df2= df1[df1.index==i]
                ii=df2.index[0]
                name=df2.at[ii,'name']
                wert=df2.at[ii,'wert']
                
                eintraege[name]=wert

        return eintraege
    
    def BestimmeListeDerVertraege(self):
        
        datei=self.file_system_bestand
        struktur = self.file_system_bestand_struktur_dict
        
        #lese Bestand:
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        
        liste = []
        
        if df.__len__() == 0:
            text='System_Dialog_Verrtrag/BestimmeListeDerVertraege: keine Verträge in der Bestandsdatei vorhanden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            df1=df[df.name == 'vsnr']['vsnr']
 
            for vsnr in df1:
                liste.append(vsnr)

        return liste
    
    

