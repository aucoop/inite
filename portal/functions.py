import requests
import os
from inite.settings import ROUTER_USER, ROUTER_PASSWD

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
  payload="/usr/bin/expect << EOF\n"
  payload+="spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no "+usr+"@192.168.33.1 \n"
  payload+='expect "password"\n'
  payload+='send "'+passwd+'\\n"\n'
  payload+='expect "#"\n'
  payload+='send "configure\\n"\n'
  payload+='expect "#"\n'
  payload+='send "if show firewall name INT | grep \'rule 10\' ; then delete firewall name INT rule 10 ; else set firewall name INT rule 10 action drop; set firewall name INT rule 10 protocol tcp_udp ; set firewall name INT rule 10 destination port 80,8080,8000,443 ; fi\\n"\n'
  payload+='expect "#"\n'
  payload+='send "commit\\n"\n'
  payload+='expect "#"\n'
  payload+='send "save\\n"\n'
  payload+='expect "#" \n'
  payload+='send "exit\\n"\n'
  payload+='expect "#" \n'
  payload+='EOF\n'

  os.system(payload)
