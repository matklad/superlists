Provisioning a new site
=======================

## Required packages

* nginx
* Python3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host configuration

* see nginx.template.conf
* replace SITENAME

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME

## Folder structure
Assume we have a user account at /home/matklad

/home/matklad/
+--sites
   +--SITENAME
      +--database
      |--source
      |--static
      +--virtualenv
