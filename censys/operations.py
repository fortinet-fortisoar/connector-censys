from connectors.core.connector import get_logger, ConnectorError, _api_call

logger = get_logger('censys')

'''
    These lookup_x functions all look very similar to one another.
    They are kept separate so that the outputs can be cleaned up based on
    the different outputs from their api calls.

    See the commented lines in lookup_cert for an example of this
'''

error_msgs = {
    400: 'Bad/Invalid Request',
    401: 'Unauthorized: Invalid credentials provided failed to authorize',
    403: 'Access Denied',
    404: 'Not Found',
    500: 'Internal Server Error',
    503: 'Service Unavailable',
    'time_out': 'The request timed out while trying to connect to the remote server',
    'ssl_error': 'SSL certificate validation failed'
}


def lookup_domain(config, params):
    try:
        domain = params.get("domain")
        url = "{0}/api/v1/view/websites/{1}".format(config.get("url"), domain)
        request_status, request_result = _api_call(url, method='GET')
        return {"status_code": request_status, "response": request_result}
    except Exception as e:
        error_message = "Error looking up domain. Error message as follows:\n{}".format(str(e))
        logger.error(error_message)
        raise ConnectorError(error_message)


def lookup_cert(config, params):
    try:
        sha256_cert = params.get("sha256_cert")

        url = "{0}/api/v1/view/certificates/{1}".format(config.get("url"), sha256_cert)
        request_status, request_result = _api_call(url, method='GET')

        # The lines below can be used to return a more focused subset of the data in request_result

        # cert = request_result.get("parsed")
        # cert_validity = cert.get("validity")
        # cert_info = {"valid_from": cert_validity.get("start"),
        #             "valid_to": cert_validity.get("end")}
        # cert_info["self_signed"] = cert.get("self_signed")
        # cert_info["issuer_dn"] = cert.get("issuer").get("common_name")
        # cert_info["subject_dn"] = cert.get("subject").get("common_name")
        if request_status == 200:
            return {"status_code": request_status, "response": request_result}
        else:
            raise ConnectorError('{}'.format(error_msgs[request_status]))
    except Exception as e:
        error_message = "Error looking up certificate. Error message as follows:\n{}".format(str(e))
        logger.error(error_message)
        raise ConnectorError(error_message)


def lookup_ip(config, params):
    try:
        ipaddr = params.get("ipaddr")
        url = "{0}/api/v1/view/ipv4/{1}".format(config.get("url"), ipaddr)
        request_status, request_result = _api_call(url, method='GET')
        if request_status == 200:
            return {"status_code": request_status, "response": request_result}
        else:
            raise ConnectorError('{}'.format(error_msgs[request_status]))
    except Exception as e:
        error_message = "Error looking up IP address. Error message as follows:\n{}".format(str(e))
        logger.error(error_message)
        raise ConnectorError(error_message)


def check_health(config):
    try:
        request_status, request_result = lookup_domain(config, params={"domain": "cybersponse.com"})
        if request_status == 200:
            return True
        else:
            raise ConnectorError('{}'.format(error_msgs[request_status]))
    except Exception as e:
        error_message = "Error in health check. Error message as follows:\n{}".format(str(e))
        logger.error(error_message)
        raise ConnectorError(error_message)


operations = {
    'lookup_domain': lookup_domain,
    'lookup_cert': lookup_cert,
    'lookup_ip': lookup_ip,
    'check_health': check_health
}
