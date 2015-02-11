##################################
#
#      Auth is a former function that i used to check on the LDAP server the authentification
#
##################################


def check_user_pwd (req,server=None,dn=None,pwd=None,getinfo=False):
    """
    \brief Check user password by trying to bind to the ldap server,
    after T L Wolfe code (California Institute of Technology)
    \param[in] req http request object
    \param[in] server LDAP server name or IP address
    \param[in] dn user's DN
    \param[in] pwd user's password
    \return -1 if an error occured
    \n      0 if the password does not match or the user's dn does not exist
    \n      1 if user was authenticated
    \n Called by: check_login
    \author S. Essid
    \version 1
    \date 18/11/2007
    
    \n Updates
    \author Slim Essid
    \Date 22/10/2008
    Made sure the function always returns three args: status, error message, ldap_info
    """
    import ldap, sys

    info={}

    if (server == None) or (dn == None) or (pwd == None):
        return -1,"Bad parameter",""

    #try:
    #    1
    #    #ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)
    #    #ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,'/..../cacert.pem')
    #except ldap.LDAPError, e:
    #    return -1,e

    # Creating LDAP object
    try:
       l = ldap.initialize("ldap://" + server)  # NO TRACE
       l.protocol_version = ldap.VERSION3
       l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
    except ldap.LDAPError, e:
        return -1,e,""

    # Starting TLS connection
    try:
        l.start_tls_s()
    except ldap.LDAPError, e:
        return -1,e,""

    # Binding to server as user
    try:
        l.simple_bind_s(dn,pwd)
        usrinfo=l.search_s(dn,ldap.SCOPE_SUBTREE, "objectclass=*")[0][1]

	if getinfo:
            if usrinfo.has_key('sn') : info['name']=usrinfo['sn'][0]
            if usrinfo.has_key('givenName') : info['first_name']=usrinfo['givenName'][0]
            if usrinfo.has_key('employeeType') : info['status']=usrinfo['employeeType'][0]
            if usrinfo.has_key('mail') : info['mail']=usrinfo['mail'][0]
            if usrinfo.has_key('departmentNumber') : info['dpt']=usrinfo['departmentNumber'][0]

    except ldap.NO_SUCH_OBJECT, e:
        l.unbind_s()
        return 0,e,""
    except ldap.INVALID_CREDENTIALS, e:
        l.unbind_s()
        return 0,e,""
    except ldap.LDAPError, e:
        l.unbind_s()
        return -1,e,""

    # Un-binding from server
    l.unbind_s()	
    return 1,"",info

