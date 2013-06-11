#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: network.py
# Copyright (c) 2013 by None
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = 'Costas Tyfoxylos'
__docformat__ = 'plaintext'
__date__      = '07/06/2013'

import sys
if sys.platform == 'linux2':
    import fcntl, socket, struct
from subprocess import Popen, PIPE

class Network(object):
    def __init__(self):
        if sys.platform == 'linux2':
            self.gateway, self.interface = self.__getGatewayInterfaceL()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.netmask = self.__getNetmaskL(sock, self.interface)
            self.ipAddress = self.__getIpAddressL(sock, self.interface)
            self.macAddress = self.__getMacAddressL(sock, self.interface)
        elif sys.platform == 'win32':
            self.gateway, self.ipAddress = self.__getGatewayInterfaceIpW()
            ipconfig =  Popen(['ipconfig','/all'], stdout=PIPE).stdout.read()
            interface = ipconfig[ipconfig.find('Description'):ipconfig.find('Default Gateway')]
            while self.ipAddress not in interface:
                ipconfig = ipconfig.replace(interface, '')
                interface = ipconfig[ipconfig.find('Description'):ipconfig.find('Default Gateway')]                
            self.netmask = self.__getNetmaskW(interface, self.ipAddress)
            self.macAddress = self.__getMacAddressW(interface, self.ipAddress)            
            self.interface = self.__getInterfaceW(interface, self.ipAddress)                
        else:
            print 'Unknown platform'
            raise SystemExit

    def __getGatewayInterfaceL(self):
        route = Popen(['ip', 'route'], stdout=PIPE).stdout.read()
        for line in route.splitlines():
            if line.startswith('default'):
                route = line
                break
        return route.split()[2], route.split()[4]

    def __getNetmaskL(self, sock, interface): 
        netmask = fcntl.ioctl(sock, 0x891b, struct.pack('256s', interface))[20:24]
        return socket.inet_ntoa(netmask)

    def __getIpAddressL(self, sock, interface):
        ipAddress = fcntl.ioctl(sock.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24]
        return socket.inet_ntoa(ipAddress)
    
    def __getMacAddressL(self, sock, interface):
        info = fcntl.ioctl(sock.fileno(), 0x8927,  struct.pack('256s', interface[:15]))
        return ''.join(['%02x-' % ord(char) for char in info[18:24]])[:-1]
    
    def __getGatewayInterfaceIpW(self):
        route = Popen(['route','print'], stdout=PIPE).stdout.read()
        for line in route.splitlines():
            if 'Default Gateway' in line:
                gateway = line.split(':')[1].strip()
                break
        text=route[route.find('Active Routes'):route.find('Default Routes')]
        for line in text.splitlines()[2:-1]:
            if line.split()[2].strip() == gateway:
                ip = line.split()[3]
                break
        return gateway, ip
    
    def __getMacAddressW(self, ipconfig, ip):
        for line in ipconfig.splitlines():
            if line.strip().startswith('Physical'):
                mac = line.split(':')[1].strip()
                break        
        return mac            
    def __getNetmaskW(self, ipconfig, ip): 
        for line in ipconfig.splitlines():
            if line.strip().startswith('Subnet'):
                netmask = line.split(':')[1].strip()
                break
        return netmask
    
    def __getInterfaceW(self, ipconfig, ip):
        for line in ipconfig.splitlines():
            if line.strip().startswith('Description'):
                interface = line.split(':')[1].strip()
                break
        return interface    
    
    
    
