#!/usr/bin/python2
import socket
import time


class DNSQuery:
  def __init__(self, data, dns, ip):
    self.data=data
    self.dominio=''
    self.resolvedIp = ip
    self.dnsForwarding = dns

    tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.dominio+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])





  def respuesta(self, capture ):
    packet=''

    #print(self.dominio)
    if self.dominio:
 
      if not capture:
        rdns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rdns.settimeout(5)
        rdns.connect((self.dnsForwarding,53))
        con = 0
        rdns.send(self.data)
        response = ""
        while(con != 3):
          try:
            #print("entro al socket a google")
            response = rdns.recv(1024)
            break
            #print("surto del socket google")
          except:
            con += 1
            #print("timer")
        return response
        
      packet+=self.data[:2] + "\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
      packet+=self.data[12:]                                         # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), self.resolvedIp.split('.'))) # 4bytes of IP
    return packet

