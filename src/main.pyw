#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
################################################################################
# 
# Copyright (C) 2014 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
import wx

import appconstants
import uimods.mainframe as mainframe
import utils.flushfile

class MainApp(wx.App):
    def OnInit(self):
        # Single Instance Check
        if appconstants.AppSingleInstance:
            self.instancename = '%s-%s' % (appconstants.AppName, wx.GetUserId())
            self.instance = wx.SingleInstanceChecker(self.instancename)
            if self.instance.IsAnotherRunning():
                wx.MessageBox("Another instance is already running", "ERROR")
                return False

        # Set App/Vendor Names for Config
        self.SetAppName(appconstants.AppName)
        self.SetVendorName(appconstants.VendorName)

        # Get/Create a Global Config Object
        config = wx.ConfigBase.Get()
        config.SetRecordDefaults(True)

        # Send Logging to StdError
        wx.Log_SetActiveTarget(wx.LogStderr())
        # wx.Log_SetActiveTarget(wx.LogBuffer())

        self.view = mainframe.MainFrame(parent=None)
        title = appconstants.AppTitle + ' - ' + appconstants.AppVersion
        self.view.SetTitle(title)

        # Set the top window - no longer needed in recent wxPython versions
        # self.SetTopWindow(self.view)
        self.view.Show(True)

        return True

if __name__ == '__main__':
    # Run App avoiding redirection of errors to popup
    app = MainApp(redirect=False)
    app.MainLoop()
