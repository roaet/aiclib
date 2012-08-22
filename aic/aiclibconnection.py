'''
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
'''

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

class AICLibConnection(object):
    _encode_url_methods = set(['DELETE', 'GET', 'HEAD', 'OPTIONS'])

    _encode_body_methods = set(['PATCH', 'POST', 'PUT', 'TRACE'])
    

    def __init__(self, resourceURI, username='admin', password='admin',
                 connection=None):
        logger.info("Creating AICLibConnection")
        self.resourceURI = resourceURI
        self._conn = connection
        self.authenticated = False
        self.username = username
        self.password = password
        self.maxRetries = 5
        self._headers = {} 
        self.generationNumber = 0
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
            'X-Nvp-Wait-For-Config-Generation': self.generationNumber,
        }
        return self._headers
        

    def request(self, method, apiCall, generationNumber=0, body=None):
        retryPause = 0
        r = None
        for retryCount in xrange(self.maxRetries):
            self.generationNumber = generationNumber
            jsonBody = json.dumps(body)
            logger.info("REQ: %s" % jsonBody)
            if method in self._encode_url_methods:
                r = self.connection.request_encode_url(method, apiCall,
                                                       fields=None,
                                                       headers=self.headers)
            else:
                r = self.connection.urlopen(method, apiCall,
                                            jsonBody,
                                            headers=self.headers)
                                            
            if self._iserror(r):
                try:
                    self._handle_error(r)
                    continue
                except EnvironmentError as e:
                    logger.info("Waiting for server: ",
                                r.headers['retry-after'])
                    retryPause = r.headers['retry-after']
                    time.sleep(retryPause)
                except:
                    logger.error("Unhandled error:")
                    raise
            self._handle_headers(r)
            return r
        raise MaxRetryError('408','Maxed retry attempts')


    def _handle_headers(self, resp):
        logger.info("HEADERS: ", resp.headers)


    def _iserror(self, resp):
        errorCheck = resp.status - 200
        if errorCheck >= 100:
            return True
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
            authStatus = self._login(self.username, self.password)
            if not authStatus:
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

