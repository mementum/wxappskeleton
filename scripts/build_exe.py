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
import argparse
import subprocess, sys

import build_utils

##################################################
# APPLICATION INFORMATION
##################################################
appconstants = 'appconstants'

##################################################
# CONSTANTS FOR SPEC GENERATION
##################################################
# pyinstaller can generate spec and executable in one step
# specs_cmd = ['pyinstaller', '--noconfirm', '--windowed', '--noupx']

# Base command for spec generation
# --noconfirm is not accepted by pyi-makespec
specs_cmd = ['pyi-makespec', '--noupx',]

# Base command for executable generation
pyinst_cmd = ['pyinstaller', '--noconfirm']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare spec file and generate executable')
    parser.add_argument('-s', '--spec', action='store_true', help='do only prepare the spec file')
    parser.add_argument('-n', '--nodebug', action='store_false', default=True, help='do not optimize python (thus removing debugging)')
    args = parser.parse_args()

    print '** Building Application Information Object'
    appinfo = build_utils.AppInfo()
    print '-- Trying to locate specfile'
    specfile = appinfo.getspecfile()

    if args.spec or not specfile:
        if args.spec:
            if specfile:
                print '-- Current Specfile will be overwritten'
            else:
                print '-- New specfile will be created'
        else:
            print '-- No specfile found - creating one for executable generation'

        print '-- Building spec generation command'
        specs_cmd.append('--specpath=' + appinfo.dirs['script'])
        specs_cmd.append('--additional-hooks-dir=' + appinfo.dirs['hooks'])

        specs_cmd.append('--name=' + appinfo.getappinfo('AppName'))

        specs_cmd.append('--' + appinfo.getappinfo('AppExeType', 'onefile'))
        specs_cmd.append('--' + appinfo.getappinfo('AppUIType', 'windowed'))

        pywfile = appinfo.getpywfile()
        if not pywfile:
            print '-- ERROR: no pyw file found to generate the spec'
            sys.exit(1)
        specs_cmd.append(pywfile)

        print '-- Calling the following command:', ' '.join(specs_cmd)
        subprocess.call(specs_cmd)
        print '**-- End of operations'

        print '-- ADDING/REMOVING Debug Information'
        appinfo.debug_specfile(args.nodebug)
        if args.spec:
            # Do only exit if only "spec generation was requested"
            sys.exit(0)

        # Fill in the variable just in case it was empty
        specfile = appinfo.getspecfile()



    print '**-- Beginning of operations'
    print '-- Cleaning up backups/compiled pythons'
    appinfo.clean_srcdir()

    print '-- Making (deleting if needed) previous executable generation directories'
    appinfo.make_dirs_exe()

    pyinst_cmd.append('--workpath=' + appinfo.dirs['exe_build'])
    pyinst_cmd.append('--distpath=' + appinfo.dirs['exe_dist'])

    print '-- Adding specfile to command line arguments'
    pyinst_cmd.append(specfile)

    print '-- Generating executable with command: %s' % ' '.join(pyinst_cmd)
    subprocess.call(pyinst_cmd)
    print '**-- End of operations'
