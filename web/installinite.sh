#!/bin/bash


SetDockerRepository() {
         sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
         apt-transport-https \
         ca-certificates \
         curl \
         gnupg-agent \
         software-properties-common

        echo -n "Installing GPG key...  " ; 
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

        echo "Verifying that the key with the fingerprint is correctly installed...";

        if (( ! $(sudo apt-key fingerprint 0EBFCD88 2>/dev/null | wc -c) )); then
                echo ""; echo "[-]      Error: Fingerprint not found!"; echo "";
                return 2;
        else 
                echo ""; echo "[+]      Fingerprint found!"; echo "";
        fi
        
      add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
            stable" 

        return 0;
}

if [ "$EUID" -ne 0 ]
  then echo "ERROR: Please run as root, use sudo ./installinite.sh"
  exit
fi

if [[ ! -f "./variables.json" || ! -f "./docker-compose.yml" ]];then
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
    

# ## instalació de docker
# #docker
# a=$(which docker | grep usr)
# if [[ -z $a ]]; then
# echo "Installing docker"
#         apt-get remove docker docker-engine docker.io containerd runc
#         SetDockerRepository;
#         if (( $? )); then
#                 echo "Error installing the docker repositories, exiting...";
#         else
#                 sudo apt-get update -y;
#                 sudo apt-get DEBIAN_FRONTEND=noninteractive install -y docker-ce docker-ce-cli containerd.io
#                 sudo apt autoremove -y;
#         fi
# else
# echo "Docker already installed"
# fi
# 
# a=$(which docker-compose | grep usr)
# if [[ -z $a ]]; then
#         echo "Installing docker-compose"
#         sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#         sudo chmod +x /usr/local/bin/docker-compose
#         sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# 
# fi
# #end docker
# 
# #Setting de docker
# 
# #Estableix el dameon
# echo "Starting docker daemon..."
# sudo service docker start
# sleep 5
# echo "Docker daemon started"
# #sudo docker-compose up

# cd src/

##iniciem docker en mode producció
#sudo docker-compose pull
#sudo docker swarm init
#sudo docker stack deploy -c ./docker-compose.yml cccd

##iniciem docker en mode debug

# sudo docker-compose pull
# sudo docker-compose -d


## Configuració de postgres
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

