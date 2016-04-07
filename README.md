# CKAN openid extension 

Adds openid authentication support to ckan 

## Prerequisites

* Install lastest version of CKAN 
* Install automatic 

activate python virtual environment and install automatic library
```sh
pip install authomatic
```

## Build instructions 

activate python virtual env 

```sh
. /usr/lib/ckan/default/bin/activate
```

clone git repository

```sh
git clone https://gitlab.insight-centre.org/egov/ckanext-openid.git
cd ckanext-openid
```

build the plugin

```sh
python setup.py develop
```

Add 'openid' plugin to CKAN config file :
```sh
ckan.plugins = stats text_view recline_view openid
```

start ckan
```sh
paster serve /etc/ckan/default/development.ini
```


Dvelopment of TET extenstions is supported by European Commision through the [ROUTE-TO-PA project](http://routetopa.eu/)