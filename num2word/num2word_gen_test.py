# -*- coding: utf-8 -*-
#/usr/bin/env python

'''
Module: num2word_gen_test.py
Requires: num2word_PL.py
Version: 0.1

Authors:
   Sebastian Żurek (sebzur@gmail.com)
   Maciej Sznajder (maciejsznajder@gmail.com)
   
Copyright:
    Copyright (c) 2008, Sebastian Żurek.  All Rights Reserved.
    Copyright (c) 2008, Maciej Sznajder.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

History:

    1.0 : UI app for generating num2word tests   
'''

import wx
import num2word_PL as n2wPL

labels="EXE".split()
flags={"EXE":wx.ALIGN_TOP}


class ChildPanel(wx.Panel):

    def __init__(self,parent=None,id=-1,title="New test"):

        wx.Panel.__init__(self,parent,id) 
        self.SetBackgroundColour("grey")
        self.panelControls = {'checkboxes':{},  # stores checkboxes references
                              'ranges':{}}      # stores ranges ctrls
        
        sizer=wx.FlexGridSizer(rows=4,cols=3,hgap=5,vgap=5)

        self.GenerateCheckBox(sizer)
        self.GenerateTestRange(sizer)
        self.GenerateTextCtrl(sizer)
        
        self.GenerateStaticText(sizer)
        
        for label in labels:
            self.button=wx.Button(parent=self,id=-1,label=label)
            sizer.Add(self.button,0,flags.get(label,0),100)
            self.Bind(wx.EVT_BUTTON,self.Execute,self.button)

        self.GrowableCols(sizer)
        self.GrowableRows(sizer)

        self.SetSizer(sizer)
        self.Fit()

    # methods for StaticText
    def StaticTextData(self):
        
        return (("Dafault values:\nfrom 1 to 10 with step 1"),(""))    

    def GenerateStaticText(self,sizer):

        for label in self.StaticTextData():
            sizer.Add(wx.StaticText(self,id=-1,label=label))

    #methods for sizer Growable Cols & Rows
    def GrowableColsData(self):
        return ((0,1),(1,1),(2,1))

    def GrowableCols(self,sizer):

        for cR in self.GrowableColsData():
            sizer.AddGrowableCol(cR[0],cR[1])
    
    def GrowableRowsData(self):
        return ((0,1),(1,1),(2,2))

    def GrowableRows(self,sizer):

        for cR in self.GrowableRowsData():
            sizer.AddGrowableRow(cR[0],cR[1])
    
    #methodn for CheckBox
    def CheckBoxData(self):

        return (("n2w_MainTest"),
                ("n2w_currency"),
                ("n2w_date"))

    def GenerateCheckBox(self,sizer):

        for eachItem in self.CheckBoxData():
            self.panelControls['checkboxes'][eachItem] = wx.CheckBox(parent=self,id=-1,label=eachItem)
            sizer.Add(self.panelControls['checkboxes'][eachItem])

    #-----------------------
    def TestRangeData(self):

        return (("Min :"),
                ("Max :"),
                ("Step :"))
                

    def GenerateTestRange(self,sizer):
        
        for eachItem in self.TestRangeData():
            label=eachItem
                        
            Stext=wx.StaticText(self,id=-1,label=label)
            sizer.Add(Stext)

    def TextCtrlPos(self):
        
        return (("min"),
                ("max"),
                ("step"))
    
    def GenerateTextCtrl(self,sizer):

        for eachItem in self.TextCtrlPos():
            self.panelControls['ranges'][eachItem] = wx.TextCtrl(parent=self,id=-1)
            sizer.Add(self.panelControls['ranges'][eachItem])

    def Execute(self,event):

        t=n2wPL.Test()
        
        tM=[()]*6
        i=0
        for k,v in self.panelControls['ranges'].iteritems() :
            
            if v.GetValue() == '': #default values
                if k == 'min':
                    v=1
                    min=v
                elif k == 'max':
                    v=10
                    max=v
                elif k == 'step':
                    v=1
                    step=v
            elif v.GetValue != '': #not default values
                var=int(v.GetValue())
                if k == 'min' and var != '' :
                    v=var
                    min=var
                elif k == 'max' and var != '' :
                    v=var
                    max=var
                elif k == 'step' and var != '' :
                    v=var
                    step=var
            
            tM[i]=(k,v)
            i+=1

        for k,v in self.panelControls['checkboxes'].iteritems():
            v=int(v.GetValue())
            tM[i]=(k,v)
            i+=1

        for item in tM:

            if item[0] == 'n2w_date':
                Date = item[1]
            elif item[0] == 'n2w_currency':
                Currency = item[1]
            elif item[0] == 'n2w_MainTest':
                MainTest = item[1]
        
        t.test(MainTest,Currency,Date,min,max,step)


class ParentFrame(wx.Frame):

    def __init__(self,parent=None,id=-1,title="WxApp for genereting n2w tests",size=(1024,768)):
        
        wx.Frame.__init__(self,parent,id,title,size)
        
        mbar=self.MakeMenuBar()
        self.SetMenuBar(mbar)
        self.CreateStatusBar()
        panel=ChildPanel(self)
    
    def MakeMenuBar(self):

        menuBar=wx.MenuBar()
        menu=wx.Menu()
        exit=menu.Append(-1,"Exit")
        menuBar.Append(menu,"File")
        self.Bind(wx.EVT_MENU,self.CloseUI,exit)
        
        return menuBar

    def CloseUI(self,event):

        self.Close()

if __name__ == "__main__":
    app=wx.PySimpleApp()
    ParentFrame().Show()
    app.MainLoop()

