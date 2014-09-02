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
import collections
import cPickle
import inspect
import itertools
import sys
import types
import weakref
import wx


from configcls import MutableSequence
from utils.doout import doout

class BindingAny(object):
    defclass = None
    wrattr = 'Write'
    rdattr = 'Read'

    ncache = dict()
    callbacks = collections.defaultdict(weakref.WeakKeyDictionary)

    def __init__(self, name, **kwargs):
        assert doout(name)
        self.name = name

        self.doconfig = kwargs.get('config', True)
        self.defval = kwargs.get('default', None)
        self.install()

    def getdefault(self):
        defval = self.__class__.defclass() if self.defval is None else self.defval
        return self.prewr(defval)

    @property
    def config(self):
        return wx.Config.Get()

    def wr(self, bindname, value):
        assert doout(value)
        if self.doconfig:
            wrfunc = getattr(self.config, self.wrattr)
            wrfunc(bindname, value)
            self.config.Flush()

    def rd(self, bindname):
        assert doout()
        if not self.doconfig:
            return self.getdefault()

        rdfunc = getattr(self.config, self.rdattr)
        value = rdfunc(bindname, self.getdefault())
        self.config.Flush()
        return value

    def postrd(self, value):
        return value

    def prewr(self, value):
        return value

    def addcallback(self, callback):
        assert doout(callback)
        # im_self ensures if the object is not there it will not be found
        bindname = self.makebindname(callback.im_self)
        try:
            self.callbacks[bindname][callback.im_self] = callback
        except KeyError:
            pass
        else:
            # Tell the callback the current value
            # (it will for example check/uncheck a checkbox)
            # callback(self.__get__(self, self.__class__))
            callback(self.__get__(callback.im_self, callback.im_self.__class__))


    def makebindname(self, obj):
        rootbindname = getattr(obj, 'bindname', '')
        bindname = '/'.join([rootbindname, self.name]).strip('/')
        return bindname.replace('//', '/')

    def install(self):
        for i in itertools.count(1):
            locals_ = sys._getframe(i).f_locals
            if '__module__' in locals_:
                locals_[self.name] = self
                # self.bindname = self.makebindname(locals_.get('bindname', ''))
                break
            
            self_ = locals_['self']
            cls = self_.__class__
            if self.__class__ != cls:
                if not hasattr(cls, self.name):
                    setattr(cls, self.name, self)
                    # self.bindname = self.makebindname(getattr(self_, 'bindname', ''))
                break

    def __get__(self, obj, cls=None):
        assert doout(obj, cls)
        if obj is None:
            # this prevents early auto-setting if for example a decorator does a "dir" of the class
            # attributes even before the registry object has been created and allows access to the object itself
            return self

        objbindname = self.makebindname(obj)

        try:
            return self.ncache[objbindname]
        except KeyError:
            value = self.rd(objbindname)
            value = self.postrd(value)
            self.ncache[objbindname] = value
            return value

    def __set__(self, obj, value, cb=True):
        assert doout(obj, value)
        objbindname = self.makebindname(obj)
        try:
            if self.ncache[objbindname] == value:
                return
        except KeyError:
            pass

        self.ncache[objbindname] = value
        value = self.prewr(value)
        self.wr(objbindname, value)
        # self.config.Flush()

        # Report to any callback
        # if obj is not None:
        if cb:
            map(lambda callback: callback(value), self.callbacks[objbindname].itervalues())


class BindingBool(BindingAny):
    defclass = bool
    wrattr = 'WriteBool'
    rdattr = 'ReadBool'

    def __init__(self, name, **kwargs):
        BindingAny.__init__(self, name, default=True, **kwargs)
        assert doout(name)

class BindingString(BindingAny):
    defclass = str
    wrattr = 'Write'
    rdattr = 'Read'

class BindingInt(BindingAny):
    defclass = int
    wrattr = 'WriteInt'
    rdattr = 'ReadInt'

class BindingFloat(BindingAny):
    defclass = int
    wrattr = 'WriteInt'
    rdattr = 'ReadInt'

class BindingList(BindingAny):
    defclass = MutableSequence
    wrattr = 'Write'
    rdattr = 'Read'

    def getdefault(self):
        defval = self.__class__.defclass(iterable=self.defval, owner=self)
        return self.prewr(defval)

    def postrd(self, value):
        # cPickle expexts str but wx.Config returns unicode
        # cPickle gives me a standard list which needs to be turned into our special MutableSequence
        return self.defclass(iterable=cPickle.loads(str(value)), owner=self)

    def prewr(self, value):
        return cPickle.dumps(value)


class MetaAuto(type):
    def __getattribute__(cls, name):
        attrname = type.__getattribute__(cls, 'attrname')
        if name == 'attrname':
            return attrname
        def decorator(*args, **kwargs):
            def wrapper(function):
                setattr(function, attrname, name)
                return function

            if len(args) == 1 and type(args[0]) == types.FunctionType:
                # Allow for attribute to be set without () if no additional parameters are needed
                return wrapper(args[0])

            return wrapper
        return decorator

class AutoAttribute(object):
    __metaclass__ = MetaAuto

class AutoBind(AutoAttribute):
    attrname = '_event_name'

class AutoCallback(AutoAttribute):
    attrname = '_var_name'


##################################################
# NOT USED RIGHT NOW
def WidgetBindings(cls):
    base1 = cls.__bases__[0] # wx.Frame/Dialog or similar
    baseoldinit = base1.__init__
    def basenewinit(self, *args, **kwargs):
        assert doout()
        baseoldinit(self, *args, **kwargs)
        modclsname = self.__class__.__module__ + '.' + self.__class__.__name__
        for widget in BindingWidget.defined[modclsname]:
            widget(owner=self)

    base1.__init__ = basenewinit
    return cls
##################################################

class BindingWidget(object):
    wprefix = None

    def __init__(self, name, **kwargs):
        assert doout(name)
        self.name = name
        self.wname = kwargs.get('wname', None)

        self.install()
        self.bindname = self.makebindname(self.owner)
        self.findwidget()
        self.createvars(**kwargs)
        self.dobindings()

    def makebindname(self, obj):
        rootbindname = getattr(obj, 'bindname', '')
        bindname = '/'.join([rootbindname, self.name]).strip('/')
        return bindname.replace('//', '/')

    def createvars(self, **kwargs):
        for binding in self.bindings:
            bindname = binding[0]
            bindclass = binding[1]
            bindkwargs = kwargs
            if len(binding) == 3:
                bindkwargs = kwargs.copy()
                bindkwargs.update(binding[2])

            bindclass(bindname, **bindkwargs)

    def install(self):
        for i in itertools.count(1):
            frame = sys._getframe(i)
            owner = frame.f_locals['self']
            if not isinstance(owner, self.__class__):
                self.owner = owner
                setattr(self.owner, self.name, self)
                return

        assert False, 'BindingWidget::install SHOULD never fail but it FAILED!'

    def findwidget(self):
        assert doout()
        if not self.wname:
            self.wname = 'm_' + self.wprefix.lower() + self.name.lower()

        for attr in dir(self.owner):
            if attr.lower() == self.wname:
                self.widget = getattr(self.owner, attr, None)
                break

        assert getattr(self, 'widget', None), 'Failed to acquire widget - ' + self.wname

    def dobindings(self):
        for methodname, method in inspect.getmembers(self.__class__, inspect.ismethod):
            if hasattr(method, AutoBind.attrname):
                event = getattr(wx, method._event_name)
                boundmethod = method.__get__(self, self.__class__)
                self.widget.Bind(event, boundmethod)
            elif hasattr(method, AutoCallback.attrname):
                boundmethod = method.__get__(self, self.__class__)
                attr = getattr(self.__class__, method._var_name)
                attr.addcallback(boundmethod)

    def _set(self, name, value):
        attr = getattr(self.__class__, name, None)
        attr.__set__(self, value, cb=False)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            # FIXME: I do potentially need to look for self.widget
            # avoiding a recursion
            widget = object.__getattribute(self, 'widget')
            return getattr(widget, name)

class BindingCheckBox(BindingWidget):
    wprefix = 'checkBox'
    bindings = (('value', BindingBool),)

    def __init__(self, name, **kwargs):
        assert doout(name, kwargs)
        BindingWidget.__init__(self, name, **kwargs)

    @AutoBind.EVT_CHECKBOX
    def OnCheckBox(self, event):
        assert doout(event)
        event.Skip()
        # self.value = event.GetInt()
        # This avoids a callback to 
        self._set('value', event.GetInt())

    @AutoCallback.value
    def OnValueChange(self, value):
        assert doout(value)
        self.widget.SetValue(value)

class BindingTextCtrl(BindingWidget):
    wprefix = 'textCtrl'
    bindings = (('value', BindingString),)

    def __init__(self, name, **kwargs):
        assert doout(name, kwargs)
        BindingWidget.__init__(self, name, **kwargs)

    @AutoBind.EVT_TEXT
    def OnText(self, event):
        assert doout(event)
        event.Skip()
        self._set('value', event.GetString())

    @AutoCallback.value
    def OnValueChange(self, value):
        assert doout(value)
        self.widget.SetValue(value)

class BindingTextCtrlFocus(BindingWidget):
    wprefix = 'textCtrl'
    bindings = (('value', BindingString),)

    def __init__(self, name, **kwargs):
        assert doout(name, kwargs)
        BindingWidget.__init__(self, name, **kwargs)

    @AutoBind.EVT_KILL_FOCUS
    def OnKillFocus(self, event):
        assert doout(event)
        event.Skip()
        self._set('value', self.widget.GetValue())

    @AutoCallback.value
    def OnValueChange(self, value):
        assert doout(value)
        self.widget.SetValue(value)


class BindingComboBox(BindingWidget):
    # Index vs StringSelection in the 'config' hive
    # If index is saved and the "sorted" property of the control is changed
    # the indices will not match the strings
    # But if the saved item to the config is which string was selected (hence: 'stringselection')
    # such quirk will not show up

    wprefix = 'comboBox'
    bindings = (
        ('selection', BindingInt, {'config': False}),
        ('items', BindingList),
        ('stringselection', BindingString),
        ('value', BindingString),
    )

    def __init__(self, name, **kwargs):
        assert doout(name, kwargs)
        BindingWidget.__init__(self, name, **kwargs)

    @AutoBind.EVT_COMBOBOX
    def OnComboBox(self, event):
        assert doout(event)
        event.Skip()
        self._set('selection', event.GetInt())
        self._set('stringselection', event.GetString())

    @AutoBind.EVT_TEXT
    def OnText(self, event):
        assert doout(event)
        event.Skip()
        self.value = event.GetString()

    @AutoBind.EVT_TEXT_ENTER
    def OnTextEnter(self, event):
        assert doout(event)
        event.Skip()
        self.value = event.GetString()
        self.items.append(self.value)
        self.stringselection = self.value

    @AutoCallback.value
    def OnTextChange(self, value):
        assert doout(value)
        self.widget.SetValue(value)

    @AutoCallback.selection
    def OnSelectionChange(self, value):
        assert doout(value)
        self.widget.SetSelection(value)

    @AutoCallback.items
    def OnItemsChange(self, value):
        assert doout(value)
        # FIXME:
        # A more complex policy is needed to ensure that if string x is selected
        # it remains selected after we clear the combobox or if for example the previous
        self.widget.Clear()
        self.widget.SetItems(value)

        self.stringselection = self.stringselection # make sure it's selected if possible

    @AutoCallback.stringselection
    def OnStringSelectionChange(self, value):
        assert doout(value)
        retval = self.widget.SetStringSelection(value)
        # The variable must contain the reality and not what was sent, because the operation may fail
        # if the "value" is not in the list of items (use _set to avoid an infinite loop)
        self._set('stringselection', self.widget.GetStringSelection())
        # No event was emitted ... manual selection update
        self._set('selection', self.widget.GetSelection())
        return retval

class BindingFilePicker(BindingWidget):
    wprefix = 'filePicker'
    bindings = (('path', BindingString),)

    @AutoBind.EVT_FILEPICKER_CHANGED
    def OnFilePickerChanged(self, event):
        assert doout(event)
        event.Skip()
        # value can also be gotten from self.widget
        self._set('path', event.GetPath())

    @AutoCallback.value
    def OnPathChange(self, path):
        assert doout(value)
        # FIXME: Should this check if the input is a real valid file?
        # Alternative the BindingString can be marked as read-only (need to develop)
        # and only settable via a direct call to __set__
        self.widget.SetPath(path)

class BindingDirPicker(BindingWidget):
    wprefix = 'dirPicker'
    bindings = (('path', BindingString),)

    @AutoBind.EVT_DIRPICKER_CHANGED
    def OnFilePickerChanged(self, event):
        assert doout(event)
        event.Skip()
        # value can also be gotten from self.widget
        self._set('path', event.GetPath())

    @AutoCallback.value
    def OnPathChange(self, path):
        assert doout(value)
        # FIXME: Should this check if the input is a real valid dir?
        # Alternative the BindingString can be marked as read-only (need to develop)
        # and only settable via a direct call to __set__
        self.widget.SetPath(path)


class WGroup(object):

    def __init__(self, name, status):
        self.name = name
        self.status = status
        self.widgets = list()
        self.install()

    def install(self):
        for i in itertools.count(1):
            frame = sys._getframe(i)
            owner = frame.f_locals['self']
            if not isinstance(owner, self.__class__):
                self.owner = owner
                setattr(self.owner, self.name, self)
                return

        assert False, 'BindingWidget::install SHOULD never fail but it FAILED!'

    def __lshift__(self, widget):
        self.findwidget(widget)
        return self

    def enable(self, status=True):
        self.status = status
        for wwidget, widget in self.widgets:
            if wwidget.wprefix in ['tool',]:
                tb = widget.GetToolBar()
                tb.EnableTool(widget.GetId(), self.status)
            else:
                widget.Enable(self.status)
        self.owner.Refresh()

    def disable(self):
        self.enable(status=False)

    def reverse(self):
        self.enable(status=not self.status)

    def findwidget(self, wwidget):
        wnamelow = wwidget.name.lower()
        for attr in dir(self.owner):
            if attr.lower() == wnamelow:
                widget = getattr(self.owner, attr, None)
                self.widgets.append((wwidget, widget))
                if wwidget.wprefix in ['tool',]:
                    tb = widget.GetToolBar()
                    tb.EnableTool(widget.GetId(), self.status)
                else:
                    widget.Enable(self.status)

                return

        assert 'Failed to acquire widget - ' + widget.name

class WidgetGeneric(object):
    def __init__(self, name):
        self.name = 'm_' + self.wprefix + name

class WButton(WidgetGeneric):
    wprefix = 'button'

class WTool(WidgetGeneric):
    wprefix = 'tool'

class WMenuItem(WidgetGeneric):
    wprefix = 'menuItem'

class WCheckBox(WidgetGeneric):
    wprefix = 'checkBox'
