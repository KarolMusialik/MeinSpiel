#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Hilfe_System(object):    
    def __init__(self):
        pass
    
    def DictAusDatum(self, datum_str):
        jahr=datum_str[0:4]
        monat=datum_str[4:6]   
        tag=datum_str[6:8]
        dic={}
        dic['jahr'] = jahr
        dic['monat'] = monat
        dic['tag'] = tag
        dic['jjjjmmtt'] = datum_str
        
        s=''
        if tag[0]=='0':
            s=tag[1]
        else:
            s=tag
        
        dic['tt_int']=int(s)

        s=''
        if monat[0]=='0':
            s=monat[1]
        else:
            s=monat
        
        dic['mm_int']=int(s)
        dic['jjjj_int']=int(jahr)
        
        return dic

class VerketteteListe(object):
    
    def __init__(self, vsnr, histnr, von, bis, nxt):
        self.vsnr=vsnr
        self.histnr=histnr
        self.von=von
        self.bis=bis
        self.nxt=nxt
