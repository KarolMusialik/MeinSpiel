# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
import os
import optionen as opt

class Einstellungen(QtWidgets.QDialog):
    def __init__(self, f_dict, parent=None):
        super(Einstellungen, self).__init__(parent)
        
        self.files_dict = f_dict

        verzeichnis_aktuell = os.getcwd()
        sep_dir = f_dict.get('sep_dir')
        verzeichnis = verzeichnis_aktuell + sep_dir

        self.files_dict['optionen_file_einstellungen'] = verzeichnis + 'optionen_einstellungen.csv'
        file_opt = self.files_dict.get('optionen_file_einstellungen')
        self.oopt = opt.Optionen(file_opt)

        key = 'work_dir'
        wert = self.oopt.LeseInhaltOptionen(key)
        if wert == '':
            print('Einstellungen/__init__: keine Datei für Optionen gefunden. Es wird eine Standartdatei eingestellt.')
            self.work_dir = '/home/karol/Meine_projekte/MeinSpiel/Datei'
        else:
            self.work_dir = wert

        key = 'username'
        wert = self.oopt.LeseInhaltOptionen(key)
        if wert == '':
            print('Einstellungen/__init__: kein Username in Optionen gefunden. Es wird ein Standartuser eingestellt.')
            self.username = 'karol'
        else:
            self.username = wert

        file_ui = verzeichnis+'einstellungen.ui'
        self.ui = uic.loadUi(file_ui, self)

    def EinstellungenFestlegen(self):
        # work directory:
        self.files_dict['work_dir'] = self.work_dir
        self.files_dict['username'] = self.username

        sep_dir = self.files_dict.get('sep_dir')
        verzeichnis = self.work_dir + sep_dir

        #einzelne Dateien:
        self.files_dict['mainwindow_file'] = verzeichnis+'mainwindow.ui'
        self.files_dict['spielwindow_file'] = verzeichnis+'spielwindow.ui'
        self.files_dict['leereswindow_file'] = verzeichnis+'leereswindow.ui'
        
        self.files_dict['file_grafik_zsk'] = verzeichnis+'grafik_zsk.png'
        self.files_dict['grafik_file_entwicklung_renten'] = verzeichnis+'grafik_renten.png'
        
        self.files_dict['optionen_file_main'] = verzeichnis+'optionen_main.csv'
        self.files_dict['protokoll_file_main'] = verzeichnis+'protokoll_main.txt'
        
        self.files_dict['optionen_file_vertrieb'] = verzeichnis+'optionen_vertrieb.csv'
        self.files_dict['protokoll_file_vertrieb'] = verzeichnis+'protokoll_vertrieb.txt'
        self.files_dict['file_vertrieb'] = verzeichnis+'vertrieb.csv'
        
        self.files_dict['optionen_file_antrag'] = verzeichnis+'optionen_antrag.csv'
        self.files_dict['protokoll_file_antrag'] = verzeichnis+'protokoll_antrag.txt'
        self.files_dict['file_system_antrag'] = verzeichnis+'system_antrag.csv'
        self.files_dict['optionen_file_antrag_oe'] = verzeichnis+'optionen_antrag_oe.csv'
        self.files_dict['protokoll_file_antrag_oe'] = verzeichnis+'protokoll_antrag_oe.txt'
        
        self.files_dict['protokoll_file_bilanz'] = verzeichnis+'protokoll_bilanz.txt'
        self.files_dict['file_bilanz'] = verzeichnis+'bilanz.csv'
        self.files_dict['file_bilanz_start'] = verzeichnis+'bilanz_start.csv'
        self.files_dict['file_bilanz_struktur'] = {'jahr':int, 'rgl':str, 'avbg': str, 'name':str, 'wert':str}
        
        self.files_dict['protokoll_file_system'] = verzeichnis+'protokoll_system.txt'
        self.files_dict['file_system_fortschreibung_struktur'] = {'vsnr':str, 'histnr':int ,'von':int, 'bis':int, 'name':str, 'wert':str}
        self.files_dict['file_system_bestand_struktur'] = {'vsnr':str, 'histnr':int ,'von':int, 'bis':int, 'name':str, 'wert':str}
        self.files_dict['file_system_fortschreibung'] = verzeichnis+'system_fortschreibung.csv'
        
        self.files_dict['grafik_file_statistik_anzahl'] = verzeichnis+'grafik_statistik_anzahl.png'
        self.files_dict['grafik_file_statistik_jsb'] = verzeichnis+'grafik_statistik_jsb.png'
        self.files_dict['file_system_statistik'] = verzeichnis+'system_statistik.csv'
        self.files_dict['file_system_statistik_beschreibung'] = verzeichnis+'system_statistik_beschreibung.txt'
    
    def LeseUsername(self):
        username = self.lineEditUser.text()
        if username == '':
            text = 'Du muss einen Namen festlegen!'
            self.SchreibeMessage(text)
            return False
        else:
            self.username = username
            key = 'username'
            text = username
            self.oopt.SchreibeInOptionen(key, text)
            return True

    def LeseWorkDir(self):
        work_dir = self.labelVerzeichnisImSpiel.text()
        if work_dir == '':
            text = 'Du muss ein Verzeichnis festlegen!'
            self.SchreibeMessage(text)
            return False
        else:
            self.work_dir = work_dir
            key = 'work_dir'
            text = work_dir
            self.oopt.SchreibeInOptionen(key, text)
            return True

    def PruefeVerzeichnis(self, verz):
        return True

    def VerzeichnisAuswaehlen(self):
        verz = QtWidgets.QFileDialog.getExistingDirectory(self, 'Wähle ein Verzeichnis aus')

        if self.PruefeVerzeichnis(verz) == True:
            self.work_dir = verz
            key = 'work_dir'
            text = verz
            self.oopt.SchreibeInOptionen(key, text)

            return True

        else:
            self.work_dir = ''
            text = 'Du muss ein Verzeichnis mit den Dateien aussuchen!'
            self.SchreibeMessage(text)
            return False

    def PruefeEingaben(self):
        pruefung = False
        if self.LeseUsername() == True:
            pruefung = True
        else:
            return False

        if self.LeseWorkDir() == True:
            pruefung = True
        else:
            return False

    def EinstellungDialog(self):

        self.pushButtonVerzeichnis.clicked.connect(self.VerzeichnisAuswaehlen)

        self.labelVerzeichnisImSpiel.setText(self.work_dir)
        self.lineEditUser.setText(self.username)
        
        if self.ui.exec_() == QtWidgets.QDialog.Accepted:
            self.work_dir = self.labelVerzeichnisImSpiel.text()
            self.username = self.lineEditUser.text()
            return True
        else:
            return False

    def LeseEinstellungen(self):
        if self.EinstellungDialog() == True:
            self.EinstellungenFestlegen()
            return True
        else:
            return False

    def SchreibeMessage(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle('Info')
        msg.exec()