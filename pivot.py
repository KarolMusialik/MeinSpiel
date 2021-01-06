#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

class Pivot(object):

    def __init__(self, f_dict):
        self.data = f_dict.get('file_data')
        self.beschreibung = f_dict.get('file_beschreibung')
    
    def ZeigePivotDialog(self):
        indexListe = self.GetIndex()
        valuesListe = self.GetValues()

        return pd.pivot_table(self.date, index=indexListe, values=valuesListe, aggfunc=sum)
        
    def GetIndex(self):
        liste=[]
        return liste

    def GetValues(self):
        liste=[]
        return liste
    
    
