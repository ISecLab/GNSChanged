# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# code@gns3.net
#

import sys
import GNS3.Globals as globals
from optparse import OptionParser
from GNS3.Application import Application
from GNS3.Utils import translate
from PyQt4 import QtCore
from __main__ import VERSION  
import os,errno
from time import sleep



def pid_is_running(pid):
""" Функция проверяет запущен ли процесс
    Если процесс работает то возвращает True иначе False
"""    
    if pid < 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError, e:
        return e.errno == errno.EPERM
    else:
        return True

def write_pidfile_or_die(path_to_pidfile):
""" Функция проверяет наличие PID в файле path_to_pidfile
    Если процесс PID которого записан в файле запущен, то программа завершается с кодом 1 
""" 
    if os.path.exists(path_to_pidfile):
        pid = int(open(path_to_pidfile).read())
        if pid_is_running(pid):
            print("Sorry, found a pidfile!  Process {0} is still running.".format(pid))
            exit(1)
        else:
            os.remove(path_to_pidfile)
    open(path_to_pidfile, 'w').write(str(os.getpid()))
    return path_to_pidfile


#определЯется путь к PID файлу 
userName = os.environ.get( "USERNAME" )
pidfile = "/home/" + userName +  "/.gns3/gns.pid"

#Если GNS уже запущен то завершаем программу
write_pidfile_or_die(pidfile)

usage = "usage: %prog [--debug] [--configdir <config_dir>] <net_file>"
parser = OptionParser(usage, version="%prog " + VERSION)
parser.add_option("-d", "--debug", action="store_true", help="display debug messages")
parser.add_option("-c", "--configdir", action="store_true", dest="config_dir", help="directory where gns3.ini is located")

try:
    (options, args) = parser.parse_args()
except SystemExit:
    sys.exit(1)

if options.debug == True:
    globals.debugLevel = 2

if options.config_dir == True:
    if len(args) >= 1:
        config_dir = args.pop()
        if sys.platform.startswith('win'):
            QtCore.QSettings.setPath(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, config_dir)
        else:
            print unicode(translate("Main", "On Unix you can choose the config directory by setting the XDG_CONFIG_HOME environment variable"))
            sys.exit(1)
    else:
        print usage
        sys.exit(1)

file = None

if len(args) >= 1:
    file = args.pop()

app = Application()
app.run(file)
