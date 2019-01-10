#!/bin/bash
#sudo apt-get install -y python-dev python-pip apache2 apache2-dev
sudo apt-get install -y apache2 libapache2-mod-wsgi libapache2-mod-php5 php5-curl

sudo cp /vagrant/provisioners/wsgi.conf /etc/apache2/conf-enabled/
sudo /etc/init.d/apache2 restart
#echo | openssl s_client -showcerts -servername pypi.python.org -connect pypi.python.org:443 2>/dev/null > /home/vagrant/pypi.pem

#sudo pip install --cert /home/vagrant/pypi.pem mod_wsgi

