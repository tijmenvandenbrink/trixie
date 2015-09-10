from utils import CiscoPrimeResource
from urlparse import urlparse
import time


class PortSummary:
    """
        Returns port summary (ports up, oper down, admin down) for one or more devices from Cisco Prime Infra

    :param url: Base URL incl credentials for Cisco Prime server (e.g. https://username:password@ip_address:port/)
    :type url: string
    :param ip_address: List of IP addresses for which to retrieve the port summary data
    :type ip_address: List of IP addresses

    :returns: list
    """

    def __init__(self, url, ip_addresses=[], **kwargs):
        self.RESOURCE_URL = '/webacs/api/v1/op/statisticsService/device/portSummary'
        self.ip_addresses = ip_addresses
        self.params = kwargs

        obj = urlparse(url)
        self.username = obj.username
        self.password = obj.password
        self.port = obj.port
        self.hostname = obj.hostname
        self.scheme = obj.scheme

    def get_url(self):
        return "{}://{}:{}/{}".format(self.scheme, self.hostname, self.port, self.RESOURCE_URL)

    def get_result(self):
        """
        :return: List of dictionaries: [{'1.1.1.1': {u'Administratively Down Ports': 27,
                                                     u'Up Ports': 136,
                                                     u'Operationally Down Ports': 8}},
                                        {'2.2.2.2': {u'Administratively Down Ports': 27,
                                                     u'Up Ports': 136,
                                                     u'Operationally Down Ports': 8}}]
        """
        result = []
        for ip in self.ip_addresses:
            params = self.params
            params['ipAddress'] = ip
            resource = CiscoPrimeResource(self.get_url(), self.username, self.password, **params)
            data = resource.get_result()
            device_result = {ip: {}}
            try:
                for child in data.json()['mgmtResponse']['statisticsDTO']['childStatistics']['childStatistic']:
                    device_result[ip][child['statisticEntries']['statisticEntry'][1]['entryValue']] = child['statisticEntries']['statisticEntry'][0]['entryValue']
            except KeyError:
                continue

            result.append(device_result)
            time.sleep(0.5)

        return result


class Port:
    """ Placeholder for Port objects
    """
    pass


class PortSummaryReport:
    """
        Returns port summary (ports up, oper down, admin down) for all devices in Cisco Prime Infra

    :param url: Base URL incl credentials for Cisco Prime server (e.g. https://username:password@ip_address:port/)
    :type url: string

    :returns: dict
    """
    def __init__(self, url, **params):
        self.RESOURCE_URL = '/webacs/api/v1/op/reportService/report'
        self.params = params

        obj = urlparse(url)
        self.username = obj.username
        self.password = obj.password
        self.port = obj.port
        self.hostname = obj.hostname
        self.scheme = obj.scheme

    def get_url(self):
        return "{}://{}:{}/{}".format(self.scheme, self.hostname, self.port, self.RESOURCE_URL)

    def get_result(self):
        """
        :return: List of Port objects
        """
        report = CiscoPrimeResource(self.get_url(), self.username, self.password, **self.params)
        data = report.get_result()
        result = []

        try:
            for dataRow in data.json()['mgmtResponse']['reportDataDTO']['dataRows']['dataRow']:
                port = Port()
                for entry in dataRow['entries']['entry']:
                    setattr(port, entry['attributeName'], entry['dataValue'])
                result.append(port)
            return result
        except:
            import pdb
            pdb.set_trace()