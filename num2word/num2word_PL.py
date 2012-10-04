# -*- coding: utf-8 -*- 
'''
Module: num2word_PL.py
Requires: num2word_PL.py
Version: 0.1

Author:
   Sebastian Żurek (sebzur@gmail.com)
   Maciej Sznajder (maciejsznajder@gmail.com)
   
Copyright:
    Copyright (c) 2007, Sebastian Żurek.  All Rights Reserved.
    Copyright (c) 2008, Maciej Sznajder.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

Data from:
    http://www.uni-bonn.de/~manfear/large.php
    
Usage:
    from num2word_PL import n2w, to_card, to_ord, to_ordnum
    to_card(1234567890)
    n2w.is_title = True
    to_card(1234567890)
    to_ord(1234567890)
    to_ordnum(1234567890)
    to_year(1976)
    to_currency(dollars*100 + cents, longval=False)
    to_currency((dollars, cents))
    

History:

    1.3.2 : new method full_numbers(), it solved problem with ord big numbers
    
    1.3.1 : new to_ordinal() method, it turns right words but ther are some problems
    with exceptions like f.e.: 1e3 or 1e6;
    Fixed problem with word "tysiąc" in some numbers -> merge method;
    
    1.2   : to_ordinal_num() made shorter and simpler (but slower)
    strings in merge() now interpolated
    to_year() and to_currency() added
         
    1.1   : to_ordinal_num() fixed for 11,12,13   
'''
from __future__ import division 
import num2word_EU

    
class Num2Word_PL(num2word_EU.Num2Word_EU):

    def set_high_numwords(self, high):
        max = 3 + 3*len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10**n] = word + u"ilion"

    def setup(self):
        self.negword = u"minus "
        self.pointword = u"kropka"
        self.errmsg_nonnum = u"Only numbers may be converted to words."
        self.exclude_title = [u"and", u"point", u"minus"]

        self.mid_numwords = [(1000, u"tysiąc"), (100, u"sto"), 
                             (90, u"dziewięćdziesiąt"), (80, u"osiemdziesiąt"), (70, u"siedemdziesiąt"),
                             (60, u"sześćdziesiąt"), (50, u"pięćdziesiąt"), (40, u"czterdzieści"),
                             (30, u"trzydzieści")]

        self.low_numwords = [u"dwadzieścia", u"dziewiętnaście", u"osiemnaście", u"siedemnaście",
                             u"szesnaście", u"piętnaście", u"czternaście", u"trzynaście",
                             u"dwanaście", u"jedenaście", u"dziesięć", u"dziewięć", u"osiem",
                             u"siedem", u"sześć", u"pięć", u"cztery", u"trzy", u"dwa",
                             u"jeden", u"zero"]
        
        self.ords = { u"jeden"      : u"pierwszy",
                      u"dwa"        : u"drugi",
                      u"trzy"       : u"trzeci",
                      u"cztery"     : u"czwarty",
                      u"pięć"       : u"piąty",
                      u"sześć"      : u"szósty",
                      u"siedem"     : u"siódmy",
                      u"osiem"      : u"ósmy",
                      u"dziewięć"   : u"dziewiąty",
                      u"dziesięć"   : u"dziesiąty",
                      u"dwanaście"  : u"dwunasty",
                      u"dwadzieścia": u"dwudziesty",
                      u"sto"        : u"setny",
                      u"dwieście"   : u"dwusetny",
                      u"trzysta"    : u"trzysetny",
                      u"czterysta"  : u"czterechsetny" }
        
        
        self.ords_next_lo_last = {u"dwadzieścia" : u"dwudziesty"}

        self.full_exceptions = {u"jeden"  : u"tysięczny",
                                u"dwa"    : u"dwutysięczny",
                                u"trzy"   : u"trzytysięczny",
                                u"cztery" : u"czterotysięczny",
                                u"siedem" : u"siedmiotysięczny",
                                u"osiem"  : u"ośmiotysieczny"}
        
        
    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next
        
        if cnum == 1 and nnum < 100:
            return next
        elif 100 > cnum > nnum :
            return ("%s %s"%(ctext, ntext), cnum + nnum)
        elif cnum >= 100 > nnum:
            return ("%s  %s"%(ctext, ntext), cnum + nnum)            
        elif nnum > cnum:            
            if nnum<1000:
                if cnum<2 :
                    return ("%s"%(ntext), cnum * nnum)            
                elif cnum<3:
                    return ("%s"%(u'dwieście'), cnum * nnum)            
                elif cnum<5:
                    return ("%s%s"%(ctext,'sta'), cnum * nnum)            
                elif cnum<10:
                    return ("%s%s"%(ctext,'set'), cnum * nnum)                                 

        if cnum+nnum>1000:
            #print unicode(ctext,'utf-8').encode('iso-8859-2'), cnum, unicode(ntext,'utf-8').encode('iso-8859-2'), nnum
            if cnum*nnum<2000 :
                return ("%s %s"%(ctext, ntext), cnum * nnum)
            elif cnum*nnum<5000 :
                return ("%s %s"%(ctext, ntext+'e'), cnum * nnum)
            
        if curr[1]<1000 and cnum*nnum>=5000 :
            i,j=0,0
            ctext_new,ntext_new='','' 
            for word in ctext.split():
                i+=1
                if word==u'tysiąc':
                    ctext_new+=u' tysięcy'
                elif word!=u'tysiąc':
                    ctext_new+=' '+ctext.split()[i-1]

            for word in ntext.split():
                j+=1
                if word==u'tysiąc':
                    ntext_new+=u' tysięcy'
                elif word!=u'tysiąc':
                    ntext_new+=' '+ntext.split()[j-1]

            ctext,ntext=ctext_new,ntext_new
                        
        return ("%s %s"%(ctext, ntext), cnum * nnum)

#-------------------------------------------------
    def to_ordinal(self, value):
        outwords = self.to_cardinal(value).split()
 
        self.last_number(outwords)
        self.next_to_last_number(outwords)
        
        # "if" condition solve problem with small numbers. Method full_numbers dosn't do anything with values<1000 so it broke ord word in method n2w.test()

        if value>=1000:
            self.full_numbers(outwords,value)        
        
        return " ".join(outwords)

    def last_number(self,outwords):
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
            
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == "e" or "a" and lastword[-2] == "i":
                lastword=lastword[:-5]+u"sty"
            if lastword[-1] == u"i" and lastword[-2] == u"c":
                 lastword=lastword[:-4]+u"sty"
            if lastword[-1] == u"t" and lastword[-2] == u"e":
                lastword+=u"ny"
            if lastword[-1] == u"y" and lastword[-2] == u"c":
                lastword=lastword[:-1]+u"zny"
            if lastword[-1] == u"n" and lastword[-2] == u"o":
                lastword+=u"owy"
            if lastword[-1] == u"t":
                lastword+=u"y"
            if lastword[-1] == u"e":
                lastword=lastword[:-3]+u"ty"
        
        lastwords[-1] = self.title(lastword)
        outwords[-1] = u"-".join(lastwords)
        
    def next_to_last_number(self,outwords):
        if len(outwords)>1:
            losts=outwords[-2].split(u"-")
            lost=losts[-1].lower()
         
            try:
                lost = self.ords_next_lo_last[lost]
            except KeyError:
                if lost[-1] == u"t":
                    lost+=u"y"
                if lost[-1] == u"i" and lost[-2] == u"c":
                    lost = lost[:-4]+u"sty"
                if lost[-1] == u"a" and lost[-2] == u"i":
                    lost=lost[:-3]+u"sty"
                if lost[-1] == u"o":
                    lost=lost
        
            losts[-1] = self.title(lost)
            outwords[-2] = u"-".join(losts)

    def full_numbers(self,outwords,value):

        #values > 1000
        
        fulls=outwords[-2].split(u"-")
        full=fulls[-1].lower()

        lasts=outwords[-1].split(u"-")
        last=lasts[-1].lower()

        firsts=outwords[0].split(u"-")
        first=firsts[0].lower()

        try:
            full = self.full_exceptions[full]
            outwords[-1] = u""
        except KeyError:
            if first == u"jeden":
                outwords[0] = u""
            if full == u"szósta" and last == u"szósty":
                outwords[-2] = last
                outwords[-1] = u""
            if full[-1] == u"ć": #\x87 -> ć
                full = full[:-2]+u"cio"
            if full[-1] == u"o" or u"e" and value/1000<19:
                full = full + u" " + last
                outwords[-1]=u""
            if full[-2] == u"t" and full[-3] == u"s" and last[-1] == u"y" and value>10000:
                full = full[:-1] + u"a " + last
                outwords[-1]=u""
            if full[-3] == u"\x85" and value>10000:
                full = full[:-4] + u"ęcio " + last
                outwords[-1]=u""
                      
        fulls[-1] = self.title(full)
        outwords[-2] = u"-".join(fulls)
#------------------------------------------------

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return u"%s%s"%(value, self.to_ordinal(value)[-2:])


    def to_year(self, val, longval=True):
        if not (val//100)%10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt=u"hundred", jointxt=u"and",
                                longval=longval)

    def to_currency(self, val, longval=True):
        return self.to_splitnum(val, hightxt=u"zł", lowtxt=u"gr",
                                jointxt=u"i", longval=longval)

class Test:
    def test(self,choice,min,max,step):
        
        n2w = Num2Word_PL()
        to_card = n2w.to_cardinal
        to_ord = n2w.to_ordinal
        to_ordnum = n2w.to_ordinal_num
        to_year = n2w.to_year
        
        result = ""
        for val in range(min,max,step):
            if choice == 0:
                result += n2w.test(val)
                result += "\n"
            if choice == 1:
                result += n2w.to_currency(val)
                result += "\n"
            if choice == 2:
                result += n2w.to_year(val)
                result += "\n"

        return result

if __name__=="__main__":
    print Test().test(0,1999,2002,1)
