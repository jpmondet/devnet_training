#! /usr/bin/env python

"""
    Some practicing on the APIC Rest API
"""

from __future__ import print_function, unicode_literals
import requests
import json
from cisco_sandboxes import apicdc
import cobra.mit.session
import cobra.mit.access
import cobra.mit.request
import cobra.model.pol
import cobra.model.fv

if __name__ == '__main__':
    """
     Main function
    """

    requests.packages.urllib3.disable_warnings() #pylint: disable=no-member
    url = apicdc['address']
    passwd = apicdc['password']
    user = apicdc['username']
    
    auth = cobra.mit.session.LoginSession(url, user, passwd)
    session = cobra.mit.access.MoDirectory(auth)
    session.login()

    tenant_query = cobra.mit.request.DnQuery("uni/tn-TenantName")
    tenant = session.query(tenant_query)

    uni = cobra.model.pol.Uni('')
    new_tenant = cobra.model.fv.Tenant(uni, "NewTenant")
    new_app = cobra.model.fv.Ap(new_tenant, "NewApp")
    new_epg = cobra.model.fv.AEPg(new_app, "NewEPG")

    config_request = cobra.mit.request.ConfigRequest()
    config_request.addMo(new_epg)
    session.commit(config_request)

