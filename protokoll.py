#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os

class Protokoll:
    
    def __init__(self, f):
        self.file_protokoll = f
        datei= Path(self.file_protokoll)
        if datei.is_file():
            text="Datei " + self.file_protokoll+ " existiert."
            print(text)
            self.SchreibeInProtokoll(text)
            os.remove(self.file_protokoll)
            text='Datei ' + self.file_protokoll+ ' wird gelöscht.'
        else:
            print("Datei " + self.file_protokoll + " existiert nicht!!!")   
            return
        
    def SchreibeInProtokoll(self, text):
        text=text + "\n"
        f=open(self.file_protokoll, "a")
        f.write(text)    
        f.close()     
