# -*- coding: utf-8 -*-
from  myfile import vlan ,server, work_dir
import commands
"""
Этот скрипт должен быть в автозагруке 
Выполняет монтирование расшаренных на сервере папок, необходимых для работы GNS:
- монтирование временной рабочей директории
- монтирование папки с проектами 
"""
print commands.getoutput("mkdir " + work_dir)
print commands.getoutput("mount -t nfs " + server + ":/nfs/virtualization/GNS3Files/labs/labs /usr/share/GNS3/labs/labs")
print commands.getoutput("mount -t nfs " + server + ":/nfs/virtualization/GNS3Files/labs/test_labs /usr/share/GNS3/labs/test_labs")
print commands.getoutput("mount -t nfs " + server + ":" + work_dir + " " + work_dir)
print commands.getoutput("chmod -R 0777 " + work_dir )

