#!/usr/bin/python2

import socket
import time
from functions import Registre_IPs
from dnsQuery import DNSQuery
import signal
import os, sys
import logging, argparse
import json

with open('/etc/inite/variables.json','r') as f:
  variables = json.load(f)

IP_SERVIDOR=variables['IP_SERVIDOR']
IP_DNS=variables['IP_DNS']
DOMAINS =variables['DOMAINS']

#db = Registre_IPs('u_dks', 'NTExMmZhMmU3', 'localhost', '5432', 'db_dks', 'portal_registre')
#p = None

def capture(req, domains, addr, loggedAddrs):
  return (addr[0] not in loggedAddrs) or (req in domains)


def handler(nombre, frame):
  db.actualitza()
  logging.debug("[*]\tIp list updated:\n"+", ".join(db.getIPs()))  
  

if __name__ == '__main__':


  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--debug', default=False, action='store_true'  )
  

  args = parser.parse_args()
  loglevel = 'debug' if  vars(args)['debug']  else 'warning'

  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
  logging.basicConfig(level=numeric_level, format='%(message)s')
  
  global p
  global db
  try: 
    logging.debug('[*]\tConnecting with DB...')
    db = Registre_IPs(variables['DB_USER'], variables['DB_PASSWORD'], 'localhost', '5432', variables['DB_NAME'], 'portal_registre') 
  except Exception as e:
    logging.debug('Error connecting with db: '+str(e))
    sys.exit()
  with open("/run/fakeDNS.pid","w") as pid_file:
    pid_file.write(str(os.getpid()))
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  #udps.settimeout(5)
  try:
    udps.bind(('',53))
    logging.debug('[*]\tDns listening on port 53')
  except Exception as e:
    logging.debug('Error while port binding: '+str(e))
    sys.exit()
  signal.signal(signal.SIGUSR1, handler)
  logging.debug('[*]\tCapturing SIGUSR1...\n')


  try:
    while 1:
      try:
              data, addr = udps.recvfrom(1024)
              p=DNSQuery(data, IP_DNS ,IP_SERVIDOR)
              logging.debug('[***] Dns request from {}:\t{}'.format(addr[0],p.dominio))
              tocapture = capture(p.dominio, DOMAINS, addr, db.getIPs())
              response = p.respuesta(tocapture)
              if  vars(args)['debug']:
                chars = response[-4:]
                resolved = str(ord(chars[0])) + '.'
                resolved += str(ord(chars[1])) + '.'
                resolved += str(ord(chars[2])) + '.'
                resolved += str(ord(chars[3]))
                logging.debug('\t[*] Dns respone: {}\n'.format(resolved))
              udps.sendto(response, addr)
      except Exception as e:
                            logging.debug("Hi ha hagut un error %s" % e)
                            pass
      #print("surto del socket 1")
# #print 'Respuesta: %s -> %s' % (p.dominio, ip)
  except KeyboardInterrupt:
    #print ('Finalizando')
    udps.close()
