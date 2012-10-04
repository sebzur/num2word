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


class ChildPanel(wx.Panel):

    def __init__(self,parent=None,id=-1,title="New test"):

        wx.Panel.__init__(self,parent,id) 
        self.SetBackgroundColour("grey")
        self.panelControls = {'checkboxes':{},  # stores checkboxes references
                              'ranges':{}       # stores ranges ctrls
                              }

        self.GenerateCheckBox()
        self.GenerateTestRange()
        self.GenerateTextCtrl()
        
        self.button=wx.Button(parent=self,id=-1,label="EXE",pos=(250,125))
        self.Bind(wx.EVT_BUTTON,self.Execute,self.button)

        sizer=wx.BoxSizer()
        self.SetSizer(sizer)

    def CheckBoxData(self):

        return (("n2w_MainTest",(20,20)),
                ("n2w_currency",(20,50)),
                ("n2w_date",(20,80)))

    def GenerateCheckBox(self):

        for eachItem in self.CheckBoxData():
            self.panelControls['checkboxes'][eachItem[0]] = wx.CheckBox(parent=self,id=-1,label=eachItem[0],pos=eachItem[1])

    def TestRangeData(self):

        return (("Min :",(200,20)),
                ("Max :",(200,50)),
                ("Step :",(200,80)),
                ("Dafault values:\nfrom 1 to 10 with step 1",(20,110)))

    def GenerateTestRange(self):
        
        for eachItem in self.TestRangeData():
            label=eachItem[0]
            pos=eachItem[1]
            
            wx.StaticText(self,id=-1,label=label,pos=pos)
            
    def TextCtrlPos(self):
        
        return (('min',(250,16)),
                ('max',(250,46)),
                ('step',(250,76)),
                )
    
    def GenerateTextCtrl(self):

        for eachItem in self.TextCtrlPos():
            self.panelControls['ranges'][eachItem[0]] = wx.TextCtrl(parent=self,id=-1,pos=eachItem[1])
            
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

    def __init__(self,parent=None,id=-1,title="WxApp for genereting n2w tests",size=(640,480)):
        
        wx.Frame.__init__(self,parent,id,title,size)
        self.count=0
        mbar=self.MakeMenuBar()
        self.SetMenuBar(mbar)
        self.CreateStatusBar()
        panel=ChildPanel(self)
    
    def MakeMenuBar(self):

        menuBar=wx.MenuBar()
        menu=wx.Menu()
        exit=menu.Append(-1,"Exit")
        menuBar.Append(menu,"File")
        self.Bind(wx.EVT_MENU,self.CloseAUI,exit)
        
        return menuBar

    def CloseAUI(self,event):

        self.Close()

if __name__ == "__main__":
    app=wx.PySimpleApp()
    ParentFrame().Show()
    app.MainLoop()

