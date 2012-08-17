'''
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
'''

import json
import urllib3

class AICLibConnection(object):
    apimap = {
        'login': '/ws.v1/login',
        'logout': '/ws.v1/logout'
    }


    def __init__(self, resourceURI, username  = 'admin', password = 'admin'):
        self.resourceURI = resourceURI
        self._conn = None
        self.username = username
        self.password = password
        self.authcookie = None


    @property
    def connection(self):
        if(not self._conn):
            self._conn = urllib3.connection_from_url(self.resourceURI)
        self._login(self.username, self.password)
        return self._conn


    def _login(self, username, password):
        fields = { 'username' : username, 'password' : password }
        r = self._conn.request_encode_body('POST',self.apimap['login'],
                                                fields = fields,
                                                encode_multipart= False)
        print r.headers

    def logout(self):
        r = self.connection.request('GET',self.apimap['logout'])
        print r.headers


