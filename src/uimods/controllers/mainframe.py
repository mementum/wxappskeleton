#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
################################################################################
# 
#  Copyright (C) 2014 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from utils.mvc import DynBind
import wx

if True:
    @DynBind.EVT_BUTTON.Button.ClearSomeText
    def OnButtonClearSomeText(self, event):
        event.Skip()
        self.view.m_textCtrlSomeText.Clear()

if True:
    def OnButtonClickClickMe(self, event):
        event.Skip()
        self.samestatus.value = not self.samestatus.value
        self.view.ClickedMe()

if True:
    def OnButtonClickGetMOTD(self, event):
        event.Skip()
        self.model.GetNextMOTD()

if True:
    def OnButtonClickReloadModules(self, event):
        event.Skip()
        self.__class__._reload_modules()


if True:
    def OnCheckBoxSameStatus(self, event):
        event.Skip()
        # self.samestatus = self.m_checkBoxSameStatus.GetValue()

if True:
    def OnButtonClickAddElement(self, event):
        event.Skip()
        dlg = wx.TextEntryDialog(parent=self, message='Enter text', caption='New Entry', defaultValue='')
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            print 'ok pressed'
            self.test.items.append(dlg.GetValue())

if True:
    def OnButtonClickSomeText(self, event):
        event.Skip()
        self.sometext = ''
