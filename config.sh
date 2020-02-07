#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ ! -f "./variables.json" ];then
echo "ERROR: You must be in Inite repository's root folder?"
exit 1
fi


### CONFIGURACIÓ DEL ROUTER ###
# Falta aquí la configuració del router


### INSTALLACIO
## installacio del programari necssari
apt update
sudo apt install python python-pip python3 python3-dev python-dev python3-pip apache2 postgresql postgresql-contrib libpq-dev apache2-utils libapache2-mod-wsgi-py3 expect -y

## Entorn de python
pip3 install venv
python3 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
deactivate

##Configuracióp de postgres
systemctl enable postgresql
systemctl start postgresql
##ENS HEM QUEDAT AQUI

## Apache variables d'entorn
echo "export PROJ_PATH=`pwd`" >> /etc/apache2/envvars

## Configuracio dels moduls i entorn
cp web_server/inite.conf /etc/apache2/sites-available/
ln -s /etc/apache2/sites-available/inite.conf /etc/apache2/sites-enabled/inite.conf
cp web_server/mod-wsgi.conf /etc/apache2/conf-available/
a2enconf mod-wsgi
a2enmod wsgi
systemctl enable apache2
systemctl restart apache2





