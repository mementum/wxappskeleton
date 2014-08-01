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
import functools
import glob
import imp
import inspect
import os.path
from pubsub import pub
import sys
import types
import weakref
import wx

rootdir='.'

def load_modules(cls, subdirs, relpath=None):
    '''
    1. Find out what the base path is for the application
    2. Get the classname
    3. Find in subdirectories views and controllers
    3.1 A classname.py file
    3.2 One or more classname/*.py files
    4. Load and return the found py files
    '''

    clsmod = sys.modules[cls.__module__]
    modpathbase = os.path.dirname(clsmod.__file__)

    clsname = cls.__name__
    clsnamelow = clsname.lower()
    loadedmodules, findfailed, loadfailed = list(), list(), list()

    for subdir in subdirs:
        modpath = os.path.join(modpathbase, subdir)

        modpys = list()

        # Check (case insensitive) if a file with the classname exists
        modpathpys = os.path.join(modpath, '*.py')
        for modpy in glob.glob(modpathpys):
            modname = os.path.basename(modpy)
            modname, modext = os.path.splitext(modname)
            if clsnamelow == modname.lower():
                modpys.append(modpy)
                break

        # Check (case insensitive) if a directory with the classname exists
        modpathpydirs = os.path.join(modpath, '*')
        modpydirs = filter(os.path.isdir, glob.glob(modpathpydirs))
        for modpydir in modpydirs:
            modpydirname = os.path.basename(modpydir)
            if clsnamelow == modpydirname.lower():
                modpys.extend(glob.glob(os.path.join(modpydir, '*.py')))

        for modpy in modpys:
            moddir = os.path.dirname(modpy)
            modname = os.path.basename(modpy)
            modname, modext = os.path.splitext(modname)

            try:
                # foundmodule = imp.find_module(modname, [modpath,])
                foundmodule = imp.find_module(modname, [moddir,])
            except Exception, e:
                findfailed.append((modpy, e))
                continue

            try:
                loadedmodule = imp.load_module(modname, *foundmodule)
            except Exception, e:
                loadfailed.append((modpy, e))
                continue

            # everything worked ...
            loadedmodules.append(loadedmodule)

    return loadedmodules, findfailed, loadfailed

def _reload_modules(klass, reloading=True):
    def fgetter(funcname):
        def realfgetter(owner, *args, **kwargs):
            return owner._dynmethods[funcname](owner, *args, **kwargs)
        return realfgetter

    klass._ldmodules, klass._findfailed, klass._loadfailed = load_modules(klass, subdirs=klass._moddirs)
    for ldmodule in klass._ldmodules:
        for funcname in dir(ldmodule):
            if funcname.startswith('_'):
                continue
            func = getattr(ldmodule, funcname)
            if isinstance(func, types.FunctionType):
                newfunc = funcname not in klass._dynmethods
                klass._dynmethods[funcname] = func
                if not reloading or newfunc:
                    funcgetter = fgetter(funcname)
                    funcgetter._pubrecv = getattr(func, '_pubrecv', None)
                    setattr(klass, funcname, funcgetter)

    if reloading:
        for instance in klass._instances:
            instance._subscribe()

def _subscribe(self):
    def sgetter(funcname):
        def realsgetter(owner, msg):
            return owner._subs[funcname](owner, msg)
        return realsgetter

    # wx classes throw exception if getmember is applied to the instance (self)
    methods = inspect.getmembers(self.__class__, inspect.ismethod)
    topicmgr = pub.getDefaultTopicMgr()
    for mname, method in methods:
        pubsubtopic = getattr(method, '_pubrecv', None)
        if pubsubtopic:
            self._subs[mname] = method
            subsgetter = sgetter(mname)
            if not topicmgr.getTopic(pubsubtopic, True) or not pub.isSubscribed(subsgetter, pubsubtopic):
                setattr(self, mname, subsgetter)
                pub.subscribe(subsgetter.__get__(self, self.__class__), pubsubtopic)

def DynamicClass(moddirs=None):
    if not moddirs:
        moddirs = ['.', 'mods', 'modules']

    def ClassWrapper(cls):
        def _getview(self):
            return self
        cls.view = property(_getview)

        cls._subscribe = _subscribe

        def _newinit(self, *args, **kwargs):
            cls._instances.add(self)
            self._subs = dict()
            self._subscribe()
            _oldinit(self, *args, **kwargs)

        _oldinit, cls.__init__ = cls.__init__, _newinit

        cls._instances = weakref.WeakSet()
        cls._dynmethods = dict()
        cls._moddirs = moddirs
        cls._reload_modules = classmethod(_reload_modules)
        cls._reload_modules(reloading=False)

        return cls

    return ClassWrapper

def PubRecv(topic):
    def decorate(func):
        func._pubrecv = topic
        return func
    return decorate

def PubSend(topic, queue=True):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            msg = func(self, *args, **kwargs)
            if queue:
                wx.CallAfter(pub.sendMessage, topic, msg=msg)
            else:
                pub.sendMessage(topic, msg=msg)
        return wrapper
    return decorate
