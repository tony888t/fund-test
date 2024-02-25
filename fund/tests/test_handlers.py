from collections import namedtuple, OrderedDict

from django.test import TestCase

from fund.views import process_csv_handler
from fund.models import Fund


class HandlerTestCase(TestCase):
    def setUp(self):
        Data = namedtuple(
            "Fund", ("name", "strategy", "aum", "inception_date")
        )

        self.valid_data = Data(
            "test fund",
            Fund.Strategy.LONG_SHORT_EQUITY.label,
            30000,
            "2023-04-30",
        )
        self.invalid_data = Data(
            "test fund", Fund.Strategy.GLOBAL_MACRO.label, None, "2023-04-30"
        )
        self.file_name = "Test-File.csv"

    def test_process_csv_with_valid_data(self):
        """
        Test data is only saved when all data is present
        """
        process_csv_handler([self.valid_data], self.file_name)

        funds = Fund.objects.all()
        self.assertEqual(len(funds), 1)

    def test_process_csv_with_invalid_data(self):
        """
        Test data is not save when not all data is present
        """
        process_csv_handler([self.invalid_data], self.file_name)

        funds = Fund.objects.all()
        self.assertFalse(funds)
