import socket, struct, sys
from httplib import HTTPResponse
from StringIO import StringIO


class Response(HTTPResponse):
    def __init__(self, response_text):
        self.fp = StringIO(response_text)
        self.debuglevel = 0
        self.strict = 0
        self.msg = None
        self._method = None
        self.begin()

def queryUpnp(ip):
    msg = ('M-SEARCH * HTTP/1.1\r\n' +
    'ST: ssdp:all\r\n' +
    'MX: 2\r\n' +
    'MAN: "ssdp:discover"\r\n' +
    'HOST: 239.255.255.250:1900\r\n\r\n')
    services = []
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    sock.settimeout(2)
    sock.bind((ip, 1900))
    for time in xrange(2):
        sock.sendto(msg, ('239.255.255.250', 1900))
    try:
        while sock:
            data, addr = sock.recvfrom(1024)
            services.append(data)
            if not data:
                break
    except socket.timeout:
        pass
    finally:
        for service in services:
            response = Response(service)
            print 'Service Location :', response.getheader('Location')
            print 'Server :', response.getheader('Server')
            print 'ST :', response.getheader('ST')
            print ''
    return

if __name__ == '__main__':
    from network import Network
    network = Network()
    queryUpnp(network.ipAddress)
    
