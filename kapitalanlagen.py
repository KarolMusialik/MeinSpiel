# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import ka_renten as ka_rente

class Kapitalanlagen:
        
    def __init__(self, f_dict):
        work_dir = f_dict.get('work_dir')+f_dict.get('sep_dir')
        file_protokoll = work_dir+'protokoll_kapitalanlagen.txt'
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_kapitalanlagen = work_dir+'kapitalanlagen.csv'
        self.file_renten_tabelle = work_dir+'ka_renten.csv'
        self.file_aktien_tabelle = work_dir+'ka_aktien.csv'
        self.file_sa_tabelle = work_dir+'ka_sa.csv'
        
        self.file_bilanz = f_dict.get('file_bilanz')

        self.oka_renten = ka_rente.KA_Renten(f_dict)
        
        self.LegeKapitalanlagenAn()
        
        self.LegeAktienTabelleAn()
        self.LegeSATabelleAn()

        
    def Init_KA(self, jahr):
        pass
        
    def Init_SA(self, eintrag_dict):
        jahr=eintrag_dict.get('jahr')
        
        satz={}
        satz_renten={}
        satz_renten = eintrag_dict.get('renten')
        self.oka_renten.Init_SA(satz_renten)
        
        name='renten'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='anteil_aktien'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='anteil_renten'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='vola_aktien'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()
        
    def ZeichneKapitalanlagen(self, jahr):
        self.oka_renten.ZeichneRenten()
    
    def Fortschreibung(self, jahr):
        self.oka_renten.Fortschreibung(jahr)
        
        key_dict={}
        key_renten_dict={}
        
        von = int(str(jahr)+'0101')
        bis = int(str(jahr)+'1231')
        
        key_renten_dict['jahr']=jahr
        key_renten_dict['nr']=999
        key_renten_dict['von']=von
        key_renten_dict['bis']=bis

        key_renten_dict['name']='ende'
        wert = self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        
        name='ende'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='zins'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='zins'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='zugang'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='zugang'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='ablauf'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='ablauf'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.SchreibeInKapitalanlagenCSV(key_dict)


    def LeseSACSV(self, key_dict):
        datei=self.file_sa_tabelle
        df=pd.read_csv(datei, sep=";")
        df[['jahr', 'name', 'wert']] = df[['jahr', 'name', 'wert']].astype(str)
       
        jahr=key_dict.get('jahr')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == str(jahr)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='kapitalanlagen/LeseSACSV: kein Eintrag in der Tabelle gefunden. Es wurde null verwendet'+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1['wert'][index]
   
        return wert   
        
    def ZeileLoeschenInSACSV(self, key_dict):
        datei=self.file_sa_tabelle
        
        jahr=key_dict.get('jahr')
        name=key_dict.get('name')
        
        if self.LeseSACSV(key_dict) != 0:
            df = pd.read_csv(datei, sep=';')
            df1=df[(df['jahr'] != jahr) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='Kapitalanlage: Eintrag in der Tabelle SA geloescht: jahr='+str(jahr)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)

    def SchreibeInSACSV(self, eintrag_dict):
        datei=self.file_sa_tabelle
        
        jahr=eintrag_dict.get('jahr')
        name=eintrag_dict.get('name')
        wert=eintrag_dict.get('wert')
        
        if self.LeseSACSV(eintrag_dict) != 0:
            self.ZeileLoeschenInSACSV(eintrag_dict)
        
        text=str(jahr)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       
        
    def LegeKapitalanlagenAn(self):
        datei=self.file_kapitalanlagen
        ocsv=pd.DataFrame()
        ocsv["jahr"]=None
        ocsv["topf"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv[['jahr', 'topf','name', 'wert']] = ocsv[['jahr', 'topf','name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Kapitalanlegen: Tabelle fuer die Kapitalanlagen wurde angelegt: '+str(self.file_kapitalanlagen)
        self.oprot.SchreibeInProtokoll(text)

    def LegeAktienTabelleAn(self):
        datei=self.file_aktien_tabelle
        ocsv=pd.DataFrame()
        ocsv['jahr']=None
        ocsv['von']=None
        ocsv['bis']=None
        ocsv['status']=None
        ocsv['name']=None
        ocsv["wert"]=None
        ocsv[['jahr', 'von', 'bis', 'status','name', 'wert']] = ocsv[['jahr', 'von', 'bis', 'status','name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Kapitalanlegen: Tabelle fuer die Aktien wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)
    
    def LeseAktienCSV(self, key_dict):
        datei=self.file_aktien_tabelle
        df=pd.read_csv(datei, sep=";")
        df[['jahr', 'von', 'bis', 'status', 'name', 'wert']] = df[['jahr', 'von', 'bis', 'status', 'name', 'wert']].astype(str)
       
        jahr=key_dict.get('jahr')
        von=key_dict.get('von')
        bis=key_dict.get('bis')
        status=key_dict.get('status')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == str(jahr)) & (df.von==str(von)) & (df.bis==str(bis)) & (df.status==str(status)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
        else:
            wert=df1['wert'].get_values()[0]
       
        return float(wert)   

    def ZeileLoeschenInAktienCSV(self, key_dict):
        datei=self.file_aktien_tabelle
        
        jahr=key_dict.get('jahr')
        von=key_dict.get('von')
        bis=key_dict.get('bis')
        status=key_dict.get('status')
        name=key_dict.get('name')
        
        if self.LeseAktienCSV(key_dict) != 0:
            df = pd.read_csv(datei, sep=';')
            df1=df[(df['jahr'] != jahr) & (df['von']!=von) & (df['bis']!=bis) & (df['status']!=status) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='Kapitalanlage: Eintrag in der Bilanztabelle geloescht: jahr='+str(jahr)+' von='+str(von)+' bis='+str(bis)+' status='+str(status)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)

    def SchreibeInAktienCSV(self, eintrag_dict):
        datei=self.file_aktien_tabelle
        
        jahr=eintrag_dict.get('jahr')
        von=eintrag_dict.get('von')
        bis=eintrag_dict.get('bis')
        status=eintrag_dict.get('status')
        
        name=eintrag_dict.get('name')
        wert=eintrag_dict.get('wert')
        
        if self.LeseAktienCSV(eintrag_dict) != 0:
            self.ZeileLoeschenInAktienCSV(eintrag_dict)
        
        text=str(jahr)+';'+str(von)+';'+str(bis)+';'+str(status)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       

    def LegeSATabelleAn(self):
        datei=self.file_sa_tabelle
        ocsv=pd.DataFrame()
        ocsv['jahr']=None
        ocsv['name']=None
        ocsv["wert"]=None
        ocsv[['jahr', 'name', 'wert']] = ocsv[['jahr', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Kapitalanlegen: Tabelle fuer die SA wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    def Beginn(self, jahr):
        self.oka_renten.Beginn(jahr)
        
        key_dict={}
        key_ka_dict={}
        key_renten_dict={}
        
        name='kasse_anfang'
        key_dict['rl']='bilanz'
        key_dict['name']=name
        key_dict['jahr']=jahr
        key_dict['avbg']='999'
        kasse_anfang=self.LeseBilanzCSV(key_dict)
        
        key_ka_dict['jahr']=jahr
        key_ka_dict['name']=name
        key_ka_dict['topf']='999'
        key_ka_dict['wert']=kasse_anfang
        self.SchreibeInKapitalanlagenCSV(key_ka_dict)
        
        name='umbuchung_von_kasse_zu_ka_zugang'
        key_ka_dict['jahr']=jahr
        key_ka_dict['name']=name
        key_ka_dict['topf']='999'
        key_ka_dict['wert']=kasse_anfang
        self.SchreibeInKapitalanlagenCSV(key_ka_dict)
        
        bis_vj = str(int(jahr-1))+'1231'
        von_vj = str(int(jahr-1))+'0101'
        
        key_renten_dict['jahr']=int(jahr)-1
        key_renten_dict['nr']=999
        key_renten_dict['von']=von_vj
        key_renten_dict['bis']=bis_vj
        key_renten_dict['name']='ende'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='anfang'
        key_ka_dict['jahr']=jahr
        key_ka_dict['name']=name
        key_ka_dict['topf']='renten'
        key_ka_dict['wert']=wert
        self.SchreibeInKapitalanlagenCSV(key_ka_dict)

        self.UmschichteKapitalanlagen(jahr)
    
    def UmschichteKapitalanlagen(self, jahr):
        ka_dict={}
        ka_renten_dict={}
        ka_aktien_dict={}
        sa_dict={}
        
        ka_dict['jahr']=jahr
        ka_dict['name']='umbuchung_von_kasse_zu_ka_zugang'
        ka_dict['topf']='999'
        umbuchung=self.LeseKapitalanlageCSV(ka_dict)

        ka_dict['jahr']=jahr
        ka_dict['name']='anfang'
        ka_dict['topf']='999'
        ka_dict['topf']='renten'
        ka_renten_anfang=self.LeseKapitalanlageCSV(ka_dict)

        ka_dict['jahr']=jahr
        ka_dict['name']='anfang'
        ka_dict['topf']='aktien'
        ka_aktien_anfang=self.LeseKapitalanlageCSV(ka_dict)
    
        sa_dict['jahr']=jahr
        sa_dict['name']='anteil_renten'
        anteil_renten=float(self.LeseSACSV(sa_dict))
        sa_dict.clear()        

        sa_dict['jahr']=jahr
        sa_dict['name']='anteil_aktien'
        anteil_aktien=float(self.LeseSACSV(sa_dict))
        sa_dict.clear()        
        
        ka_anfang=ka_renten_anfang+ka_aktien_anfang+umbuchung
        umbuchung_renten=anteil_renten*umbuchung
        umbuchung_aktien=anteil_aktien*umbuchung
        
        max_betrag_aktien=anteil_aktien*ka_anfang
        if ka_aktien_anfang+umbuchung_aktien <= max_betrag_aktien:
            #man kann noch mehr zu aktien verschieben:
            verschiebung_zu_aktien=max(max_betrag_aktien-(ka_aktien_anfang+umbuchung_aktien), 0)
            umbuchung_renten= umbuchung_renten-verschiebung_zu_aktien
            umbuchung_aktien= umbuchung_aktien+verschiebung_zu_aktien
        else:
            #zu viel Aktien. Reduktion erforderilch:
            verschiebung_zu_renten=ka_aktien_anfang+umbuchung_aktien-max_betrag_aktien
            umbuchung_renten= umbuchung_renten+verschiebung_zu_renten
            umbuchung_aktien= umbuchung_aktien-verschiebung_zu_renten
            
        ka_renten_anfang_nach_reallokation=ka_renten_anfang+umbuchung_renten
        ka_aktien_anfang_nach_reallokation=ka_aktien_anfang+umbuchung_aktien
        
        #Schreibe Renten:
        
        ka_renten_dict.clear()
        von = str(jahr)+'0101'
        bis = str(jahr)+'1231'

        ka_dict.clear()
        ka_dict['jahr']=jahr
        ka_dict['name']='anfang'
        ka_dict['topf']='renten'
        ka_dict['wert']=ka_renten_anfang_nach_reallokation
        self.SchreibeInKapitalanlagenCSV(ka_dict)
        
        #***********************************************
        
        #Schreibe Aktien:
        ka_dict.clear()
        ka_dict['jahr']=jahr
        ka_dict['name']='anfang'
        ka_dict['topf']='aktien'
        ka_dict['wert']=ka_aktien_anfang_nach_reallokation
        self.SchreibeInKapitalanlagenCSV(ka_dict)
        #************************************************
        
        if umbuchung_aktien>0:
            self.KaufeAktien(jahr, umbuchung_aktien)
        else:
            self.VerkaufeAktien(jahr, umbuchung_aktien)

        if umbuchung_renten>0:
            self.oka_renten.KaufeRenten(jahr, umbuchung_renten)
        else:
            self.VerkaufeRenten(jahr, umbuchung_renten)
            
    def VerkaufeAktien(self, jahr, betrag):
        pass
    
    def KaufeAktien(self, jahr, betrag):
        aktien_dict={}
        
        von=str(jahr)+'01'+'01'
        bis=str(jahr)+'12'+'31'

        
        aktien_dict['jahr']=jahr        
        aktien_dict['von']=von        
        aktien_dict['bis']=bis        
        aktien_dict['status']='offen'        

        aktien_dict['name']='anlage_betrag'
        aktien_dict['wert']=betrag
        self.SchreibeInAktienCSV(aktien_dict)
        aktien_dict.clear()

        sa_dict={}
        sa_dict['jahr']=jahr
        sa_dict['name']='vola_aktien'
        vola_aktien=float(self.LeseSACSV(sa_dict))
        sa_dict.clear()        

        aktien_dict['jahr']=jahr        
        aktien_dict['von']=von        
        aktien_dict['bis']=bis        
        aktien_dict['status']='offen'        

        aktien_dict['name']='vola_aktien'
        aktien_dict['wert']=vola_aktien
        self.SchreibeInAktienCSV(aktien_dict)
        aktien_dict.clear()

    def VerkaufeRenten(self, jahr, betrag):
        pass

            
    def SchreibeInKapitalanlagenCSV(self, key_dict):
        datei=self.file_kapitalanlagen
        
        jahr=key_dict.get('jahr')
        topf=key_dict.get('topf')
        name=key_dict.get('name')
        wert=key_dict.get('wert')
        
        if self.LeseKapitalanlageCSV(key_dict) != 0:
            self.ZeileLoeschenInKapitalanlageCSV(key_dict)
        
        text=str(jahr)+';'+str(topf)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       

    def LeseKapitalanlageCSV(self, key_dict):
        datei=self.file_kapitalanlagen
        df=pd.read_csv(datei, sep=";")
        df[['jahr', 'topf', 'name', 'wert']] = df[['jahr', 'topf', 'name', 'wert']].astype(str)
       
        jahr=key_dict.get('jahr')
        topf=key_dict.get('topf')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == str(jahr)) & (df.topf==str(topf)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='kapitalanlagen/LeseKapitalanlagenCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return float(wert)   

    def ZeileLoeschenInKapitalanlageCSV(self, key_dict):
        datei=self.file_kapitalanlagen
        
        jahr=key_dict.get('jahr')
        topf=key_dict.get('topf')
        name=key_dict.get('name')
        
        if self.LeseKapitalanlageCSV(key_dict) != 0:
            df = pd.read_csv(datei, sep=';')
            df1=df[(df['jahr'] != jahr) & (df['topf']!=topf) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='Kapitalanlage: Eintrag in der Bilanztabelle geloescht: jahr='+str(jahr)+' topf='+str(topf)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)
    
    
    def LeseBilanzCSV(self, key_dict):
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";")
        df[['jahr', 'rl', 'avbg', 'name', 'wert']] = df[['jahr', 'rl', 'avbg', 'name', 'wert']].astype(str)
       
        jahr=key_dict.get('jahr')
        rl=key_dict.get('rl')
        avbg=key_dict.get('avbg')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == str(jahr)) & (df.rl==str(rl)) & (df.avbg==str(avbg)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='kapitalanlagen/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return float(wert)   
    


