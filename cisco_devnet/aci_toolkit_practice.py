#! /usr/bin/env python3

"""
    Just a lil bit of practicing of aci toolkit
    for the NPDEV exam
"""

from __future__ import print_function, unicode_literals
from acitoolkit.acitoolkit import *
from cisco_sandboxes import apicdc




if __name__ == '__main__':
    """
    Contacting the device to 
    open a session and then calling
    functions with this session.
    """

    session = Session(apicdc['address'], apicdc['username'], apicdc['password'])
  
    session.login()
  
    for tenant in Tenant.get(session):
        if "Heroes" in tenant.name: 
            print('Tenant:', tenant.name)
            app_list = AppProfile.get(session, tenant)
            for app in app_list:
                print('  App: ', app.name)
                for epg in EPG.get(session, app, tenant):
                    print('    EPG: ', epg.name)

        
