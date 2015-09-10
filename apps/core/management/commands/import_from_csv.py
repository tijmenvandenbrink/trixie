from optparse import make_option

from django.core.management.base import BaseCommand

#todo Create csv import command
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (make_option('-f', '--csvfile',
                                                         dest='csv_file',
                                                         help='Specify csv file'),
                                             make_option('-d', '--dry',
                                                         action='store_true',
                                                         dest='dry',
                                                         default=False,
                                                         help="Don't actually do the upload"),
    )

    args = "period"
    help = ("Uploads availability/volume reports to VERS for a specific time period (default=monthly)\n\n"
            "action can be: insert, delete\n"
            "type can be: ip_volume, ip_availability, lp_volume, lp_availability\n"
            "period format: YYYY-MM")

    def handle(self, period, *args, **options):
        """
        Uploads availability/volume reports to VERS for a specific time period (default=monthly)

        :param action: tells whether to insert or delete the report from VERS
        :type action: string
        :param report_type: specifies the report type (i.e. ip_volume, ip_availability, lp_volume, lp_availability, all)
        :type report_type: string
        :param period: date (YYYY-MM)
        :type period: string
        """