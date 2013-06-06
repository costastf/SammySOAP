#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: changeVolume.py
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
__date__      = '06/06/2013'

import sys, httplib

def sanitizeVolume(volume):
    try:
        volume = int(volume)
        if volume > 99 or volume < 0:
            volume = False
    except:
        volume = False
    return volume

def setVolume(host, volume):
    port = 7676
    post = '/smp_16_'
    SOAP = """<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:ns0="urn:schemas-upnp-org:service:RenderingControl:1" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ns0:SetVolume><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredVolume>%s</DesiredVolume></ns0:SetVolume></s:Body></s:Envelope>"""
    SoapMessage = SOAP%(volume)
    connection = httplib.HTTP(host, port)
    connection.putrequest('POST', post)
    connection.putheader('Host', host)
    connection.putheader('User-Agent', 'Twisted PageGetter')
    connection.putheader('Content-Length', len(SoapMessage))
    connection.putheader('SOAPACTION', '"urn:schemas-upnp-org:service:RenderingControl:1#SetVolume"')
    connection.putheader('content-type', 'text/xml ;charset="utf-8"')
    connection.putheader('connection', 'close')
    connection.endheaders()
    connection.send(SoapMessage)
    statuscode, statusmessage, header = connection.getreply()
    response = connection.getfile().read()

if __name__==   '__main__':
    host = '192.168.254.4'
    try:
        volume = sanitizeVolume(sys.argv[1])
    except IndexError:
        print 'You need to supply at least one numeric argument'
        sys.exit(0)
    if isinstance(volume, bool):
        print 'First argument should be an integer between 0 and 99'
        sys.exit(0)
    else:
        setVolume(host, volume)
