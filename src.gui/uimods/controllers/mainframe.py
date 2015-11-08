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
from uimods.aboutdialog import AboutDialog
from utils.mvc import DynBind
import wx

if True:
    @DynBind.EVT_BUTTON.Button.ClickMe
    def OnButtonClickClickMe(self, event):
        event.Skip()
        self.samestatus.value = not self.samestatus.value
        self.view.ClickedMe()

if True:
    @DynBind.EVT_BUTTON.Button.GetMOTD
    def OnButtonClickGetMOTD(self, event):
        event.Skip()
        self.model.GetNextMOTD()

if True:
    @DynBind.EVT_BUTTON.Button.ReloadModules
    def OnButtonClickReloadModules(self, event):
        event.Skip()
        self.__class__._reload_modules()


if True:
    @DynBind.EVT_CHECKBOX.CheckBox.SameStatus
    def OnCheckBoxSameStatus(self, event):
        event.Skip()
        # self.samestatus = self.m_checkBoxSameStatus.GetValue()

if True:
    @DynBind.EVT_BUTTON.Button.AddElement
    def OnButtonClickAddElement(self, event):
        event.Skip()
        dlg = wx.TextEntryDialog(parent=self,
                                 message='Enter text',
                                 caption='New Entry',
                                 defaultValue='')
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            print 'ok pressed'
            self.test.items.append(dlg.GetValue())

if True:
    @DynBind.EVT_BUTTON.Button.ClearSomeText
    def OnButtonClickClearSomeText(self, event):
        event.Skip()
        self.sometext = ''

if True:
    @DynBind.EVT_BUTTON.Button.AboutDialog
    @DynBind.EVT_TOOL.Tool.AboutDialog
    @DynBind.EVT_MENU.MenuItem.AboutDialog
    def OnEventAboutDialog(self, event):
        event.Skip()
        dialog = AboutDialog(self)
        dialog.ShowModal()

