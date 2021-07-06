import requests
import os
from inite.settings import ROUTER_USER, ROUTER_PASSWD, ROUTER_IP

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def toogle_router():
  passwd=ROUTER_PASSWD
  usr=ROUTER_USER
  ip=ROUTER_IP
  payload="/usr/bin/expect << EOF\n"
  payload+="spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no "+usr+"@"+ip+" \n"
  payload+='expect "password"\n'
  payload+='send "'+passwd+'\\n"\n'
  payload+='expect "#"\n'
  payload+='send "configure\\n"\n'
  payload+='expect "#"\n'
  payload+='send "if show firewall | grep \'name INT\'; then  delete interfaces ethernet eth0 firewall out; commit; delete firewall name INT ; else  set firewall name INT description \'Toogle internet\'; set firewall name INT default-action accept; set firewall name INT rule 20 action accept; set firewall name INT rule 10 action drop; set firewall name INT rule 10 protocol tcp_udp ; set firewall name INT rule 10 destination port 80,8080,8000,443 ; set interfaces ethernet eth0 firewall out name INT; fi\\n"\n'
  payload+='expect "#"\n'
  payload+='send "commit\\n"\n'
  payload+='expect "#"\n'
  payload+='send "save\\n"\n'
  payload+='expect "#" \n'
  payload+='send "exit\\n"\n'
  payload+='expect "#" \n'
  payload+='EOF\n'

  os.system(payload)
