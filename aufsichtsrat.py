#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
import protokoll as prot
import pandas as pd
import bilanz as bil


class Aufsichtsrat(QtWidgets.QDialog):

    def __init__(self, f_dict, parent=None):
        super().__init__(parent)
        
        self.work_dir=f_dict.get('work_dir')
        self.file_aufsichtsrat=self.work_dir+'aufsichtsrat.csv'
        self.file_aufsichtsrat_struktur_dict={'jahr':int, 'name':str, 'wert':str}
        self.LegeTabelleAufsichtaratAn()

        file_protokoll=self.work_dir+'protokoll_aufsichtsrat.txt'
        self.oprot = prot.Protokoll(file_protokoll)
       
        self.file_ui=self.work_dir+'aufsichtsrat.ui'
        
        self.mindestverzinsung = 0.04
        self.wobinich = 'hallo'
        self.meinzustand = 'gruen'
        self.stimmung_icon = self.SetztStimmungIcon()

        self.ui = uic.loadUi(self.file_ui, self)

        self.obil = bil.Bilanz(f_dict)
        
        self.startjahr=f_dict.get('Startjahr_Simulation')

    def BestimmeZielerreichung(self, jahr):
        gj=int(jahr)
    
        bil_key_dict={}
        ar_key_dict={}
        
        ar_key_dict.clear()
        ar_key_dict['jahr']=gj
        ar_key_dict['name']='darlehen_ende'
        wert = self.LeseWertAusAufsichtsratCSV(ar_key_dict) 
        if wert == '':
            darlehen_ende = 0
            text='aufsichtsrat/BestimmeZielerreichung: keine Daten zu dem Key: ,' +str(ar_key_dict)+ ' in der Tabelle Aufsitzsrat vorhanden'
            self.oprot.SchreibeInProtokoll(text)
            print(text)
        else:
            darlehen_ende = float(wert)
        
        bil_key_dict.clear()
        bil_key_dict['jahr']=gj
        bil_key_dict['rl']='bilanz'
        bil_key_dict['avbg']='999'
        bil_key_dict['name']='eigenkapital_ende'
        eigenkapital_ende = float(self.obil.LeseBilanzCSV(bil_key_dict))
        ar_key_dict.clear()
        ar_key_dict['jahr']=gj
        ar_key_dict['name']='eigenkapital_ende'
        ar_key_dict['wert']=eigenkapital_ende
        self.SchreibeInAufsichtsratCSV(ar_key_dict) 


        delta_im_eigenkapital=eigenkapital_ende-darlehen_ende
        ar_key_dict.clear()
        ar_key_dict['jahr']=gj
        ar_key_dict['name']='delta_im_eigenkapital'
        ar_key_dict['wert']=delta_im_eigenkapital
        self.SchreibeInAufsichtsratCSV(ar_key_dict) 

        bil_key_dict.clear()
        bil_key_dict['jahr']=gj
        bil_key_dict['rl']='guv'
        bil_key_dict['avbg']='999'
        bil_key_dict['name']='jahresueberschuss'
        jahresueberschuss = float(self.obil.LeseBilanzCSV(bil_key_dict) )
        
        ar_key_dict.clear()
        ar_key_dict['jahr']=gj
        ar_key_dict['name']='jahresueberschuss'
        ar_key_dict['wert']=jahresueberschuss
        self.SchreibeInAufsichtsratCSV(ar_key_dict)
        
        if delta_im_eigenkapital > 0:
            self.meinzustand='gruen'
            return
        
        if delta_im_eigenkapital<= 0:
            self.meinzustand='gelb'
            if eigenkapital_ende<0:
                self.meinzustand = 'gefeuert'
        
    def BestimmeJahresZiele(self, jahr):
        startjahr=int(self.startjahr)
        gj=int(jahr)
    
        bil_key_dict={}
        ar_key_dict={}
        
        if startjahr == gj: #wir sind im ersten Jahr der Simulation
            bil_key_dict.clear()
            bil_key_dict['jahr']=gj-1
            bil_key_dict['rl']='bilanz'
            bil_key_dict['avbg']='999'
            bil_key_dict['name']='eigenkapital_ende'
            wert=self.obil.LeseBilanzCSV(bil_key_dict)
            if wert == '':
                darlehen_beginn = 0
                text='aufsichtsrat/BestimmeJahresZiele: keine Daten zu dem Key: ,' +str(bil_key_dict)+ ' in der Tabelle Bilanz vorhanden'
                self.oprot.SchreibeInProtokoll(text)
                print(text)
            else:
                darlehen_beginn = float(wert)
                
        else:
            ar_key_dict.clear()
            ar_key_dict['jahr']=gj-1
            ar_key_dict['name']='darlehen_ende'
            wert=self.LeseWertAusAufsichtsratCSV(ar_key_dict)
            if wert == '':
                darlehen_beginn = 0
                text='aufsichtsrat/BestimmeJahresZiele: keine Daten zu dem Key: ,' +str(ar_key_dict)+ ' in der Tabelle Aufsichtsrat vorhanden'
                self.oprot.SchreibeInProtokoll(text)
                print(text)
            else:
                darlehen_beginn = float(wert)

        ar_key_dict.clear()
        ar_key_dict['jahr']=gj
        ar_key_dict['name'] ='darlehen_beginn'
        ar_key_dict['wert'] = darlehen_beginn
        self.SchreibeInAufsichtsratCSV(ar_key_dict)
    
        darlehen_ende = (1+self.mindestverzinsung)*darlehen_beginn
        ar_key_dict['name'] ='darlehen_ende'
        ar_key_dict['wert'] = darlehen_ende
        self.SchreibeInAufsichtsratCSV(ar_key_dict)

        ar_key_dict['name'] ='mindestverzinsung'
        ar_key_dict['wert'] = self.mindestverzinsung
        self.SchreibeInAufsichtsratCSV(ar_key_dict)

    def LegeTabelleAufsichtaratAn(self):
        #Hier wird die Tabelle "aufsichtsrat.csv" angelegt
        datei=self.file_aufsichtsrat
        ocsv=pd.DataFrame()
        ocsv["jahr"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv.to_csv(datei, ';', index=False)
    
    def SchreibeInAufsichtsratCSV(self, eintrag):
        datei=self.file_aufsichtsrat
        
        jahr = int(eintrag.get('jahr'))
        name=eintrag.get('name')
        wert=eintrag.get('wert')
        
        text=str(jahr) + ";" + str(name) + ";" + str(wert) + "\n"
        
        f=open(datei, "a")
        f.write(text)    
        f.close()           

    
    def LeseWertAusAufsichtsratCSV(self, f_dict):
        #hier wird ein Wert aus der Tabelle ausgelesen:
        
        datei=self.file_aufsichtsrat
        struktur = self.file_aufsichtsrat_struktur_dict
        
        jahr=int(f_dict.get('jahr'))
        name=f_dict.get('name')
        
        wert=''
        #lese Tabelle:
        df=pd.read_csv(datei, sep=";", dtype=struktur)
        if df.__len__() == 0:
            text='aufsichtsrat/LeseWertAusAufsichtsratCSV: keine Daten zu dem Key: ,' +str(f_dict)+ ' in der Tabelle vorhanden'
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            return wert 
    
        df1=df[(df.jahr == jahr) & (df.name == name)]

        if df1.__len__() > 1:
            text='aufsichtsrat/LeseWertAusAufsichtsratCSV: mehrere Werte zu dem Key: ,' +str(f_dict)+ ' in der Tabelle vorhanden'
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            return wert 
            
        for i in df1.index:
            df2= df1[df1.index==i]
            ii=df2.index[0]
            wert=df2.at[ii,'wert']

        return wert
    
    def SetztStimmungIcon(self):
        if self.meinzustand == 'gruen':
            self.stimmung_icon = self.work_dir+'gruen_icon.png'
        elif self.meinzustand == 'gelb':     
            self.stimmung_icon = self.work_dir+'gelb_icon.png'
        elif self.meinzustand == 'rot':     
            self.stimmung_icon = self.work_dir+'rot_icon.png'
        elif self.meinzustand == 'gefeuert':     
            self.stimmung_icon = self.work_dir+'gefeuert_icon.png'
        else:
            text = 'Aufsichtsrat/SetztStimmungIcon: es konnte kein Icon zugeordnet werden'
            self.oprot.SchreibeInProtokoll(text)
    
    def SetzteWoBinIch(self, text):
        self.wobinich = text

    def GibStimmungFile(self):
        return self.stimmung_icon
        
    def LeseGroesseEinesButtonsAus(self, btn):
        dim_dict={}
        w=btn.width()
        h=btn.height()
        dim_dict['hoehe']=h
        dim_dict['breite']=w
        return dim_dict
    
    def AussageAR(self, jahr):

        file_bild = self.BestimmeBild()
        text = self.BestimmeText(jahr)        
        
        pixmap = QPixmap(file_bild)

        hoehe=self.LeseGroesseEinesButtonsAus(self.label_Mein_Bild).get('hoehe')-20
        breite=self.LeseGroesseEinesButtonsAus(self.label_Mein_Bild).get('breite')-20
        #breite = pixmap.width()
        #hoehe = pixmap.height()
        pixmap.scaled(breite, hoehe)
        self.label_Mein_Bild.setPixmap(pixmap)
        #self.label_Mein_Bild.setScaledContents(True)
        #self.label_Mein_Bild.resize(breite, hoehe)
        

        hoehe=self.LeseGroesseEinesButtonsAus(self.textEdit_Mein_Text).get('hoehe')-10
        breite=self.LeseGroesseEinesButtonsAus(self.textEdit_Mein_Text).get('breite')-10

        self.textEdit_Mein_Text.setText(text)
        self.textEdit_Mein_Text.resize(breite, hoehe)
        
        self.exec_()
        
    def LeseJAB(self):
        pass
    
    def PruefeStimmungAR(self, jahr):
        pass
    
    def BestimmeBild(self):
        
        if self.wobinich == 'hallo':
            file_bild=self.work_dir+'ar_hallo_1.png'
        elif self.wobinich == 'jab':
            if self.meinzustand == 'gruen':
                file_bild=self.work_dir+'ar_jab_gruen_1.png'
            elif self.meinzustand == 'gelb':
                file_bild=self.work_dir+'ar_jab_gruen_1.png'
            elif self.meinzustand == 'rot':
                file_bild=self.work_dir+'ar_jab_gruen_1.png'
            elif self.meinzustand == 'gefeuert':
                file_bild=self.work_dir+'ar_jab_gefeuert_1.png'
            else:
                text = 'Aufsichtsrat/BestimmeBild: es konnte kein passendes Bild zum Zustand zugeordnet werden'
                self.oprot.SchreibeInProtokoll(text)
                
        else:
            text = 'Aufsichtsrat/BestimmeBild: es konnte kein Bild zugeordnet werden'
            self.oprot.SchreibeInProtokoll(text)
            
        
        return file_bild
    
    def BestimmeText(self, jahr):
        
        text = ''
        
        if self.wobinich == 'hallo':
            text = 'Hallo! Ich heisse Rachel. \n' 
            text += 'Ich bin deine Geldgeberin. \n'
            text += 'Arbeite sorgfälltig mit dem Geld. Ich melde mich nach jedem Jahresabschluss. Wir besprechen dann deine Zukunft.\n'
            text += '\n\nIch sehe vielleicht nett aus, bin aber nicht nett. Ich erwarte:\n'
            text += "- eine Mindestverzinsung von meinem Kapital von %5.2f" %(self.mindestverzinsung*100) +'%\n'
            text += '- Meine Geduld für Verluste ist begerntzt. Verlierst Du die Hälfte des Kapitals, bist du gefeuert'
            text += '\n\nDas sind doch klare Regeln. Möge die Macht mit Dir sein.'
        elif self.wobinich == 'jab':
            ar_key_dict={}
        
            ar_key_dict.clear()
            ar_key_dict['jahr']=jahr
            ar_key_dict['name']='darlehen_ende'
            wert = self.LeseWertAusAufsichtsratCSV(ar_key_dict) 
            if wert == '':
                darlehen_ende = 0
                text='aufsichtsrat/BestimmeText: keine Daten zu dem Key: ,' +str(ar_key_dict)+ ' in der Tabelle Aufsitzsrat vorhanden'
                self.oprot.SchreibeInProtokoll(text)
                print(text)
            else:
                darlehen_ende = float(wert)

            
            text = 'Oh! Der Jahresabschluss ist da.\n'
            text +='Wir haben vereinbart, dass das Eigenkapital mindestens %.2f' %darlehen_ende +' beträgt \n'
            
            ar_key_dict['name']='eigenkapital_ende'
            wert = self.LeseWertAusAufsichtsratCSV(ar_key_dict) 
            if wert == '':
                eigenkapital_ende = 0
                text_1='aufsichtsrat/BestimmeText: keine Daten zu dem Key: ,' +str(ar_key_dict)+ ' in der Tabelle Aufsitzsrat vorhanden'
                self.oprot.SchreibeInProtokoll(text_1)
                print(text)
            else:
                eigenkapital_ende = float(wert)
            
            text +='Du hast %.2f' %eigenkapital_ende +' erreicht. \n'
            
            if eigenkapital_ende >= darlehen_ende:
                text +='Ich bin zufrieden mit dir. Weiter so!\n'
                return text

            if eigenkapital_ende < darlehen_ende:
                if eigenkapital_ende > 0:
                    text +='Strenge dich an. Sonst wird es ungemütlich mit uns beiden.\n'
                    return text
                else:
                    text +='Du bist gefeuert!!!\n'
                    return text
            
        else:
            text = 'Aufsichtsrat/BestimmeText: es konnte kein Text zugeordnet werden'
            self.oprot.SchreibeInProtokoll(text)

        return text