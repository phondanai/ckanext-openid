from ckan.common import session
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model
import pylons
import pylons.config as config
from ckan.lib import base
from ckan.model import User
import ckan.lib.helpers as h
from ckan.lib.base import BaseController
from ckan.common import json, response, request
import logging
log = logging.getLogger(__name__)
from pylons.controllers.util import redirect_to, redirect
from authomatic.providers import oauth2, oauth1, openid
from authomatic import Authomatic
from authomatic.adapters import WebObAdapter
import uuid
import urlparse


CONFIG = {
    'oi': {
        'class_': openid.OpenID,
    }
}

redirect = h.redirect_to

def get_username(openid):
    return urlparse.urlparse(openid).path.split('/')[-1].strip().lower()

def get_user(openid):
        username = get_username(openid)
	user = User.by_name(username)
	if user:
		user_dict = toolkit.get_action('user_show')(data_dict={'id': user.id})
		return user_dict
	else:
		return None

def unique_string():
    return str(uuid.uuid4())

authomatic = Authomatic(config=CONFIG, secret=unique_string())

class OpenIDController(BaseController):
	def verify(self):
		result = authomatic.login(WebObAdapter(request, response), "oi")
		if result:
			if result.error:
				redirect("/user/logged_in")
			if not (result.user.name and result.user.id):
				result.user.update()
			user = get_user(result.user.id)
			if not user:
				 user = toolkit.get_action('user_create')(
                    context={'ignore_auth': True},
                    data_dict={'email': result.user.email,
                               'name': get_username(result.user.id),
                               'password': unique_string()})
			session['openid-user'] = user['name']
			session.save()
			redirect("/")


class OpenidPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    def configure(self, config):
         required_keys = ('ckan.openid.default_provider',)

         for key in required_keys:
             if config.get(key) is None:
                 raise RunTimeError('Required configuration option {0} not found.'.format(key))

    @staticmethod
    def before_map(m):
    	 m.connect('/user/oilogin',
            controller='ckanext.openid.plugin:OpenIDController',
            action='verify')
    	 return m


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'openid')

    # IAuthenticator
    def identify(self):
        user = session.get('openid-user')
    	if user:
    		toolkit.c.user = user

    def distory_session(self):
        if 'openid-user' in session:
            del session['openid-user']
        session.save()

    def logout(self):
        self.distory_session()

    def abort(self, status_code, detail, headers, comment):
        self.distory_session()
