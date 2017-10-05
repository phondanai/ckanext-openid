# CKAN openid extension 

This extension adds suuport of OpenID authentification to your ckan platform (link: http://openid.net/what-is-openid/).

## Prerequisites

* Install lastest version of CKAN 
* Install automatic 

Activate python virtual environment and install automatic library
```sh
pip install authomatic python-openid
```

## Build instructions 

* Activate python virtual env 

```sh
. /usr/lib/ckan/default/bin/activate
```

* Clone git repository

```sh
git clone https://github.com/routetopa/ckanext-openid.git
cd ckanext-openid
```

* Build the plugin

```sh
python setup.py develop
```

* Add 'openid' plugin to CKAN config file :
```sh
ckan.plugins = stats text_view recline_view openid
```

* Start ckan
```sh
paster serve /etc/ckan/default/development.ini
```


Dvelopment of TET extenstions is supported by European Commision through the [ROUTE-TO-PA project](http://routetopa.eu/)
