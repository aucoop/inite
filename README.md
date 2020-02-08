# INITE: Captive portal basat en DNS spoofing.
Aquesta és la documentació bàsica d'Inite. Inite incorpora un servidor DNS fet en python i un [Captive Portal](https://en.wikipedia.org/wiki/Captive_portal) fet en el _REST framework_ de python Django:

- **CustomDNS:** Aquest senzill dns (a la carpeta customDNS) permet l'aparició automàtica del _captive portal_ i l'enllaç amb els altres serveis del servidor. El seu funcionament és el següent:
  1. Un _host_ de la xarxa interna desitja connectar-se a internet. Si el router ha estat ben configurat com explica la [documentació](#configuracio-del-router) aquest _host_ farà una petició DNS al servei per resoldre el nom del recurs que demana.
  2. Al rebre aquesta petició el servidor customDNS té dos comportaments:
    - Aquest host no ha passat pel _captive portal_: En aquest cas mostrarà el portal perquè el host es pugui registar.
    - Aquest host s'ha registrat correctament al _captive portal_: En aquest cas podrà accedir als recurosos d'internet i/o del servidor lliurement. La base de dades del DNS serà borrada cada ( **encara no ho sabem** ) hores per forçar el registre de la gent tenint en compte que els cursos pels que s'ha dissenyat aquest servei duren 4 hores i els ordinadors són compartits.

- **Captive Portal:** La funció principal és recollir les dades de les persones que es dirigeixin al centre a fer els cursos. Aquest portal es veurà cada cop que un nou _host_ entri a la xarxa en les X (**aqui cal posar el nombre d'hores**) hores entre que la base de dades es _reseteja_. Permet també a un administrador amb usuari i contrasenya poder-se descarregar aquestes dades i bloquejar o permetre la sortida a internet.

## Configuració de la instal·lació

Abans de tot cal donar el valor correcte a les variables d'instal·lació:
ROUTER_PASSWD: Password del router
ROUTER_USER: User del router
ROUTER_IP: IP del router
IP_SERVIDOR: IP del servidor web (192.168.33.2) en la nostra configuració
IP_DNS: IP del servidor DNS pel _forwarding_
DOMAINS: Domini base. (ex: _duniakato.org_)
DB_NAME: Nom de la base de dades, a escollir.
DB_USER: Usuari de la base de dades, a escollir.
DB_PASSWD: Contrasenya de la base de dades, a escollir.
(**Aquí en falten encara**)

Cal també donar permisos d'exexcució a l'script d'instal·lació
```bash
chmod +x installinite.sh
```


## Configuració del Router

(falta aqui la docu de la configuració del router, el de diadem ja està configurat)

## Instal·lació

Guia d'instal·lació ràpida del servei Inite en un servidor Devian/Ubuntu i derivats. La instal·lació pot fer-se de forma automàtica per mitjà del _script_ d'instal·lació _installinite.sh_ o de forma manual amb els passos següents ( **Això encara no està implementat. Cal instal·lar manualment** ). Si s'opta per la instal·lació automàtica el manual segueix al punt [posada en marxa](#posada-en-marxa).

Abans de començar la instal·lació cal moure el fitxer de configuracions al lloc que el pertoca

```bash
mkdir /etc/inite
cp variables.json /etc/inite/
```

### Instal·lació del programari necessari

1. Cal primer instalar python i l'instal·lador de paquets _pip_, el servidor web Apache2, el SGBD postgresql

```bash
sudo apt update -y
sudo apt install python python-pip python3 python3-dev python-dev python3-pip apache2 postgresql postgresql-contrib libpq-dev apache2-utils libapache2-mod-wsgi-py3 expect -y 
```

2. Configuració de Postgres. És important escriure aquestes comandes per separat per evitar problemes amb el _shell_ de postgres. **CAL DONAR AL NOM DE L'USUARI, AL NOM DE LA BASE DE DADES I A LA CONTRASENYA EL MATEIX VALOR QUE S'HA INDICAT EN EL FITXER DE CONFIGURACIÓ _variables.json_** 

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
su postgres
psql
create user <valor del fitxer variables.json>;
create database <valor del fitxer variables.json>;
\password <valor del fitxer variables.json>;  
alter user u_dks createdb;
\q
exit
```


3. Configuració de l'entorn python
  1. Crear entorn virtual
  ```bash
  pip3 install venv
  python3 -m venv venv
  source venv/bin/activate
  ```
  2. Instal·lacció dels requisits de python
```bash
pip3 install wheel
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
deactivate
```
4. Deshabilitar el dns server per defecte d'unix
```bash
systemctl disable systemd-resolved
```
5. Configuració de l'apache. 
  1. Configuració de les variables d'entorn
    Cal donar valor a la variable PROJ_PATH present a _web_server/envvars_. Exemple:
    ```bash
    #Això és el fitxer envvars
    export PROJ_PATH=/home/quim/inite
    ```
    Afegir la variable a l'entorn d'Apache:
    ```bash
    su -c "cat web_server/envvars  >> /etc/apache2/envvars"
    ```
  2. Configuració dels mòduls i entorn
  ```bash
  sudo cp web_server/inite.conf /etc/apache2/sites-available/ 
  sudo ln -s /etc/apache2/sites-available/inite.conf /etc/apache2/sites-enabled/inite.conf 
  sudo cp web_server/mod-wsgi.conf /etc/apache2/conf-available/
  sudo a2enconf mod-wsgi
  sudo a2enmod wsgi
  sudo systemctl enable apache2
  sudo systemctl restart apache2
  chmod +x enable updateIP
  sudo chown root:root updateIP
  echo "www-data ALL= (root) NOPASSWD: `pwd`/updateIP" | sudo EDITOR='tee -a' visudo
  ``` 
### Instal.lació del dns customDNS
1. Procedim a la instal·lació de customDNS

```bash
pip install -r customDNS/requirements.txt
```
2. Copiar la carpeta la carpeta de sistema /usr/local/.

```bash
sudo cp -r ./customDNS /usr/local/
```

3. Copiar el servei a la carpeta de serveis de Debian

```bash
 sudo cp ./customDNS/fakeDNS.service /etc/systemd/system/fakeDNS.service
 ```

## Posada en marxa

Instruccions de posada en marxa dels serveis:
- **Mode debugging:** Permet engegar els serveis en terminals i veure els outputs de _debugging_ per a detectar errors en la configuració/programació
- **Mode producció:** Fet amb daemons de systemd per garantir l'execució en segon plà, l'engegada del servei amb l'engegada de l'ordinador i el restabliment del servei si cau. 

### Posada en marxa com a procés des del terminal. Versió de _debugging_
1. Assegurarnos que tenim tots els daemons al port 80 i al port 53 desctivats
```bash
netstat -putan #per veure les connexions
systemctl stop apache2 #apagar la connexió d'apache que podem tenir encesa
systemctl stop fakeDNS #apagar el dns que podem tenir encès
systemctl stop systemd-resolved #apagar el dns resolver d'ubuntu
```

2. Assegurar-nos que la base de dades està activada
```bash
systemctl start postgresql
```
3. Assegurar-nos que la variable IP_SERVIDOR del fitxer customDNS/fakeDNS.py té el valor del dispositiu que esta exercit de servidor DJango. 

4. Engegar el dns en un terminal
```bash
python2 customDNS/fakeDNS.py
```
5. Engegar el server DJango
```bash
source venv/bin/activate
sudo su
python3 manage.py runserver 0.0.0.0:80
deactivate
```
  Si es el primer cop que accedim (és a dir, la base de dades està buida) caldrà entrar creant un usuari administrador per defecte amb la seguent comanda
  ```bash
  source venv/bin/activate
  python3 manage.py createsuperuser
  sudo su
  python3 manage.py runserver 0.0.0.0:80
  deactivate
  ```
  
Llest. Al obrir un navegador amb el DNS ben configurat i dirigit al nostre servidor ens sortirà un _popup_ del navegador per registrar-nos.

### Posada en marxa com a server (daemon). Versió de producció
1. Posada en marxa del daemon de customDNS.
```bash 
sudo systemctl enable fakeDNS
sudo systemctl start fakeDNS
```
2. Posada en marxa del daemon apache2
```bash
sudo systemctl start apache2
```

### IMPORTANT!! Observacions
Cal tenir en compte que l'única forma de creat nous usuaris és a través de la comanda _createsuperuser_ mostrada en el punt anterior. Cal preveure quants usuaris cal donar.  

## Manual d'ús d'Inite
Per poder seguir aquest punt cal haver completat [Instal·lació](#Instal·lacio) i [Posada en marxa](#posada-en-marxa).
1. A l'iniciar un navegador, ens sortirà un pop-up demanant-nos que ens registrem per usar la xarxa. 
(foto popup)
2. Al accedir-hi, s'ens mostrarà un formulari que haurem d'omplir per usar els recursos de la xarxa. Des d'aquest panell podrem anar també al taulell d'administració (punt 4).
(foto)
3. Des d'aquesta se'ns mostren els recursos als que podem accedir sense internet
(foto)
4. Si cliquem al botó d'_Admin_ accedirem al panell d'administració des del que ens haurem de _loggejar_.
(foto)
5. Des d'aquest panell d'administració tenim accés a diverses funcionalitats
  1. Descarregar les dades dels usuaris en format csv des de la data assenyalada
  2. Canviar la contrasenya i el nom d'usuari
  3. Permetre o bloquejar l'accés a internet dels ordinadors de la sala
  4. Sortir de l'usuari

## Manual per al desenvolupament.
### Com adaptar Inite a les meves necessitats
A la carpeta templates hi ha els templates html amb els textos que es poden canviar per adaptar-los a les necessitats d'allà on implementem el projecte
(en un futur aquesta docu estarà millor). 
## Manual per al desenvolupament.
### Com adaptar Inite a les meves necessitats (desactualitzat)

### Descripció dels directoris i fitxers d'Inite

