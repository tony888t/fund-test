from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from fund.tests.factories import FundFactory
from fund.models import Fund


class FundViewSetTestCase(APITestCase):
    def setUp(self):
        self.fund = FundFactory(strategy=Fund.Strategy.ARBITRAGE)
        self.second_fund = FundFactory(strategy=Fund.Strategy.GLOBAL_MACRO)
        self.url = reverse("fund-list")
        self.detail_url = reverse(
            "fund-detail", kwargs={"pk": self.second_fund.id}
        )

    def test_get_all_funds(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp_data = resp.json()
        self.assertEqual(len(resp_data), 2)

    def test_search_by_strategy(self):
        url = self.url + f"?strategy={self.fund.strategy}"
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_data = resp.json()
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp_data[0]["id"], self.fund.id)
        self.assertEqual(resp_data[0]["name"], self.fund.name)
        self.assertEqual(resp_data[0]["strategy"], self.fund.strategy)
        self.assertEqual(resp_data[0]["aum"], self.fund.aum)
        self.assertEqual(
            resp_data[0]["inception_date"],
            self.fund.inception_date.strftime("%Y-%m-%d"),
        )

    def test_view_by_id(self):
        resp = self.client.get(self.detail_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_data = resp.json()
        self.assertEqual(resp_data["id"], self.second_fund.id)
        self.assertEqual(resp_data["name"], self.second_fund.name)
        self.assertEqual(resp_data["strategy"], self.second_fund.strategy)
        self.assertEqual(resp_data["aum"], self.second_fund.aum)
        self.assertEqual(
            resp_data["inception_date"],
            self.second_fund.inception_date.strftime("%Y-%m-%d"),
        )

    def test_post_not_possible(self):
        resp = self.client.post(self.url, data={"test": "test_data"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_possible(self):
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_possible(self):
        resp = self.client.patch(self.detail_url, data={"test": "test_data"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_possible(self):
        url = reverse("fund-detail", kwargs={"pk": self.second_fund.id})
        resp = self.client.put(self.detail_url, data={"test": "test_data"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
