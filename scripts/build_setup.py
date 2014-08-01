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
import argparse, subprocess, sys
import build_utils

iscc_cmd = ['iscc',]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare iss file and build setup file')
    parser.add_argument('--iss', action='store_true', help='do only prepare the iss file')
    args = parser.parse_args()

    print '**-- Beginning of operations - Preparation of iss file'

    appinfo = build_utils.AppInfo()

    print 'Locating the innosetup iss file'
    issfile = appinfo.getissfile()
    if not issfile:
        print '-- ERROR: iss file not found'
        sys.exit(1)

    print 'Preparing iss file'
    appinfo.prepare_issfile()

    if args.iss:
        print '--- Generated iss file. Exiting'
        sys.exit(0)

    print '-- Generation of setup'
    print '-- Checking build/dist directories'
    if not appinfo.check_dirs_exe():
        print '--- Found not build directory. Exiting'
        sys.exit(0)

    print '--- Making dist dir'
    appinfo.make_dirs_setup()

    print 'Copying distributable files'
    appinfo.copy_exedist_to_setupbuild()

    print 'Copying data files/directories to build directory'
    appinfo.copy_items_to_setupbuild()

    iscc_cmd.append(issfile)
    print 'Generating executable with command: %s' % ' '.join(iscc_cmd)
    subprocess.call(iscc_cmd)
    print '-- End of operations'
