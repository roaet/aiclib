'''
Created on August 22, 2012

@author: Justin Hammond, Rackspace Hosting
'''

import json
import logging

from aic.aiccore import AICQuery
import aic.common as common

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class NVPBaseQuery(AICQuery):


    def __init__(self, aic_connection):
        super(NVPBaseQuery, self).__init__(aic_connection)


    def fields(self, fieldlist):
        return self


