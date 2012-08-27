"""
Created August 23, 2012

@author: Justin Hammond, Rackspace Hosting
"""
import aic
nvp = aic.nvp.Connection('https://nvp')


def testCreateSwitch():
    switch = nvp.lswitch().create()
    print switch
    nvp.lswitch(switch).delete()


def testCreateSwitchPort():
    switch = nvp.lswitch().create()
    print switch
    lport = nvp.lswitch_port(switch).create()
    print lport
    nvp.lswitch_port(switch, lport).delete()
    nvp.lswitch(switch).delete()
