'''
Created on August 17, 2012

@author: Justin Hammond, Rackspace Hosting
'''

import json
from aic.aiclibconnection import AICLibConnection

class AICLib(object):


    def __init__(self, username, password):
        self.connections = list() 
        self.username = username
        self.password = password


    def createConnection(self, resourceURI, username, password):
        self.connections.append(AICLibConnection(resourceURI,
                                                 username,
                                                 password))


    def logout(self):
        for connection in self.connections:
            print connection


