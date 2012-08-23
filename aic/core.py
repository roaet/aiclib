"""
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
"""

import json
import logging
import time
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import urllib3
from urllib3.exceptions import MaxRetryError

import common


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class CoreLib(object):

    def __init__(self, uri, poolmanager=None, username='admin', 
                 password='admin'):
        '''
        Constructor for the AICLib object.
        - If pool_manager is 
        '''
        if poolmanager is None:
            self.conn = urllib3.connection_from_url(uri)
        else:
            self.conn = poolmanager.connection_from_url(uri)
        self.connection = _Connection(connection=self.conn,
                                      username=username,
                                      password=password)

    def _action(self, entity, method, resource):
        if not entity:
            return
        logger.info("(%s @ %s): %s" % (method, resource, 
                                       entity._unroll()))
        r = self.connection.request(method, resource,
                                          body = entity._unroll())
        logger.info("Response headers: %s" % r.headers)
        responselength = 0
        if 'content-length' in r.headers:
            responselength = int(r.getheader('content-length'))
        if responselength > 0:
            if r.getheader('content-type') == 'application/json':
                jsonreturn = json.loads(r.data)
                return jsonreturn
            else:
                return r.data
        return None


class Entity(object):

    def __init__(self, connection):
        self.connection = connection
        self.info = {}

    def _action(self, method, resource):
        return self.connection._action(self, method, resource)

    def _unroll(self):
        return self.info


class Query(object):

    def __init__(self, connection, resource):
        self.connection = connection
        self.query = {}
        self.resource = resource

    def _query(self, method):
        return self.connection._action(self, method, self.resource)

    def _unroll(self):
        return self.query


class _Connection(object):
    _encode_url_methods = set(['DELETE', 'GET', 'HEAD', 'OPTIONS'])
    _encode_body_methods = set(['PATCH', 'POST', 'PUT', 'TRACE'])

    def __init__(self, username='admin', password='admin',
                 connection=None):
        logger.info("Creating AICLibConnection")
        self._conn = connection
        self.authenticated = False
        self.username = username
        self.password = password
        self.maxRetries = 5
        self._headers = {} 
        self.generationnumber = 0
        self.authkey = ''

    @property
    def connection(self):
        if(not self.authenticated and 
           not self._login(self.username, self.password)):
                logger.error("Authorization failed.")
                raise IOError('401','Unauthorized')
        return self._conn

    def _login(self, username, password):
        fields = { 'username' : username, 'password' : password }
        r = self._conn.request_encode_body('POST',common.apimap('login'),
                                           fields=fields,
                                           encode_multipart=False)
        if self._iserror(r):
            logger.error("Need to handle error")
            return False
        else:
            self.authkey = r.headers['set-cookie']
            logger.info("Authorized (%s)" % (self.authkey))
        self.authenticated = True
        return True
    
    @property
    def headers(self):
        self._headers = {
            'Cookie' : self.authkey,
            'Content-Type' : 'application/json',
            'X-Nvp-Wait-For-Config-Generation': self.generationnumber,
        }
        return self._headers

    def request(self, method, apicall, generationnumber=0, body=None):
        retryPause = 0
        r = None
        for retryCount in xrange(self.maxRetries):
            self.generationnumber = generationnumber
            jsonBody = json.dumps(body)
            if method in self._encode_url_methods:
                r = self.connection.request_encode_url(method, apicall,
                                                       fields=body,
                                                       headers=self.headers)
            else:
                r = self.connection.urlopen(method, apicall,
                                            jsonBody,
                                            headers=self.headers)
                                            
            if self._iserror(r):
                try:
                    self._handle_error(r)
                    continue
                except EnvironmentError as e:
                    logger.info("Waiting for server: ",
                                r.headers['retry-after'])
                    retrypause = r.headers['retry-after']
                    time.sleep(retrypause)
                except:
                    logger.error("Unhandled error:")
                    raise
            self._handle_headers(r)
            return r
        raise MaxRetryError('408','Maxed retry attempts')

    def _handle_headers(self, resp):
        return

    def _iserror(self, resp):
        errorcheck = resp.status - 200
        if errorcheck >= 100:
            return True
        logger.info("Request success %s (%s)" % (resp.status, resp.reason))
        return False

    def _handle_error(self, resp):
        logger.info("Received error %s (%s)" % (resp.status, resp.reason))
        comment = "%s: %s" % (resp.reason, resp.data)
        if resp.status == 400:
            logger.error("Bad request")
            raise TypeError('400',comment)
        elif resp.status == 401:
            logger.info("Authorization expired; renewing")
            self.authenticated = False
            authstatus = self._login(self.username, self.password)
            if not authstatus:
                logger.error("Re-authorization failed.")
                raise IOError('401','Unauthorized')
        elif resp.status == 403:
            logger.error("Access forbidden")
            raise LookupError('403',comment)
        elif resp.status == 404:
            logger.error("Resource not found")
            raise LookupError('404',comment)
        elif resp.status == 409:
            logger.error("Conflicting configuration")
            raise LookupError('409',comment)
        elif resp.status == 500:
            logger.error("Internal server error")
            raise SystemError('500',comment)
        elif resp.status == 503:
            logger.error("Service unavailable")
            raise EnvironmentError('503',comment)

