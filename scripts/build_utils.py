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
import fnmatch, glob, imp, os, os.path, shutil, sys, tempfile, uuid
#
# Line buffering is broken in Win32 platforms
# Running under cygwin/mingw32 this is needed to see a line
# show up when the print statement is issued
class flushfile(object):
    def __init__(self, f):
        self.f = f

    def write(self, x):
        self.f.write(x)
        self.f.flush()

if sys.platform == 'win32':
    sys.stdout = flushfile(sys.stdout)
    sys.stderr = flushfile(sys.stderr)

##################################################
# CONFIGURABLE VALUES
##################################################
copy_items = {
    # diralias, [item_list]
    'base': ['README.md', 'LICENSE'],
    'src': [],
}

inno_replace = ['AppName', 'AppVersion', 'AppPublisher', 'AppYear', 'AppURL', 'AppExeName', 'AppId']
inno_appid = ['AppId',]
inno_dirs = {'BuildDir': 'setup_build', 'DistDir': 'setup_dist'}

clean_patterns = ['*~', '*.bak', '*.pyc', '*.pyo',]

appinfomodname = 'appconstants'

appdirs = [
    # dirname, basedir, dir relative path
    ('script', 'app', '.'),
    ('base', 'script', '..'),
    ('hooks', 'script', 'hooks'),
    ('src', 'base', 'src'),

    # Base Directory for binaries
    ('binaries', 'base', 'binaries'),

    # Executable Generation/Distribution Directories
    ('exe', 'binaries', 'exe'),
    ('exe_build', 'exe', 'build'),
    ('exe_dist', 'exe', 'dist'),

    # Setup Generation/Distribution Directories
    ('setup', 'binaries', 'setup'),
    ('setup_build', 'setup', 'build'),
    ('setup_dist', 'setup', 'dist'),
]

appreldirs = [
    # Inno Setup needs relative paths to the script in the iss file
    ('setup_build', 'setup_build', 'script'),
    ('setup_dist', 'setup_dist', 'script'),
]

##################################################
# Operational object for Executable and Setup generation
##################################################
class AppInfo(object):

    def __init__(self):
        self.init_dirs()
        self.init_module()

    def init_dirs(self):
        self.dirs = dict()
        self.reldirs = dict()

        if getattr(sys, 'frozen', False):
            self.dirs['app'] = os.path.dirname(sys.executable)
        elif __file__:
            self.dirs['app'] = os.path.dirname(sys.argv[0])

        for appdir in appdirs:
            dirname, basedir, dirext = appdir
            self.dirs[dirname] = os.path.join(self.dirs[basedir], dirext)

        for appreldir in appreldirs:
            dirname, basedir, dirext = appreldir
            dirrel = self.dirs[dirext]
            self.reldirs[dirname] = os.path.relpath(self.dirs[basedir], dirrel)

    def init_module(self):
        try:
            foundmodule = imp.find_module(appinfomodname, [self.dirs['src'],])
        except Exception, e:
            raise e

        try:
            self.appinfomod = imp.load_module(appinfomodname, *foundmodule)
        except Exception, e:
            raise e

    def getappinfo(self, varname, defvalue=None):
        return getattr(self.appinfomod, varname, defvalue)

    def getfilepath(self, dirname, appvar, ext, optional=None):
        filedir = self.dirs[dirname]
        filename = self.getappinfo(appvar) + '.' + ext
        filepath = os.path.join(filedir, filename)
        if os.path.isfile(filepath):
            return glob.glob(filepath)[0]
        if optional:
            filename = optional + '.' + ext
            filepath = os.path.join(filedir, filename)
            if os.path.isfile(filepath):
                return glob.glob(filepath)[0]
        return None

    def getspecfile(self):
        return self.getfilepath('script', 'AppName', 'spec', 'pyinstaller')

    def getpywfile(self):
        return self.getfilepath('src', 'AppName', 'pyw', 'main')

    def getissfile(self):
        return self.getfilepath('script', 'AppName', 'iss', 'innosetup')

    def clean_srcdir(self):
        clean_dir = self.dirs['src']
        for root, dirs, files in os.walk(clean_dir):
            for clean_pattern in clean_patterns:
                for filename in fnmatch.filter(files, clean_pattern):
                    os.remove(os.path.join(root, filename))

    def check_dir_build(self):
        return os.path.isdir(self.dirs['build'])

    def make_del_dir(self, dirname):
        dirpath = self.dirs[dirname]
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)

    def make_dirs_exe(self):
        self.make_del_dir('binaries')
        self.make_del_dir('exe')
        self.make_del_dir('exe_build')
        self.make_del_dir('exe_dist')

    def check_dirs_exe(self):
        distdir = self.dirs['exe_dist']
        return os.path.isdir(distdir) and len(os.listdir(distdir))

    def make_dirs_setup(self):
        self.make_del_dir('setup')
        self.make_del_dir('setup_build')
        self.make_del_dir('setup_dist')

    def debug_specfile(self, nodebug):
        #Create temp file
        ofilehandle, ofilepath = tempfile.mkstemp() # open temporary file
        ofile = os.fdopen(ofilehandle, 'w')  # wrap fhandle in "file object"

        ifilepath = self.getspecfile()
        ifile = open(ifilepath) # open original file
        for line in ifile:
            if 'a.scripts' in line:
                print 'FOUND a.scripts and nodebug is', nodebug
                line = '          a.scripts'
                if nodebug:
                    line += " + [('O','','OPTION')]"
                line += ',\n'

            ofile.write(line)

        ofile.close() # close temp file
        ifile.close() # close original file
        os.remove(ifilepath) # remove original file
        shutil.move(ofilepath, ifilepath) # move new file

    def prepare_issfile(self):
        #Create temp file
        ofilehandle, ofilepath = tempfile.mkstemp() # open temporary file
        ofile = os.fdopen(ofilehandle, 'w')  # wrap fhandle in "file object"

        ifilepath = self.getissfile()
        ifile = open(ifilepath) # open original file
        for line in ifile:
            line = self.replace_lines(line)
            ofile.write(line)

        ofile.close() # close temp file
        ifile.close() # close original file
        os.remove(ifilepath) # remove original file
        shutil.move(ofilepath, ifilepath) # move new file

    def replace_lines(self, line):
        if line.startswith('#define'):
            # Do the replacement magic here
            define, defname, defvalue = line.strip('\r\n').split(None, 2)

            # check if defname is on the list of replacements
            # if yes replace using "" for the value
            # else write the original line
            defkey = defname[2:] # remove "My"
            # Remove the quotes from the value
            value = defvalue.strip('"')

            if defkey in inno_replace:
                if defkey == 'AppId':
                    # try to validate a uuid and if failed - generate one
                    # unless manually removed, it will only be done once
                    try:
                        valid_uuid = uuid.UUID(value, version=4)
                    except ValueError:
                        value = uuid.uuid4()
                else:
                    value = self.getappinfo(defkey)
            elif defkey in inno_dirs:
                dirname = inno_dirs[defkey]
                value = self.reldirs[dirname]
            
            line = ' '.join([define, defname, '"%s"' % value]) + '\n'

        return line

    def copy_exedist_to_setupbuild(self):
        src = self.dirs['exe_dist']
        dst = self.dirs['setup_build']

        src_files_dirs = glob.glob(os.path.join(src, '*'))

        copy_files = lambda x: shutil.copy(x, dst)
        src_files = filter(os.path.isfile, src_files_dirs)
        map(copy_files, src_files)

        copy_dirs = lambda x: shutil.copytree(x, dst)
        src_dirs = filter(os.path.isdir, src_files_dirs)
        map(copy_files, src_dirs)

    def copy_items_to_setupbuild(self):
        for dirname, items in copy_items.iteritems():
            for item in items:
                itempath = self.dirs[dirname]
                srcpath = os.path.join(itempath, item)
                dstpath = os.path.join(self.dirs['setup_build'], item)

                if os.path.isfile(srcpath):
                    shutil.copy(srcpath, dstpath)
                else:
                    shutil.copytree(srcpath, dstpath)
