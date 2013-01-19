#-*- coding: utf-8 -*-
import commands

numberOfClients = 20

#разность значений начальных консольных портов между клиентами
deltaVideoPort = 50

#разность значений начальных udp-портов между клиентами;
deltaConnectionPort = 100

#начальный udp-порт первого vlan для dynamips;
base_dynamips_udp = 10000

#начальный udp-порт первого vlan для виртуальных машин;
base_qemu_udp = 20000
#начальный AUX порт первого vlan для dynamips;
base_aux = 1050
#начальный консольный порт первого vlan для dynamips;
base_dynamips_console = 2000
#начальный номер окна для VNC (порт=5900+номер окна) первого vlan для виртуальных машин
base_qemu_console = 0 
#начальный порт гипервизора dynamips 
base_dynamips_port = 7200
#начальный порт Qemuwrapper
base_qemu_port = 10525
#начальный порт server.py
base_gns_control_port = 27025
#третье число в IP адресе это номер VLAN 
vlan = int(commands.getoutput("ifconfig").split("\n")[1].split()[1][5:].split(".")[2])

gns_control_port = base_gns_control_port + vlan
dynamips_port = base_dynamips_port + vlan
qemu_port = base_qemu_port + vlan

server = "172.16.0.100"

vncCommandForQemu = "vncviewer " 

work_dir = "/tmp/" +str(vlan)

labs_dir = "/usr/share/GNS3/labs/test_labs"
gns_folder = "/usr/share/GNS3"

qemu_server = server + ":" + str(qemu_port) 
dynamips_server = server + ":" + str(dynamips_port) 

#функция вычисления консольного порта для VLAN
def getVideoPort(base_port):
    return base_port + deltaVideoPort*vlan
    
#функция вычисления UDP порта для VLAN
def getConnectionPort(base_port):
    return base_port + deltaConnectionPort*vlan

#Команды которые принимает server.py 
loadWorkDir = "loadWorkDir"
cleanWorkDir = "cleanWorkDir"
die = "die"
saveWorkDir = "saveWorkDir"
