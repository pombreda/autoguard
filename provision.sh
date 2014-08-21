#!/bin/bash
USER=autoguard
RUN_DEPS="
    libpq5
    python
    python-virtualenv
"

BUILD_DEPS="
    build-essential
    adduser
    libpq-dev
    python2.7-dev
    sudo
"

set -xe
export DEBIAN_FRONTEND=noninteractive

echo 'deb http://ftp.fr.debian.org/debian wheezy-backports main' > /etc/apt/sources.list.d/backports.list
apt-get update
apt-get install --no-install-recommends -y $RUN_DEPS $BUILD_DEPS

adduser --home /home/$USER --ingroup www-data --disabled-password --disabled-login --gecos ",,," $USER

mkdir /app
chown $USER:www-data /app

sudo -H -u $USER /bin/bash <<EOF
set -ex

cp -r /build/* /app
virtualenv /app/venv
/app/venv/bin/pip install -e /app/
EOF

SUDO_FORCE_REMOVE=yes apt-get purge -y $BUILD_DEPS
apt-get --purge autoremove -y
apt-get clean

