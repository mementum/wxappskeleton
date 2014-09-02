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
import imp
import os.path
import sys

# Find out where the script is. The script is an argument to pyi-build/pyinstaller
scriptdir = None
for arg in sys.argv[1:]:
    if not arg.endswith('.spec'):
        continue
    scriptdir = os.path.normpath(os.path.dirname(arg))
    break

# This should never happen, but checking is ok
if not scriptdir:
    raise Exception('Specfile not found in arguments to pyinstaller')

# Import own build_utils module, which should be besides the specfile
build_utils_name = 'build_utils'
try:
    # find the module
    foundmodule = imp.find_module(build_utils_name, [scriptdir,])
except Exception, e:
    raise e
else:
    try:
        # import the found module
        build_utils = imp.load_module(build_utils_name, *foundmodule)
    except Exception, e:
        raise e

# Create an applicatio info object
appinfo = build_utils.AppInfo(scriptdir)
# appinfo.compile_srcdir()

block_cipher = None

# Analysis phase
a = Analysis([appinfo.getappscript(),],
             pathex=[],
             hiddenimports=[],
             runtime_hooks=None,
             hookspath=[appinfo.getdir('hooks'),],
             cipher=block_cipher)

# Add optimization if needed
a.scripts += appinfo.getapppyoptimize()

# Add any app defined datas to binaries
a.datas += appinfo.toc_datas(tree_class=Tree)

# User32 must not be pulled in ... problem in development version os PyInstaller 2.1
# Must be done before binaries is put into coll_args
a.binaries -= [('user32.dll', None, None),]

# Default Collect Arguments from analysis
coll_args = [a.binaries, a.zipfiles, a.datas]

# onefile/onedir determines what goes to the executable (in args/kwargs form)
exe_args = [] if appinfo.getapponedir() else coll_args
exe_kwargs = dict()

# If UAC control must go to manifest add the options
appinfo.getuacadmin(exe_kwargs)

# Produce the Pure Python modules toc
pyz = PYZ(a.pure,
          cipher=block_cipher)

# Produce the exceutable
exe = EXE(pyz,
          a.scripts,
          *exe_args,
          name=appinfo.getappexename(),
          exclude_binaries=appinfo.getapponedir(),
          console=appinfo.getappconsole(),
          debug=False,
          strip=None,
          upx=False,
          **exe_kwargs)

# Collect phase in onedir mode if needed
if appinfo.getapponedir():
    coll = COLLECT(exe,
                   *coll_args,
                   name=appinfo.getappname(),
                   strip=None,
                   upx=False)

else:
    # Copy some needed datas to the onefile executable (ex: LICENSE)

    # Cannot be done earlier because the destination directories may not exist
    # This copies files like README/LICENSE which must be besides the executable
    # Even if embedded in the executable, they must also be in the exe dir
    appinfo.copy_datas()
