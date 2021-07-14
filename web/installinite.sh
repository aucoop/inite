#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "ERROR: Please run as root, use sudo ./installinite.sh"
  exit
fi

if [[ ! -f "./variables.json" ]];then
echo "ERROR: You must be in Inite repository's root folder"
exit 1
fi

## configuració de variables
mkdir /etc/inite
cp variables.json /etc/inite/

### INSTALLACIO
## installacio del programari necssari
apt update
apt install -y 
sudo DEBIAN_FRONTEND=noninteractive apt install -yyy \
        apache2                  \
        apache2-dev              \
        apache2-utils            \
        expect                   \
        libapache2-mod-wsgi-py3  \
        libpq-dev                \
        postgresql               \
        postgresql-contrib       \
        python3                  \
        python3-dev              \
        python3-pip              \
        python3-venv             \
        python-dev               \
    

## Configuració de postgres
sudo systemctl start postgresql
nom_bd=`cat variables.json | grep DB_NAME | awk -F ":" '{print $2}' | sed -r 's/[",]//g'`
nom_user=`cat variables.json | grep DB_USER | awk -F ":" '{print $2}' | sed -r 's/[",]//g'`
passwd_bd=`cat variables.json | grep DB_PASSWORD | awk -F ":" '{print $2}' | sed -r 's/[",]//g'`
sudo su postgres -c "
psql -c \"create user $nom_user with password '${passwd_bd}';\"
psql -c \"create database $nom_bd;\"
psql -c \"alter user $nom_user createdb;\""


## Entorn de python
python3 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
deactivate


## Apache variables d'entorn
echo "export PROJ_PATH=`pwd`" >> /etc/apache2/envvars

## Configuracio dels moduls i entorn
rm /etc/apache2/sites-enabled/000-default.conf
cp web_server/inite.conf /etc/apache2/sites-available/
ln -s /etc/apache2/sites-available/inite.conf /etc/apache2/sites-enabled/inite.conf
cp web_server/mod-wsgi.conf /etc/apache2/conf-available/
a2enconf mod-wsgi
a2enmod wsgi
systemctl enable apache2
systemctl restart apache2
chmod +x updateIP
sudo chown root:root updateIP
echo "www-data ALL= (root) NOPASSWD: `pwd`/updateIP" | sudo EDITOR='tee -a' visudo
systemctl disable systemd-resolved

systemctl disable systemd-resolved
systemctl stop systemd-resolved
systemctl restart apache2

echo "Installation scritp is finish. Check services are running correctly with systemctl status fakeDNS and systemctl status apache2"

