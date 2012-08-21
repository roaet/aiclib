'''
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
'''

import json
import logging
import time

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


    def __init__(self, resourceURI, username  = 'admin', password = 'admin'):
        logger.info("Creating AICLibConnection")
        self.resourceURI = resourceURI
        self._conn = None
        self.username = username
        self.password = password
        self.maxRetries = 5
        self._headers = {} 
        self.generationNumber = 0
        self.authkey = ''


    @property
    def connection(self):
        if not self._conn:
            self._conn = urllib3.connection_from_url(self.resourceURI)
            if not self._login(self.username, self.password):
                self._conn = None
                logger.error("Authorization failed.")
                raise IOError('401','Unauthorized')
        return self._conn


    def _login(self, username, password):
        fields = { 'username' : username, 'password' : password }
        r = self._conn.request_encode_body('POST',common.apimap('login'),
                                           fields = fields,
                                           encode_multipart= False)
        if self._iserror(r):
            logger.error("Need to handle error")
            return False
        else:
            self.authkey = r.headers['set-cookie']
            logger.info("Authorized (%s)" % (self.authkey))
        return True

    
    @property
    def headers(self):
        self._headers = {
            'Cookie' : self.authkey,
            'X-Nvp-Wait-For-Config-Generation': self.generationNumber,
        }
        return self._headers
        

    def _request(self, method, apiCall, generationNumber = 0):
        retryPause = 0
        r = None
        for retryCount in XRange(self.maxRetries):
            self.generationNumber = generationNumber
            r = self.connection.request(method,
                                        apiCall,
                                        headers = self.headers)
            if self._iserror(r):
                try:
                    self._handle_error(r)
                    r = None
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
        if resp.status != 200:
            return True
        return False


    def _handle_error(self, resp):
        comment = "%s: %s" % (resp.reason, resp.data)
        if resp.status == 400:
            logger.error("Bad request")
            raise TypeError('400',comment)
        elif resp.status == 401:
            logger.info("Authorization expired; renewing")
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

    
    def _generic_request(self, method, api, generationNumber = 0):
        r = self._request(method, api)

    '''
    Authentication Methods
    Login is performed by the class.
    '''
    def logout(self, generationNumber = 0):
        r = self._request('GET',common.apimap('logout'))
        logger.info(r.data)


    '''
    Documentation Methods
    '''
    def read_method(self, methodName):
        uri = "%s/%s" % (common.apimap('readMethod'), methodName)
        r = self._request('GET',uri)
        logger.info(r.data)


    def get_method_uris(self):
        uri = common.apimap('getMethodURIs')
        r = self._request('GET',uri)
        logger.info(r.data)

    
    def get_schemas(self, generationNumber = 0):
        r = self._request('GET',common.apimap('schema'))
        logger.info(r.data)


    def read_schema(self, schemaName):
        uri = "%s/%s" % (common.apimap('readMethod'), schemaName)
        r = self._request('GET',uri)
        logger.info(r.data)
    

    def get_manual(self):
        r = self._request('GET',common.apimap('manual'))
        logger.info(r.data)


    '''
    Network Control Cluster
    '''
    def get_control_cluster(self, generationNumber = 0):
        r = self._request('GET',common.apimap('controlCluster'),
                          generationNumber = generationNumber)
        logger.info(r.data)


    def create_control_cluster(self, generationNumber = 0):
        r = self._request('PUT',common.apimap('controlCluster'),
                          generationNumber = generationNumber)
        logger.info(r.data)


    '''
    Transport Zones
    '''
    def create_transport_zone(self,
