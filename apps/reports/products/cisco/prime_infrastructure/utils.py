import logging

logger = logging.getLogger(__name__)


class CiscoPrimeResource():
    """ Get resources from Cisco Prime Infra API """

    def __init__(self, url, username, password, **params):
        self.url = url
        self.username = username
        self.password = password
        self.params = params
        self.headers = {'Accept': 'application/json'}

    def get_result(self):
        """ Returns resources from Cisco Prime Infra API
        :returns: request.models.Response object
        """
        import requests
        from requests.auth import HTTPBasicAuth

        logger.debug('Requesting data from endpoint: {}'.format(self.url))
        r = requests.get(self.url, params=self.params, auth=HTTPBasicAuth(self.username,
                                                                          self.password),
                         verify=False, headers=self.headers)

        if not r.status_code == requests.codes.ok:
            logger.critical("We could not run the report: {}".format(self.url))
            import pdb
            pdb.set_trace()
            r.raise_for_status()

        return r