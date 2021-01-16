# -*- coding: utf-8 -*-

import sys
import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.uic as uic


import optionen as opt
import protokoll as prot
import bilanz as bil
import vertrieb as ver
#import oe_antrag as oe_antrag
import antrag as antrag
import system
import kapitalanlagen as kap

import hilfe_steuerung as hs
import aufsichtsrat as ar
import system_dialog_vertrag as sdv
import einstellungen

os_system = 'Linux' #bzw. Windows

files_dict = {} #hier werden alle verzeichnisse und Dateien abgelegt. Dieses Oblekt wird in jedes Klasse bei Initialisierung übergeben
if os_system == 'Linux':
    files_dict['os_system'] = os_system
    files_dict['sep_dir'] = '/'
elif system == 'Windows':
    files_dict['os_system'] = os_system
    files_dict['sep_dir'] = '/'
else:
    print('kein System festgelegt es wird Linux unterstellt!')
    files_dict['os_system'] = 'Linux'
    files_dict['sep_dir'] = '/'

#in diesem dictionary werden Infos zu Kapitalallokation abgelegt:
ka_sa_dict={}
ka_renten_sa_dict={}

#in diesem dictionary werden Infos zum Neugeschäft abgelegt:
vertrieb_dict = {}

#Startjahr der Simulation:
jahr_beginn=2020

jahr_dict={} #für das laufende Jahr der Projektion wird dieses Dictionary angelegt
jahr_dict['jahr']=jahr_beginn

#in diesem dictionary werden Infos zu Kapitalallokation abgelegt:
ka_sa_dict={}
ka_renten_sa_dict={}

#in diesem dictionary werden Infos zum Neugeschäft abgelegt:
vertrieb_dict = {}

#Startjahr der Simulation:
jahr_beginn=2020

jahr_dict={}
jahr_dict['jahr']=jahr_beginn

files_dict['Startjahr_Simulation']=jahr_beginn
    
def SetztSimmungIconAufsichtsrat():
    file = oar.GibStimmungFile() #file mit dem Icon
    icon = gui.QIcon(file)  
    wSpielwindow.pushButton_aufsichtsrat.setIcon(icon)
    hoehe=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_aufsichtsrat).get('hoehe')-10
    breite=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_aufsichtsrat).get('breite')-10
    wSpielwindow.pushButton_aufsichtsrat.setIconSize(core.QSize(breite,hoehe))

def WasMeintAufsichtsrat():
    jahr=int(jahr_dict.get('jahr'))
    oar.AussageAR(jahr)

def Vertragsverwaltung():
    osdv = sdv.SystemDialogVertrag(files_dict)
    osdv.ZeigeAlleVertraege()

def LeseGroesseEinesButtonsAus(btn):
    dim_dict={}
    w=btn.width()
    h=btn.height()
    dim_dict['hoehe']=h
    dim_dict['breite']=w
    return dim_dict

def LegeDefoultEinstellungenfest():
    index = wSpielwindow.comboBox_L1.findText("5")
    wSpielwindow.comboBox_L1.setCurrentIndex(index)    

    index = wSpielwindow.comboBox_L2.findText("10")
    wSpielwindow.comboBox_L2.setCurrentIndex(index)
    
    index = wSpielwindow.comboBox_L3.findText("20")
    wSpielwindow.comboBox_L3.setCurrentIndex(index)    

    index = wSpielwindow.comboBox_A1.findText("50")
    wSpielwindow.comboBox_A1.setCurrentIndex(index)    
    index = wSpielwindow.comboBox_A2.findText("30")
    wSpielwindow.comboBox_A2.setCurrentIndex(index)    
    index = wSpielwindow.comboBox_A3.findText("20")
    wSpielwindow.comboBox_A3.setCurrentIndex(index)    
    
    wSpielwindow.horizontalSlider_Renten.setValue(70)
    AnteilImSliderRenten()

def LegeLaufzeitAuswahlBeiProduktenFest():
    for i in range(1, 30):
        wSpielwindow.comboBox_Laufzeit_Renten.insertItem(i, str(i))
        wSpielwindow.comboBox_Laufzeit_BU.insertItem(i, str(i))

def LegeGuVTabelleAn(obil):
    #Im Dialog werden die Ergebnisse der GuV ausgegeben:
    jahr_beginn = files_dict.get('Startjahr_Simulation')
    jahr_aktuell = files_dict.get('jahr_aktuell')

    #Hilfefunktionen:
    ohs=hs.HilfeSteuerung()
        
    #Anzahl der darzustellenden Jahre:    
    anzahl_jahre = int(jahr_aktuell)-int(jahr_beginn)

    #Die Jahre werden im Dialog dargestellt:    
    wSpielwindow.tableWidget_guv.setColumnCount(anzahl_jahre+1)
    wSpielwindow.tableWidget_guv.setRowCount(1)
    
    vektor_jahre=[]
    for i in range(0, anzahl_jahre+1):
        jahr=str(jahr_beginn+i-1)
        vektor_jahre.append(jahr)
        
    wSpielwindow.tableWidget_guv.setHorizontalHeaderLabels(vektor_jahre)

    vektor_namen=[]
    index_row = 0   
    namen={}
    
    key_bilanz={}
    key_bilanz['rl']='guv'
    key_bilanz['avbg']='999'
    
    namen ['bil_gebuchter_beitrag']='gebuchter Beitrag'
    namen ['bil_derue7_veraenderung']='Veränderung der Deckungsrückstellung'
    namen ['jahresueberschuss']='Jahresüberschuss'
    
    for name in namen:
        key_bilanz['name']=name
        index_row += 1
        wSpielwindow.tableWidget_guv.setRowCount(index_row)
        vektor_namen.append(namen.get(name))
        for i in range(0, anzahl_jahre+1):
            jahr=str(jahr_beginn+i)
            key_bilanz['jahr']=jahr
            wert=obil.LeseBilanzCSV(key_bilanz)
            wert=ohs.formatter(wert)
            wSpielwindow.tableWidget_guv.setItem(index_row-1,i+1,widgets.QTableWidgetItem(str(wert)))
        
    #Zeilenüberschriften:
    wSpielwindow.tableWidget_guv.setVerticalHeaderLabels(vektor_namen)

def LegeBilanzTabelleAn(obil):
    #hier werden die Ergebnisse der Bilanz in eine Tabelle im Dialog ausgegeben:
    jahr_beginn = files_dict.get('Startjahr_Simulation')
    jahr_aktuell = files_dict.get('jahr_aktuell')

    #Hilfefunktionen:
    ohs=hs.HilfeSteuerung()

    #Anzahl der darzustellenden Jahre:    
    anzahl_jahre = int(jahr_aktuell)-int(jahr_beginn)

    wSpielwindow.tableWidget_Bilanz.setColumnCount(anzahl_jahre+1)
    wSpielwindow.tableWidget_Bilanz.setRowCount(1)
    
    vektor_jahre=[]
    for i in range(0, anzahl_jahre+1):
        jahr=str(jahr_beginn+i-1)
        vektor_jahre.append(jahr)
        
    #Im Dialog werden die Jahre dargestellt:
    wSpielwindow.tableWidget_Bilanz.setHorizontalHeaderLabels(vektor_jahre)

    #Ab hier werden die Bilanzpositionen dargestellt:
    vektor_namen=[]
    index_row = 0   
    namen={}
    
    key_bilanz={}
    key_bilanz['rl']='bilanz'
    key_bilanz['avbg']='999'
    
    namen['eigenkapital_ende']='Eigenkapital'
    namen['bil_derue7_ende']='Deckungskapital a. Risiko VN'

    for name in namen:
        key_bilanz['name']=name
        index_row += 1

        wSpielwindow.tableWidget_Bilanz.setRowCount(index_row)
        vektor_namen.append(namen.get(name))
        for i in range(0, anzahl_jahre+1):
            jahr=str(jahr_beginn+i-1)
            key_bilanz['jahr']=jahr
            wert=obil.LeseBilanzCSV(key_bilanz)        
            wert=ohs.formatter(wert)

            wSpielwindow.tableWidget_Bilanz.setItem(index_row-1,i,widgets.QTableWidgetItem(str(wert)))
    
    wSpielwindow.tableWidget_Bilanz.setVerticalHeaderLabels(vektor_namen)


def LegeLaufzeitAuswahlBeiRentenFest():
    
    for i in range(1,21):
        wSpielwindow.comboBox_L1.insertItem(i, str(i))
        wSpielwindow.comboBox_L2.insertItem(i, str(i))
        wSpielwindow.comboBox_L3.insertItem(i, str(i))
    
    for i in range(25, 51, 5):
        wSpielwindow.comboBox_L1.insertItem(i, str(i))
        wSpielwindow.comboBox_L2.insertItem(i, str(i))
        wSpielwindow.comboBox_L3.insertItem(i, str(i))
        
    for i in range(0, 101, 10):
        wSpielwindow.comboBox_A1.insertItem(i, str(i))        
        wSpielwindow.comboBox_A2.insertItem(i, str(i))        
        wSpielwindow.comboBox_A3.insertItem(i, str(i))        

def LeseAusSpielfensterKA():
    #es werden aus dem Dialog die Eingaben zu Kapitalanlagen ausgelesen:
    
    #Jahr der Simulation:
    ka_sa_dict['jahr']=wSpielwindow.label_Jahr.text()

    #laufzeiten der Renten:
    l1 = int(wSpielwindow.comboBox_L1.currentText())
    l2 = int(wSpielwindow.comboBox_L2.currentText())
    l3 = int(wSpielwindow.comboBox_L3.currentText())

    ka_renten_sa_dict['laufzeit']=[l1, l2, l3]
    ka_renten_sa_dict['anzahl']=3

    #Anteile der Renten:
    a1 = float(wSpielwindow.comboBox_A1.currentText())/100
    a2 = float(wSpielwindow.comboBox_A2.currentText())/100
    a3 = float(wSpielwindow.comboBox_A3.currentText())/100
    
    ka_renten_sa_dict['aufteilung']=[a1, a2, a3]
    
    #Aufteilung auf Renten und Aktien:
    anteil_renten = float(wSpielwindow.label_Anteil_Renten.text())/100
    anteil_aktien = float(wSpielwindow.label_Anteil_Aktien.text())/100
    
    ka_sa_dict['anteil_renten']=anteil_renten
    ka_sa_dict['anteil_aktien']=anteil_aktien
    
    ka_sa_dict['vola_aktien']=0.1
    
    #das gesamtem Dict zu Renten wird in das Dict zu KA reingeschrieben:
    ka_sa_dict['renten']=ka_renten_sa_dict
    t = 'Aus dem Dialog zu Kapitalanlagen wurden für Renten ausgelesen:' +str(ka_renten_sa_dict)
    oprot.SchreibeInProtokoll(t)


def SchreibeMessage(text):
    msg = widgets.QMessageBox()
    msg.setIcon(widgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle('Info')
    
    msg.exec()

def ZeigeGrafik(file):
    w=uic.loadUi(files_dict.get('leereswindow_file'))
    pixmap = gui.QPixmap(file)  
    w.label_Grafik.setPixmap(pixmap)
    w.label_Grafik.setScaledContents(True) 
    w.exec_()           

def ZeigeGrafik_ZSK():
    file=files_dict.get('file_grafik_zsk')
    ZeigeGrafik(file)

def ZeigeGrafik_Entwicklung_Renten():
    file=files_dict.get('grafik_file_entwicklung_renten')
    ZeigeGrafik(file)

def ZeigeGrafik_Statistik_Anzahl():
    file=files_dict.get('grafik_file_statistik_anzahl')
    ZeigeGrafik(file)

def ZeigeGrafik_Statistik_JSB():
    file=files_dict.get('grafik_file_statistik_jsb')
    ZeigeGrafik(file)

def LeseAusFensterMainAlleEingaben():
    
    #das Risiko in der kapitalanlage kann man nur einmalig fuer alle Laeufe definiert werden:
    if wMainwindow.radioButton_KA_Risiko_normal.isChecked():
        ka_renten_sa_dict['risiko']='normal' 
    elif wMainwindow.radioButton_KA_Risiko_riskant.isChecked():
        ka_renten_sa_dict['risiko']='risky' 
    elif wMainwindow.radioButton_KA_Risiko_sehr_riskant.isChecked():
        ka_renten_sa_dict['risiko']='high_risky' 
    else:
        ka_renten_sa_dict['risiko']='nermal' 
        oprot.SchreibeInProtokoll('Das Risiko in der Kapitalanlage in den Renten konnte nicht zugerdnet werden. Es wurde daher festgelegt: ' + str(ka_renten_sa_dict.get('risiko')))
        
    oprot.SchreibeInProtokoll('Das Risiko in der Kapitalanlage in den Renten wurde festgelegt: ' + str(ka_renten_sa_dict.get('risiko')))
 

def LeseAusFensterSpielVertriebEingaben():
    #hier werden die Eingaben zum Thema Neugeschäft aus dem Dialog Spiel ausgelesen:
    
    #Jahr der Simulation:
    vertrieb_dict['jahr']=wSpielwindow.label_Jahr.text()

    #Anzahl Neugeschäft:
    try:
        a_renten = int(wSpielwindow.lineEdit_Anzahl_Renten.text())
    except:
        a_renten = 0
        text = 'Eingaben Vertrieb: Anzahl Renten-Antraege wird auf null gesetzt!'
        SchreibeMessage(text)
        wSpielwindow.lineEdit_Anzahl_Renten.setText(str(a_renten))
    
    vertrieb_dict['anzahl_renten']=a_renten
    
    try:
        a_bu = int(wSpielwindow.lineEdit_Anzahl_BU.text())
    except:
        a_bu = 0
        text = 'Eingaben Vertrieb: Anzahl BU-Antraege wird auf null gesetzt!'
        SchreibeMessage(text)
        wSpielwindow.lineEdit_Anzahl_BU.setText(str(a_bu))
        
    vertrieb_dict['anzahl_bu']=a_bu

    #Laufzeiten:
    l_renten = wSpielwindow.comboBox_Laufzeit_Renten.currentText()
    vertrieb_dict['laufzeit_renten']=int(l_renten)

    l_bu = wSpielwindow.comboBox_Laufzeit_BU.currentText()
    vertrieb_dict['laufzeit_bu']=int(l_bu)
    
    text = 'Aus dem Dialog zum Vertrieb wurden für folgende Eingaben ausgelesen:' +str(vertrieb_dict)
    oprot.SchreibeInProtokoll(text)

def LeseAusFensterSpielAlleEingaben():
    #Das Dialog Spielfenster wird ausgelesen:

    ka_renten_sa_dict['jahr']=wSpielwindow.label_Jahr.text()
 
    #lese Eingaben zu Kapitalanlagen:
    LeseAusSpielfensterKA()
    
    #lese Eingaben zum Neugeschäft:
    LeseAusFensterSpielVertriebEingaben()

def AnteilImSliderRenten():
    wert_renten = wSpielwindow.horizontalSlider_Renten.value()
    wert_aktien = 100 - int(wert_renten)
    wSpielwindow.horizontalSlider_Aktien.setValue(wert_aktien)
    wSpielwindow.label_Anteil_Renten.setText(str(wert_renten))
    wSpielwindow.label_Anteil_Aktien.setText(str(wert_aktien))
    
def KontrolleAnteilRenten():
    anteil1=wSpielwindow.comboBox_A1.currentText()
    anteil2=wSpielwindow.comboBox_A2.currentText()
    anteil3=wSpielwindow.comboBox_A3.currentText()
    
    summe=int(anteil1)+int(anteil2)+int(anteil3)
    
    if summe == 100:
        ergebnis=True
    else:
        text = 'Fehler: Summe = '+str(summe)+'. Es sollten aber 100 sein!'
        SchreibeMessage(text)
        ergebnis=False
    
    return ergebnis
    
def Kontrollen():
    
    if KontrolleAnteilRenten() == False:
        text = 'KontrolleAnteilRenten: Fehler in der Aufteilung der Renten'
        oprot.SchreibeInProtokoll(text)
        return False
        
    return True
    
def Steuerung():
    
    overtrieb = ver.Vertrieb(files_dict)
    oprot.SchreibeInProtokoll('Vertrieb wurde angelegt')
    
    oantrag = antrag.Antrag(files_dict)
    oprot.SchreibeInProtokoll('Anträge wurden angelegt')
    
    file_vertrieb=overtrieb.file_vertrieb
    oantrag.LegeVerriebstabelleFest(file_vertrieb)
    
    #oantrag_oe = oe_antrag.OE_Antarg(files_dict)

    osys = system.System(files_dict)
    
    file_system_antrag=oantrag.file_system_antrag
    osys.LegeAntragstabelleFest(file_system_antrag)
    
    obil = bil.Bilanz(files_dict)
    oprot.SchreibeInProtokoll('Bilanz wurde angelegt')
    obil.Init_Bilanz(jahr_beginn)
    
    okap = kap.Kapitalanlagen(files_dict)
    oprot.SchreibeInProtokoll('Kapitalanlagen wurden angelegt')

    okap.Init_KA(jahr_beginn)
    
    jahr=int(jahr_beginn)
    jahr_dict['jahr']=jahr
    files_dict['jahr_aktuell']=jahr

    ka_sa_dict.clear()

    LeseAusFensterMainAlleEingaben()
    wSpielwindow.label_Jahr.setText(str(jahr))
    
    #die Tabelle im Dialog mit Ergebnissen der Bilanz wird angelegt: 
    LegeBilanzTabelleAn(obil)

    #die Tabelle im Dialog mit Ergebnissen der GuV wird angelegt: 
    LegeGuVTabelleAn(obil)
    
    #solange im Spielwindow okay geclickt wird, dann wird ein Jahr weiter gespielt: 
    while wSpielwindow.exec_() == widgets.QDialog.Accepted:
        
        files_dict['jahr_aktuell']=jahr
        jahr_dict['jahr']=jahr
        
        if Kontrollen() == False:
            continue
            
        #es werden alle Eingaben aus dem Dialog ausgelesen:
        LeseAusFensterSpielAlleEingaben()
        
        von=str(jahr)+'01'+'01'
        bis=str(jahr)+'12'+'31'

        LeseAusFensterSpielAlleEingaben()

        okap.Init_SA(ka_sa_dict)
        
        obil.ErstelleBilanzAnfang(jahr)

        oar.BestimmeJahresZiele(jahr) #Die Jahresziele werden abgelegt
        
        overtrieb.SchreibeNeugeschaeft(vertrieb_dict)        
        
        okap.Beginn(jahr)
        okap.Fortschreibung(jahr)

        osys.Fortschreibung(von, bis)
        
        oantrag.LeseVertrieb(jahr)
        
        osys.Policiere(jahr)
        osys.ErstelleStatistik(von, bis)
        
        obil.ErstelleBilanzEnde(jahr)
        
        okap.ZeichneKapitalanlagen(jahr)
        
        #Angaben für den Aufsitzsrat:
        oar.SetzteWoBinIch('jab') #der JAB ist fertig!
        oar.BestimmeZielerreichung(jahr)
        SetztSimmungIconAufsichtsrat() #Die Stimmung des AR kann abgeholt werden

        jahr += 1
        files_dict['jahr_aktuell']=jahr
        LegeBilanzTabelleAn(obil) #Ergebnisse der Bilanz
        LegeGuVTabelleAn(obil) #Ergebnisse der GuV
        
        wSpielwindow.label_Jahr.setText(str(jahr))
        
        file_grafik = files_dict.get('grafik_file_entwicklung_renten')
        icon = gui.QIcon(file_grafik)  
        wSpielwindow.pushButton_Entwicklung_Renten.setIcon(icon)
        hoehe=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_Entwicklung_Renten).get('hoehe')-10
        breite=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_Entwicklung_Renten).get('breite')-10
        wSpielwindow.pushButton_Entwicklung_Renten.setIconSize(core.QSize(breite,hoehe))

        file_grafik = files_dict.get('file_grafik_zsk')
        icon = gui.QIcon(file_grafik)  
        wSpielwindow.pushButton_ZSK.setIcon(icon)
        hoehe=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_ZSK).get('hoehe')-10
        breite=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_ZSK).get('breite')-10
        wSpielwindow.pushButton_ZSK.setIconSize(core.QSize(breite,hoehe))

        file_grafik = files_dict.get('grafik_file_statistik_anzahl')
        icon = gui.QIcon(file_grafik)  
        wSpielwindow.pushButton_statistik_anzahl.setIcon(icon)
        hoehe=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_statistik_anzahl).get('hoehe')-10
        breite=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_statistik_anzahl).get('breite')-10
        wSpielwindow.pushButton_statistik_anzahl.setIconSize(core.QSize(breite,hoehe))

        file_grafik = files_dict.get('grafik_file_statistik_jsb')
        icon = gui.QIcon(file_grafik)  
        wSpielwindow.pushButton_statistik_jsb.setIcon(icon)
        hoehe=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_statistik_jsb).get('hoehe')-10
        breite=LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_statistik_jsb).get('breite')-10
        wSpielwindow.pushButton_statistik_jsb.setIconSize(core.QSize(breite,hoehe))
        
    oprot.SchreibeInProtokoll("ENDE erreicht!!!")
    print("**** Ende ****")



app = widgets.QApplication(sys.argv)

oeintellung = einstellungen.Einstellungen(files_dict)
if oeintellung.LeseEinstellungen() == False: # hier werden die Verzeichnisse festgelegt
    exit()

wMainwindow=uic.loadUi(files_dict.get('mainwindow_file'))
wSpielwindow=uic.loadUi(files_dict.get('spielwindow_file'))

wMainwindow.pushButtonSpiele.clicked.connect(Steuerung)
wMainwindow.actionSpielen.triggered.connect(Steuerung)

wSpielwindow.pushButton_ZSK.clicked.connect(ZeigeGrafik_ZSK)
wSpielwindow.pushButton_statistik_anzahl.clicked.connect(ZeigeGrafik_Statistik_Anzahl)
wSpielwindow.pushButton_statistik_jsb.clicked.connect(ZeigeGrafik_Statistik_JSB)
wSpielwindow.pushButton_Entwicklung_Renten.clicked.connect(ZeigeGrafik_Entwicklung_Renten)
wSpielwindow.horizontalSlider_Renten.valueChanged.connect(AnteilImSliderRenten)
wSpielwindow.pushButton_Vertragsverwaltung.clicked.connect(Vertragsverwaltung)
wSpielwindow.pushButton_aufsichtsrat.clicked.connect(WasMeintAufsichtsrat)

LegeLaufzeitAuswahlBeiRentenFest()
LegeLaufzeitAuswahlBeiProduktenFest() #Starteinstellungen zu Produkten

LegeDefoultEinstellungenfest()

oopt = opt.Optionen(files_dict.get('optionen_file_main'))  
    
oprot = prot.Protokoll(files_dict.get('protokoll_file_main'))

oar = ar.Aufsichtsrat(files_dict)
oar.AussageAR(int(jahr_dict.get('jahr')))
oar.SetztStimmungIcon()

wMainwindow.show()
app.exec_()
    