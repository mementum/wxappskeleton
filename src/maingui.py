# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Sample Text" ), wx.VERTICAL )
		
		self.m_textCtrlSampleText = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,75 ), wx.TE_MULTILINE )
		sbSizer1.Add( self.m_textCtrlSampleText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_checkBoxSameStatus = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"I will have the same status upon restart (unless registry is cleared)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_checkBoxSameStatus, 0, wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Sample Text 2" ), wx.VERTICAL )
		
		self.m_textCtrlSampleText2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,75 ), wx.TE_MULTILINE )
		sbSizer2.Add( self.m_textCtrlSampleText2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer2.Add( sbSizer2, 0, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"Get MOTD", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Click Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, u"Reload Modules", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear Registry && Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer3, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"label" ), wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_comboBoxTestChoices = []
		self.m_comboBoxTest = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBoxTestChoices, 0 )
		bSizer4.Add( self.m_comboBoxTest, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear Combo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button6 = wx.Button( self.m_panel1, wx.ID_ANY, u"Add Element", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button6, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_button7, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( bSizer5, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer2.Add( sbSizer3, 0, wx.EXPAND, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Some Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer6.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlSomeText = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_textCtrlSomeText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_button9 = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_checkBoxSameStatus.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxSameStatus )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnButtonClickGetMOTD )
		self.m_button1.Bind( wx.EVT_BUTTON, self.OnButtonClickClickMe )
		self.m_button3.Bind( wx.EVT_BUTTON, self.OnButtonClickReloadModules )
		self.m_button6.Bind( wx.EVT_BUTTON, self.OnButtonClickAddElement )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnButtonClickSomeText )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnCheckBoxSameStatus( self, event ):
		event.Skip()
	
	def OnButtonClickGetMOTD( self, event ):
		event.Skip()
	
	def OnButtonClickClickMe( self, event ):
		event.Skip()
	
	def OnButtonClickReloadModules( self, event ):
		event.Skip()
	
	def OnButtonClickAddElement( self, event ):
		event.Skip()
	
	def OnButtonClickSomeText( self, event ):
		event.Skip()
	

