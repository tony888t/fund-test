from rest_framework import viewsets

from fund.models import Fund
from fund.serializers import FundSerializer


class FundViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Return fund details via endpoint `/funds/.
    Can filter by strategy (LSE, GLM, ARB) like so - /funds/?strategy=LSE .
    Can get fund by id like so - /funds/1 .
    """

    serializer_class = FundSerializer

    def get_queryset(self):
        queryset = Fund.objects.all()
        strategy = self.request.query_params.get("strategy")
        if strategy:
            queryset = queryset.filter(strategy=strategy)

        return queryset
